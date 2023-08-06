from .defdatastruct cimport PyIPTPObject, Trajectory1d, constr

cpdef Trajectory1d join(Trajectory1d traj1, Trajectory1d traj2)
cpdef tuple trajsli(Trajectory1d traj, double x)
cpdef Trajectory1d mirror(Trajectory1d traj)
cpdef Trajectory1d add(Trajectory1d traj1, Trajectory1d traj2)
cpdef Trajectory1d rshift(Trajectory1d traj, double x)
cpdef Trajectory1d ashift(Trajectory1d traj, double x)
cpdef Trajectory1d hscale(Trajectory1d traj, double x)
cpdef Trajectory1d adapt(Trajectory1d traj, double start, double stop)
cpdef Trajectory1d derivative(Trajectory1d traj, int nu = *)
cpdef Trajectory1d antiderivative(Trajectory1d traj, int nu = *)
cpdef void savexml(PyIPTPObject obj, str fname, str oname)
cpdef Trajectory1d setValueTr(Trajectory1d traj, constr p)
cpdef Trajectory1d setValueAm(Trajectory1d traj, constr p)
cpdef Trajectory1d setValueSm(Trajectory1d traj1, Trajectory1d traj2,
                              constr p)