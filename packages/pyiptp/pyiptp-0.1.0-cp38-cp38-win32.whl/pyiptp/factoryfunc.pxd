from .defdatastruct cimport Trajectory1d

cpdef Trajectory1d bspltraj(double[::1] knots, double[::1] cpts, int p,
                            int order)
cpdef Trajectory1d fromdata(double[::1] xp, double[::1] fp, int p, int order,
                            bint clamp = *, (double, double) dy = *)
cpdef Trajectory1d fromdatatdma(double[::1] xp, double[::1] fp, int order,
                                (double, double) dy = *)
cpdef Trajectory1d fromdatawaed(double[::1] xp, double[::1] fp, int p,
                                int order, double[::1] Ds, double[::1] De)
cpdef Trajectory1d constant(double start, double stop, int p, int order,
                            double k)
cpdef Trajectory1d zeros(double start, double stop, int p, int order)
cpdef Trajectory1d ones(double start, double stop, int p, int order)
cpdef Trajectory1d lin1p(double start, double stop, int p, int order,
                         (double, double) pt, double m)
cpdef Trajectory1d lin2p(double start, double stop, int p, int order,
                         (double, double) pt1, (double, double) pt2)
cpdef Trajectory1d sintraj(double[::1] xp, int p, int order, double amp = *,
                           double ph = *, double k = *, int nu = *)
cpdef Trajectory1d costraj(double[::1] xp, int p, int order, double amp = *,
                           double ph = *, double k = *, int nu = *)
cpdef Trajectory1d polytraj(double start, double stop, int p, int order,
                            double[::1] c, bint dimless = *)