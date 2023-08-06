# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: infertypes=True
# cython: initializedcheck=False
# cython: cdivision=True
# cython: language_level=3
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# coding: utf8

"""
Factory functions module; contains the functions for building trajectory
sections as Trajectory1d objects.

All functions
----------------
bspltraj
fromdata
fromdatatdma
fromdatawaed
constant
zeros
ones
lin1p
lin2p
sintraj
costraj
polytraj

"""
import numpy as np
cimport numpy as np
np.import_array()

from libc.string cimport memcpy as c_memcpy
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.math cimport sin, cos, M_PI, fabs, sqrt
from scipy.linalg.cython_lapack cimport dtptrs
from .defdatastruct cimport Trajectory1d
from .basicfunc cimport join
from .cython_ubsplclib cimport (
        validknots,
        averaging,
        averaging2,
        averaging3,
        gcsplint,
        gdsplint,
        gadsplint,
        cdsplint,
        getbmtxelement
        )

__all__ = [
        "bspltraj",
        "fromdata",
        "fromdatatdma",
        "fromdatawaed",
        "constant",
        "zeros",
        "ones",
        "lin1p",
        "lin2p",
        "sintraj",
        "costraj",
        "polytraj"
        ]

cpdef Trajectory1d bspltraj(double[::1] knots, double[::1] cpts, int p,
                            int order):
    """
    Returns a new Trajectory1d object from knot vector and control points.
    
    Parameters
    ----------
    knots: double C-contiguous array
        Knot vector (size m + 1, with m = n + p + 1). The first and the last
        knots must have multiplicity p + 1 so that:
            
            u_(0) = ... = u_(p)     &     u_(m - p) = ... = u_(m)
    
    cpts: double C-contiguous array
        Control points (size n + 1).
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef int n = cpts.shape[0] - 1
    cdef int N = n + 1, M = n + p + 2
    cdef Trajectory1d result
    
    if p < 0:
        raise ValueError("'p' must be greater than or equal to zero")
    if validknots(p, knots):
        raise ValueError("inconsistent 'knots' vector")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    cdef double *knotvector = <double*>PyMem_Malloc(M*sizeof(double))
    if knotvector is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *_cpts = <double*>PyMem_Malloc(N*sizeof(double))
    if _cpts is NULL:
        raise MemoryError("memory allocation failed")
    
    c_memcpy(_cpts, &cpts[0], N*sizeof(double))
    c_memcpy(knotvector, &knots[0], M*sizeof(double))
    
    result = Trajectory1d.from_ptrs(knotvector, _cpts, p, n, order,
                                    owner = True)
    return result

cpdef Trajectory1d fromdata(double[::1] xp, double[::1] fp, int p, int order,
                        bint clamp = False, (double, double) dy = (0., 0.)):
    """
    Returns a new Trajectory1d object from the interpolating points.
    
    Parameters
    ----------
    xp: double C-contiguous array
        The x-coordinates of the data points, must be increasing. If 'clamp'
        is True at least size p + 3, otherwise at least size p + 1.
    fp: double C-contiguous array
        The y-coordinates of the data points, same size as xp.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    clamp: bint
        If True, the 1st derivatives at the extreme points are fixed.
    dy: two-elements ctuple
        If 'clamp' is False it is ignored, otherwise the slope of the first
        and end point.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef int n = xp.shape[0] - 1
    cdef int H = n + 2 if clamp else n
    cdef int N = H + 1, M = H + p + 2
    cdef Trajectory1d result
    
    if not xp.shape[0] == fp.shape[0]:
        raise ValueError("'fp' must have the same length as 'xp'")
    if not issorted(xp, n + 1):
        raise ValueError("'xp' must be increasing")
    if p <= 0 or (clamp and p <= 1):
        raise ValueError("inconsistent 'p' value")
    if n < p or (clamp and n < p + 2):
        raise ValueError("degree inconsistent with the number of data points")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    cdef double *knotvector = <double*>PyMem_Malloc(M*sizeof(double))
    if knotvector is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] knotvector_mv = <double[:M]>knotvector
    
    cdef double *cpts = <double*>PyMem_Malloc(N*sizeof(double))
    if cpts is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] cpts_mv = <double[:N]>cpts
    
    try:
        if clamp: # clamped interpolation
            averaging2(xp, p, knotvector_mv)
            gdsplint(xp, fp, p, knotvector_mv, cpts_mv, dy)
        else: # free interpolation
            averaging(xp, p, knotvector_mv)
            if p == 1: # control points are the same as to interpolate
                c_memcpy(&cpts_mv[0], &fp[0], N*sizeof(double))
            else:
                gcsplint(xp, fp, p, knotvector_mv, cpts_mv)
        
        result = Trajectory1d.from_ptrs(knotvector, cpts, p, H, order,
                                        owner = True)
        return result
    
    except Exception as exp:
        # return the previously allocated memory to the system
        PyMem_Free(knotvector)
        PyMem_Free(cpts)
        raise exp

cpdef Trajectory1d fromdatatdma(double[::1] xp, double[::1] fp, int order,
                                (double, double) dy = (0., 0.)):
    """
    Returns a new Trajectory1d object from the interpolating points and the
    first derivatives of the bounded points. This function uses the TDMA
    (TriDiagonal Matrix Algorithm) for interpolation with cubic splines and
    the 'p' attribute is set to 3. This method generally more efficient than
    the 'fromdata' function.
    
    Parameters
    ----------
    xp: double C-contiguous array
        The x-coordinates of the data points, must be increasing. At least
        size 6.
    fp: double C-contiguous array
        The y-coordinates of the data points, same size as xp.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    dy: two-elements ctuple
        The slope of the first and end point.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object with attribute 'p' equal to 3.
    
    """
    cdef int n = xp.shape[0] - 1
    cdef int N = n + 3, M = n + 7
    cdef Trajectory1d result
    
    if not xp.shape[0] == fp.shape[0]:
        raise ValueError("'fp' must have the same length as 'xp'")
    if not issorted(xp, n + 1):
        raise ValueError("'xp' must be increasing")
    if n < 5:
        raise ValueError("too few data points")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    cdef double *knotvector = <double*>PyMem_Malloc(M*sizeof(double))
    if knotvector is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] knotvector_mv = <double[:M]>knotvector
    
    cdef double *cpts = <double*>PyMem_Malloc(N*sizeof(double))
    if cpts is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] cpts_mv = <double[:N]>cpts
    
    try:
        cdsplint(xp, fp, knotvector_mv, cpts_mv, dy)
        result = Trajectory1d.from_ptrs(knotvector, cpts, 3, n + 2, order,
                                        owner = True)
        return result
    
    except Exception as exp:
        # return the previously allocated memory to the system
        PyMem_Free(knotvector)
        PyMem_Free(cpts)
        raise exp

cpdef Trajectory1d fromdatawaed(double[::1] xp, double[::1] fp, int p,
                                int order, double[::1] Ds, double[::1] De):
    """
    Returns a new Trajectory1d object from the interpolating points with
    Arbitrary End Derivatives.
    
    Parameters
    ----------
    xp: double C-contiguous array
        The x-coordinates of the data points, must be increasing. If 'clamp'
        is True at least size p + 3, otherwise at least size p + 1.
    fp: double C-contiguous array
        The y-coordinates of the data points, same size as xp.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    Ds: double C-contiguous array
        Derivates at the start point.
    De: double C-contiguous array
        Derivates at the end point.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef:
        int n = xp.shape[0]
        int k = Ds.shape[0]
        int l = De.shape[0]
        int d = max(k, l)
        int N = n + k + l, M = N + p + 1
        Trajectory1d result
    
    if not fp.shape[0] == n:
        raise ValueError("'fp' must have the same length as 'xp'")
    if not issorted(xp, n):
        raise ValueError("'xp' must be increasing")
    if p <= 1:
        raise ValueError("inconsistent 'p' value")
    if n < p:
        raise ValueError("degree inconsistent with the number of data points")
    if not d < p:
        raise ValueError(
            "the maximum constrained derivative must be less than 'p'")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    cdef double *knotvector = <double*>PyMem_Malloc(M*sizeof(double))
    if knotvector is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] knotvector_mv = <double[:M]>knotvector
    
    cdef double *cpts = <double*>PyMem_Malloc(N*sizeof(double))
    if cpts is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] cpts_mv = <double[:N]>cpts
    
    try:
        averaging3(xp, p, k, l, knotvector_mv)
        gadsplint(xp, fp, p, Ds, De, knotvector_mv, cpts_mv)
        result = Trajectory1d.from_ptrs(knotvector, cpts, p, N - 1, order,
                                        owner = True)
        return result
    
    except Exception as exp:
        # return the previously allocated memory to the system
        PyMem_Free(knotvector)
        PyMem_Free(cpts)
        raise exp

cpdef Trajectory1d constant(double start, double stop, int p, int order,
                            double k):
    """
    Returns a new Trajectory1d object with interpolation points with constant
    value 'k' and zero slope.
    
    Parameters
    ----------
    start: number
        The starting value of the domain.
    stop: number
        The end value of the domain. Must be greater than 'start'.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    k: double
        Constant value.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef Py_ssize_t i
    cdef Trajectory1d result
    
    if start > stop:
        raise ValueError("'stop' must be greater than 'start'")
    if p < 0:
        raise ValueError(f"'p' must be greater than or equal to zero: {p}")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    cdef double *knotvector = <double*>PyMem_Malloc(2*(p + 1)*sizeof(double))
    if knotvector is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *cpts = <double*>PyMem_Malloc((p + 1)*sizeof(double))
    if cpts is NULL:
        raise MemoryError("memory allocation failed")
    
    with nogil:
        for i in range(p + 1): # Bezier curve
            knotvector[i] = start
            knotvector[2*p + 1 - i] = stop
            cpts[i] = k
    
    result = Trajectory1d.from_ptrs(knotvector, cpts, p, p, order,
                                    owner = True)
    return result

cpdef Trajectory1d zeros(double start, double stop, int p, int order):
    """
    Returns a new constant Trajectory1d object with value 0.
    
    Parameters
    ----------
    start: number
        The starting value of the trajectory.
    stop: number
        The end value of the trajectory. Must be greater than 'start'.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef Trajectory1d result
    
    result = constant(start, stop, p, order, k = 0.)
    return result

cpdef Trajectory1d ones(double start, double stop, int p, int order):
    """
    Returns a new constant Trajectory1d object with value 1.
    
    Parameters
    ----------
    start: number
        The starting value of the trajectory.
    stop: number
        The end value of the trajectory. Must be greater than 'start'.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef Trajectory1d result
    
    result = constant(start, stop, p, order, k = 1.)
    return result

cpdef Trajectory1d lin1p(double start, double stop, int p, int order,
                         (double, double) pt, double m):
    """
    Returns a new Trajectory1d object with interpolation points ​​placed on a
    straight line passing through one data point and assigned slope.
    
    Parameters
    ----------
    start: number
        The starting value of the trajectory.
    stop: number
        The end value of the trajectory. Must be greater than 'start'.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    pt: two-elements ctuple
        Point -> (x, y).
    m: double
        Slope of the line.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef Py_ssize_t i
    cdef double q, b
    cdef Trajectory1d result
    
    if start > stop:
        raise ValueError("'stop' must be greater than 'start'")
    if p < 1:
        raise ValueError(f"'p' must be at least 1: {p}")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    cdef double *knotvector = <double*>PyMem_Malloc(2*(p + 1)*sizeof(double))
    if knotvector is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *cpts = <double*>PyMem_Malloc((p + 1)*sizeof(double))
    if cpts is NULL:
        raise MemoryError("memory allocation failed")
    
    with nogil:
        q = pt[1] - m*pt[0]
        b = stop - start
        
        for i in range(p + 1): # Bezier curve
            knotvector[i] = start
            knotvector[2*p + 1 - i] = stop
            cpts[i] = m*(start + <double>i*b/<double>p) + q
    
    result = Trajectory1d.from_ptrs(knotvector, cpts, p, p, order,
                                    owner = True)
    return result

cpdef Trajectory1d lin2p(double start, double stop, int p, int order,
                         (double, double) pt1, (double, double) pt2):
    """
    Returns a new Trajectory1d object with interpolation points ​​placed on a
    straight line passing through two data points.
    
    Parameters
    ----------
    start: number
        The starting value of the trajectory.
    stop: number
        The end value of the trajectory. Must be greater than 'start'.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    pt1: two-elements ctuple
        Point one -> (x1, y1).
    pt2: two-elements ctuple
        Point two -> (x2, y2).
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef Py_ssize_t i
    cdef double m
    cdef Trajectory1d result
    
    if pt1[0] == pt2[0]:
        raise ZeroDivisionError("infinite slope is not allowed")
    
    m = (pt2[1] - pt1[1])/(pt2[0] - pt1[0])
    result = lin1p(start, stop, p, order, pt1, m)
    return result

cdef diffsin(double x, double amp, double ph, double k, int nu,
             double[::1] D):
    cdef Py_ssize_t i
    cdef int _nu
    cdef double xi = degToRad(k*x + ph)
    
    for i in range(nu):
        _nu = (i + 1)%4
        D[i] = amp*degToRad(k)**<double>(i + 1)
        
        if _nu == 0:
            D[i] *= sin(xi)
        elif _nu == 1:
            D[i] *= cos(xi)
        elif _nu == 2:
            D[i] *= - sin(xi)
        elif _nu == 3:
            D[i] *= - cos(xi)
        else:
            assert False

cpdef Trajectory1d sintraj(double[::1] xp, int p, int order, double amp = 1.,
                           double ph = 0., double k = 1., int nu = -1):
    """
    Returns a new Trajectory1d object with interpolation points according
    to the expression:
    
        fp = amp * sin(k * xp + ph) 
    
    Parameters
    ----------
    xp: double C-contiguous array
        The x-coordinates of the points interpolated from the trajectory,
        must be increasing. At least size p + 1.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    amp: double, optional
        Amplitude.
    ph: double, optional
        Phase [deg].
    k: double, optional
        Moltiplicative costant.
    nu: int, optional
        If set, it specifies up to which order the end derivatives are
        constrained. Default p - 1.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef Py_ssize_t i
    cdef int n = xp.shape[0]
    cdef double s = xp[0], e = xp[n - 1]
    cdef double[::1] fp = np.empty(n, dtype = np.float64)
    
    if nu == -1: # Default value
        nu = p - 1
    elif nu < 0:
        raise ValueError("'nu' must be greater than zero")
    
    cdef double[::1] Ds = np.empty(nu, dtype = np.float64)
    cdef double[::1] De = np.empty(nu, dtype = np.float64)
    cdef Trajectory1d result
    
    if not issorted(xp, xp.shape[0]):
        raise ValueError("'xp' must be increasing")
    if p <= 0:
        raise ValueError("'p' must be greater than or equal to zero")
    if n < p + 1:
        raise ValueError("degree inconsistent with the number of data points")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    for i in range(n): # Calculation of interpolated points
        fp[i] = amp * (sin(degToRad(k * xp[i] + ph)))
    
    # Calculation of ends derivatives
    diffsin(s, amp, ph, k, nu, Ds)
    diffsin(e, amp, ph, k, nu, De)
    
    result = fromdatawaed(xp, fp, p, order, Ds, De)
    return result

cpdef Trajectory1d costraj(double[::1] xp, int p, int order, double amp = 1.,
                           double ph = 0., double k = 1., int nu = -1):
    """
    Returns a new Trajectory1d object with interpolation points according
    to the expression:
    
        fp = amp * cos(k * xp + ph) 
    
    Parameters
    ----------
    xp: double C-contiguous array
        The x-coordinates of the points interpolated from the trajectory,
        must be increasing. At least size p + 1.
    p: int
        Degree of the interpolating B-Spline. Must be greater than zero.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    amp: double, optional
        Amplitude.
    ph: double, optional
        Phase [deg].
    k: double, optional
        Moltiplicative costant.
    nu: int, optional
        If set, it specifies up to which order the end derivatives are
        constrained. Default p - 1.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object.
    
    """
    cdef Trajectory1d result
    
    result = sintraj(xp, p, order, amp, ph + 90, k, nu)
    return result

cpdef Trajectory1d polytraj(double start, double stop, int p, int order,
                            double[::1] c, bint dimless = False):
    """
    Returns a new Trajectory1d object with interpolation points according
    to the expression:
        
                    (n-1)           (n-2)
        y = c[0] * x      + c[1] * x      + ... + c[n-2] * x + c[n-1]
    
    with n lenght of the array 'c'.
    
    Parameters
    ----------
    start: number
        The starting value of the trajectory.
    stop: number
        The end value of the trajectory. Must be greater than 'start'.
    p: int
        Degree of the interpolating B-Spline. Must be greater than or equal
        to the degree of the polynomial.
    order: int
        Order of derivation to which the trajectory refers. Must be greater
        than or equal to zero. Example:
            
            0: displacement
            1: velocity
            2: acceleration
            3: jerk
            ...
    
    c: double C-contiguous array
        1-D array of polynomial coefficients (including coefficients equal to
        zero) from highest degree to the constant term.
    dimless: bint
        If True, the coefficients of the polynomial 'c' are relative to a
        normalized domain (from 0.0 to 1.0).This corresponds to replacing
        above x with x / b where b = stop - start.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object with attribute p = n - 1.
    
    """
    cdef:
        Py_ssize_t i, j
        int N = c.shape[0]
        double s, b = stop - start
        Trajectory1d result
    
    if start > stop:
        raise ValueError("'stop' must be greater than 'start'")
    if p < N - 1:
        raise ValueError(f"'p' must be greater than or equal to the degree "
                         "of the polynomial: {p}")
    if order < 0:
        raise ValueError(f"'order' value must be greater than or "
                         "equal to zero: {order}")
    
    if N - 1 == 0:
        result = constant(start, stop, p, order, c[0])
        return result
    elif N - 1 == 1:
        result = lin1p(start, stop, p, order, pt = (0., c[1]), m = c[0])
        return result
    
    cdef double *knotvector = <double*>PyMem_Malloc(2*N*sizeof(double))
    if knotvector is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *cpts = <double*>PyMem_Malloc(N*sizeof(double))
    if cpts is NULL:
        raise MemoryError("memory allocation failed")
    
    try:
        with nogil:
            for i in range(N):
                knotvector[i], knotvector[2*N - i - 1] = start, stop
                cpts[i] = c[N - i - 1]*<double>(1 - <int>dimless)*b**<double>i
                
                s = 0.
                for j in range(i):
                    s += getbmtxelement(N - 1, i, j)*cpts[j]
                
                cpts[i] = (cpts[i] - s)/getbmtxelement(N - 1, i, i)
        
        result = Trajectory1d.from_ptrs(
            knotvector, cpts, N - 1, N - 1, order, owner = True)
        if p > N - 1:
            result = result.degelev(p - N + 1)
        
        return result
    
    except Exception as exp:
        # return the previously allocated memory to the system
        PyMem_Free(knotvector)
        PyMem_Free(cpts)
        raise exp

include "utils.pxi"