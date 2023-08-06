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
This module contains the basic functions to work on the trajectories.

All functions
-------------
join
joins
trajsli
mirror
add
rshift
ashift
hscale
adapt
derivative
antiderivative
setValueTr
setValueAm
setValueSm
savexml
saveallxml

"""
import numpy as np
cimport numpy as np
np.import_array()

from libc.math cimport fabs
from libc.string cimport memcpy as c_memcpy
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from .defdatastruct cimport (
    PyIPTPObject,
    Trajectory1d,
    Point1d,
    constr
    )
from .cython_ubsplclib cimport (
    splcjoin,
    splcsli
    )

__all__ = [
    "join",
    "joins",
    "trajsli",
    "mirror",
    "add",
    "rshift",
    "ashift",
    "hscale",
    "adapt",
    "derivative",
    "antiderivative",
    "setValueTr",
    "setValueAm",
    "setValueSm",
    "savexml",
    "saveallxml"
    ]

cpdef Trajectory1d join(Trajectory1d traj1, Trajectory1d traj2):
    """
    Joins two Trajectory1d object with no-continuity joint. The trajectory to
    the right of the joint will be automatically shifted so that:
    
            traj1.stop == traj2.start
    
    The two Trajectory1d objects must be of the same order, otherwise an
    exception is raised.
    
    Parameters
    ----------
    traj1: Trajectory1d
        Trajectory to the left of the joint. It's kept fixed.
    traj2: Trajectory1d
        Trajectory to the right of the joint.
    rtol: double
        Relative tolerance.
    atol: double
        Absolute tolerance.
    
    Returns
    -------
    out: Trajectory1d
        New Trajectory1d object as junction of the input trajectories.
    
    """
    cdef double[::1] Ul_mv, Pl_mv, Ur_mv, Pr_mv
    cdef int nl, nr
    cdef int p, N, M, order
    cdef Trajectory1d result
    
    if not traj1.p == traj2.p:
        raise ValueError("the input traiectories must have the same order")
    if not traj1.order == traj2.order:
        raise ValueError("the trajectories must have the same 'order'")
    
    p, nl, nr = traj1.p, traj1.n, traj2.n
    order = traj1.order
    ml, mr = nl + p + 1, nr + p + 1
    
    Ul_mv = <double[:ml + 1]>traj1._knotvector
    Pl_mv = <double[:nl + 1]>traj1._cpts
    Ur_mv = <double[:mr + 1]>traj2._knotvector
    Pr_mv = <double[:nr + 1]>traj2._cpts
    
    N = nl + nr + 2
    M = N + p + 1
    
    cdef double *Uh = <double*>PyMem_Malloc(M*sizeof(double))
    if Uh is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] Uh_mv = <double[:M]>Uh
    
    cdef double *Ph = <double*>PyMem_Malloc(N*sizeof(double))
    if Ph is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] Ph_mv = <double[:N]>Ph
    
    splcjoin(Ul_mv, Pl_mv, Ur_mv, Pr_mv, p, Uh_mv, Ph_mv)
    
    result = Trajectory1d.from_ptrs(Uh, Ph, p, N - 1, order, owner=True)
    return result

def joins(*trajs) -> Trajectory1d:
    """
    Wrapper of 'join()' function. Returns the sorted concatenation of more
    Trajectory1d objects with no-continuity junctions.
    
    """
    cdef int n
    cdef Trajectory1d t, result
    
    n = len(trajs)
    if n == 0:
        raise ValueError("at least 1 item required")
    
    result = trajs[0]
    
    for t in trajs[1:]:
        result = join(result, t)
    return result

cpdef tuple trajsli(Trajectory1d traj, double x):
    """
    Separate a trajectory to a specific domain value, returning two new
    Trajectory1d objects corresponding to the left and right pieces of the
    initial trajectory.
    
    Parameters
    ----------
    traj: Trajectory1d
        Trajectory to be separated.
    x: double
        X-coordinate where you want to slice the trajectory.
    
    Returns
    -------
    trajl: Trajectory1d
        Left piece of the input trajectory.
    trajr: Trajectory1d
        Right piece of the input trajectory.
    
    """
    cdef double[::1] U_mv, P_mv
    cdef int p = traj.p
    cdef int N = traj.n + 1
    cdef int M = N + p + 1
    cdef int nl, nr
    cdef int order = traj.order
    cdef Trajectory1d trajl, trajr
    
    if x < traj.start or x > traj.stop:
        raise ValueError("'x' out of domain: {}".format(x))
    
    U_mv = <double[:M]>traj._knotvector
    P_mv = <double[:N]>traj._cpts
    
    cdef double *Uk = <double*>PyMem_Malloc((M + p + 1)*sizeof(double))
    if Uk is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] Uk_mv = <double[:(M + p + 1)]>Uk
    
    cdef double *Pk = <double*>PyMem_Malloc((N + p + 1)*sizeof(double))
    if Pk is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double[::1] Pk_mv = <double[:(N + p + 1)]>Pk
    
    nl, nr = splcsli(U_mv, P_mv, p, x, Uk_mv, Pk_mv)
    
    cdef double *Ul = <double*>PyMem_Malloc((nl + p + 2)*sizeof(double))
    if Ul is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *Ur = <double*>PyMem_Malloc((nr + p + 2)*sizeof(double))
    if Ur is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *Pl = <double*>PyMem_Malloc((nl + 1)*sizeof(double))
    if Pl is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *Pr = <double*>PyMem_Malloc((nr + 1)*sizeof(double))
    if Pr is NULL:
        raise MemoryError("memory allocation failed")
    
    c_memcpy(Ul, Uk, (nl + p + 2)*sizeof(double))
    c_memcpy(Ur, &Uk[nl + 1], (nr + p + 2)*sizeof(double))
    c_memcpy(Pl, Pk, (nl + 1)*sizeof(double))
    c_memcpy(Pr, &Pk[nl + 1], (nr + 1)*sizeof(double))
    
    PyMem_Free(Uk); PyMem_Free(Pk)
    
    trajl = Trajectory1d.from_ptrs(Ul, Pl, p, nl, order, owner=True)
    trajr = Trajectory1d.from_ptrs(Ur, Pr, p, nr, order, owner=True)
    
    return trajl, trajr

cpdef Trajectory1d mirror(Trajectory1d traj):
    """
    Returns a new Trajectory1d object as a mirror of the input trajectory.
    
    Parameters
    ----------
    traj: Trajectory1d
        Trajectory input.
    
    Returns
    -------
    out: Trajectory1d
        New trajectory mirrored to the input one.
    
    """
    cdef double[::1] spanw
    cdef Py_ssize_t i
    cdef int p, N, M, size, order
    cdef Trajectory1d result
    cdef double *U = traj._knotvector
    cdef double *P = traj._cpts
    
    p = traj.p
    order = traj.order
    N = traj.n + 1
    M = N + p + 1
    
    size = M - 2*(p + 1) + 1
    spanw = np.empty(size, dtype=np.float64)
    
    cdef double *Uh = <double*>PyMem_Malloc(M*sizeof(double))
    if Uh is NULL:
        raise MemoryError("memory allocation failed")
    
    cdef double *Ph = <double*>PyMem_Malloc(N*sizeof(double))
    if Ph is NULL:
        raise MemoryError("memory allocation failed")
    
    with nogil:
        for i in range(N): # reverses ctr pts
            Ph[i] = P[N - 1 - i]
        
        for i in range(size): # span width calc
            spanw[i] = U[i + p + 1] - U[i + p]
        
        # knot vector calc
        for i in range(p + 1):
            Uh[i] = U[M - 1]
            Uh[M - 1 - i] = 2*U[M - 1] - U[0]
        
        for i in range(p + 1, M - p - 1):
            Uh[i] = Uh[i - 1] + spanw[size - i + p]
    
    result = Trajectory1d.from_ptrs(Uh, Ph, p, N - 1, order, owner=True)
    
    return result

# -----------------------------------------------------------------------------
#
# Some wrapper of Trajectory1d methods
#
cpdef Trajectory1d add(Trajectory1d traj1, Trajectory1d traj2):
    """
    Returns a new Trajectory1d object as the sum of two input trajectories.
    'traj1' and 'traj2' must be same order and have the same ends of the
    domain.
    
    Parameters
    ----------
    traj1: Trajectory1d
        Input trajectory 1.
    traj2: Trajectory1d
        Input trajectory 2.
    
    """
    cdef Trajectory1d result
    
    result = traj1.c_splcsum(traj2)
    return result

cpdef Trajectory1d rshift(Trajectory1d traj, double x):
    """
    Returns a new Trajectory1d object as a relative translation of the input
    trajectory.
    
    Parameters
    ----------
    traj: Trajectory1d
        Input trajectory.
    x: double
        Translation value.
    
    """
    cdef Trajectory1d result
    
    result = traj.copy()
    result.c_shift(x)
    return result

cpdef Trajectory1d ashift(Trajectory1d traj, double x):
    """
    Returns a new Trajectory1d object as a translation of the input trajectory
    so that the curve starts at the 'x' coordinate.
    
    Parameters
    ----------
    traj: Trajectory1d
        Input trajectory.
    x: double
        Translation value.
    
    """
    cdef Trajectory1d result
    
    result = traj.copy()
    result.ashift(x)
    return result

cpdef Trajectory1d hscale(Trajectory1d traj, double x):
    """
    Scales the input trajectory horizontally keeping the start of the domain
    fixed and returns a new Trajectory1d object.
    
    Parameters
    ----------
    traj: Trajectory1d
        Input trajectory.
    x: double
        Scale factor.
    
    """
    cdef Trajectory1d result
    
    result = traj.copy()
    result.c_hscale(x)
    return result

cpdef Trajectory1d adapt(Trajectory1d traj, double start, double stop):
    """
    Adapts the input trajectory into a new domain [start, stop] and returns
    a new Trajectory1d object.
    
    Parameters
    ----------
    traj: Trajectory1d
        Input trajectory.
    start: double
        New domain start.
    stop: double
        New domain stop. Must be greather than 'start'.
    
    """
    cdef Trajectory1d result
    
    result = traj.copy()
    result.adapt(start, stop)
    return result

cpdef Trajectory1d derivative(Trajectory1d traj, int nu = 1):
    """
    Returns a new Trajectory1d object as a derivative of the input trajectory.
    
    Parameters
    ----------
    traj: Trajectory1d
        Input trajectory.
    nu: int
        Derivative order. Default is 1.
    
    """
    cdef Trajectory1d result
    
    result = traj.derivative(nu)
    return result

cpdef Trajectory1d antiderivative(Trajectory1d traj, int nu = 1):
    """
    Returns a new Trajectory1d object as a antiderivative of the input
    trajectory.
    
    Parameters
    ----------
    traj: Trajectory1d
        Input trajectory.
    nu: int
        Antiderivative order. Default is 1.
    
    """
    cdef Trajectory1d result
    
    result = traj.antiderivative(nu)
    return result

cpdef void savexml(PyIPTPObject obj, str fname, str ID):
    """
    Wrapper of 'savexml' PyIPTPObject method.
    
    """
    obj.savexml(fname, ID)

def saveallxml(PyIPTPObjectList, fname: str, IDList):
    """
    Saves all elements contained in 'PyIPTPObjectList' in a .xml format file.
    If not specified, the file extension is .pyiptp.
    
    Parameters
    ----------
    PyIPTPObjectList: array-like of PyIPTPObject
        .
    fname: str
        .
    IDList: array-like
        .
    
    """
    cdef Py_ssize_t i
    cdef PyIPTPObject obj
    
    for i, obj in enumerate(PyIPTPObjectList):
        obj.savexml(fname, IDList[i])

# -----------------------------------------------------------------------------
#
# Condition set functions
#
cpdef Trajectory1d setValueTr(Trajectory1d traj, constr p):
    """
    Sets a condition to the Trajectory1d object by vertical shift of the
    trajectory. This method does not work if applied to the n-th integral.
    
    Parameters
    ----------
    traj: Trajectory1d
        Trajectory to which the condition applies.
    p: constr (fused type: Point1d or 3-elements tuple)
        Constraint to be set. If 3-elements tuple must be in format
                
                (t, val, order)
            
        For the description of the 't', 'val' and 'order' attributes
        see Point1d class documentation.
    
    """
    cdef Trajectory1d result
    
    result = traj.copy()
    result.setValueTr(p)
    return result

cpdef Trajectory1d setValueAm(Trajectory1d traj, constr p):
    """
    Sets a condition to the Trajectory1d object multiplying the trajectory by
    a calculated constant. This function cannot be used to set conditions close
    to zero, otherwise the whole trajectory is set to zero.
    
    Parameters
    ----------
    traj: Trajectory1d
        Trajectory to which the condition applies.
    p: constr (fused type: Point1d or 3-elements tuple)
        Constraint to be set. If 3-elements tuple must be in format
                
                (t, val, order)
            
        For the description of the 't', 'val' and 'order' attributes
        see Point1d class documentation.
    
    """
    cdef Trajectory1d result
    
    result = traj.copy()
    result.setValueAm(p)
    return result

cpdef Trajectory1d setValueSm(Trajectory1d traj1, Trajectory1d traj2,
                              constr p):
    """
    Sets a condition to the Trajectory1d object adding another Trajectory1d
    object multiplied by a calculated constant.
    
    Parameters
    ----------
    traj1: Trajectory1d
        Trajectory to which the condition applies.
    traj2: Trajectory1d
        Trajectory used by the function to set the condition.
    p: constr (fused type: Point1d or 3-elements tuple)
        Constraint to be set. If 3-elements tuple must be in format
                
                (t, val, order)
            
        For the description of the 't', 'val' and 'order' attributes
        see Point1d class documentation.
    
    Notes
    -----
    'traj2' is overwritten by the algorithm, you need to make a copy.
    
    """
    cdef:
        double oldvalue, delta
        int relord
        Point1d newp
        Trajectory1d result
    
    if not traj1.order == traj2.order:
        raise ValueError("the trajectories must have the same 'order'")
    
    if type(p) is tuple:
        p = Point1d.from_tuple(p)
    
    relord = p.order - traj1.order
    
    if relord == 0:
        result = traj1.copy()
    elif relord > 0:
        result = traj1.derivative(nu = relord)
    else:
        result = traj1.antiderivative(nu = -relord)
    
    oldvalue = result.peval(p.t)
    delta = p.val - oldvalue
    newp = Point1d(p.t, delta, p.order)
    traj2.setValueAm(newp)
    result = result.c_splcsum(traj2)
    
    if relord > 0:
        result = result.antiderivative(nu = relord)
    elif relord < 0:
        result = result.derivative(nu = -relord)
    
    return result