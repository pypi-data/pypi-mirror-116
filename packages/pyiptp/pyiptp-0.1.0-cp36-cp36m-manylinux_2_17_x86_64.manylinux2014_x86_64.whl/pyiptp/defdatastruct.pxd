cimport cython

ctypedef struct c_point1d:
    double t
    double val
    unsigned int order

cdef c_point1d make_point(double t, double val, unsigned int order)

cdef class PyIPTPObject:
    @staticmethod
    cdef PyIPTPObject c_loadxml(str fname, str ID)
    cpdef dict _getAttrib(self)
    cpdef void _addPyIPTPObject(self, object root, str ID)
    cpdef void _updatePyIPTPObject(self, object tree, object node, str ID)
    cpdef void savexml(self, str fname, str ID)

cdef class Point1d(PyIPTPObject):
    cdef c_point1d p
    @staticmethod
    cdef Point1d c_loadxml(str fname, str ID)
    cpdef Point1d copy(self)
    cpdef dict _getAttrib(self)
    cpdef void _addPyIPTPObject(self, object root, str ID)
    cpdef void _updatePyIPTPObject(self, object tree, object node, str ID)
    cpdef void savexml(self, str fname, str ID)

ctypedef fused constr:
    Point1d
    tuple

cdef class Trajectory1d(PyIPTPObject):
    cdef readonly int p, n
    cdef readonly unsigned int order
    cdef double *_knotvector
    cdef double *_cpts
    cdef bint ptrs_owner
    @staticmethod
    cdef Trajectory1d from_ptrs(double *knotvector, double *cpts, int p,
                                int n, unsigned int order, bint owner=*)
    @staticmethod
    cdef Trajectory1d new_struct(int p, int n, unsigned int order)
    @staticmethod
    cdef Trajectory1d c_loadxml(str fname, str ID)
    cdef bint c_eq(self, Trajectory1d other) except? False
    cdef void c_iadd(self, double x) nogil
    cdef void c_imul(self, double x) nogil
    cpdef Trajectory1d c_splcsum(self, Trajectory1d other)
    cpdef Trajectory1d c_splcmul(self, Trajectory1d other)
    cpdef bytes _sget_knotvector(self)
    cpdef bytes _sget_cpts(self)
    cpdef void _dset_data(self, bytes knots, bytes cpts, int p, int n,
                          unsigned int order, bint owner)
    cpdef double peval(self, double x)
    cpdef void ceval(self, double[::1] xp)
    cpdef double dpeval(self, double x, int nu = *)
    cpdef void dceval(self, double[::1] xp, int nu = *)
    cdef void c_shift(self, double x) nogil
    cpdef void rshift(self, double x)
    cpdef void ashift(self, double x)
    cdef void c_hscale(self, double x) nogil
    cpdef void hscale(self, double x)
    cpdef void adapt(self, double start, double stop)
    cpdef Trajectory1d derivative(self, int nu = *)
    cpdef Trajectory1d antiderivative(self, int nu = *)
    cpdef Trajectory1d knotins(self, double u, int r)
    cpdef Trajectory1d knotref(self, double[::1] X)
    cpdef Trajectory1d knotrem(self, double u, int r, double tol = *)
    cpdef Trajectory1d knotsrem(self, double tol = *)
    cpdef Trajectory1d knotrem_notol(self, double u, int r)
    cpdef Trajectory1d copy(self)
    cpdef Trajectory1d degelev(self, int nu = *)
    cpdef void setValueTr(self, constr p)
    cpdef void setValueAm(self, constr p)
    cpdef dict _getAttrib(self)
    cpdef void _addPyIPTPObject(self, object root, str ID)
    cpdef void _updatePyIPTPObject(self, object tree, object node, str ID)
    cpdef void savexml(self, str fname, str ID)