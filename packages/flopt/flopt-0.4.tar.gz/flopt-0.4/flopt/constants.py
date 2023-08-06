VERSION = '0.4'
DATE = 'August 12, 2021'

# termination state
SOLVER_NORMAL_TERMINATE    = 0
SOLVER_TIMELIMIT_TERMINATE = 1
SOLVER_INTERRUPT_TERMINATE = 2
SOLVER_ABNORMAL_TERMINATE  = 3

# error handlings
class SolverError(Exception):
    pass

