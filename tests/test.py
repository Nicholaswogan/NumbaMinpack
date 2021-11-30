from NumbaMinpack import lmdif, hybrd, minpack_sig
from numba import njit, cfunc
import numpy as np

@cfunc(minpack_sig)
def myfunc(x, fvec, args):
    fvec[0] = x[0]**2 - args[0]
    fvec[1] = x[1]**2 - args[1]    
funcptr = myfunc.address

def test_lmdif():
    x_init = np.array([10.0,10.0]) 
    neqs = 2
    args = np.array([30.0,8.0])
    xsol, fvec, success, info = lmdif(funcptr, x_init, neqs, args) 
    assert np.isclose(xsol[0],np.sqrt(args[0]))
    assert np.isclose(xsol[1],np.sqrt(args[1]))
    
def test_hybrd():
    x_init = np.array([10.0,10.0]) 
    args = np.array([30.0,8.0])
    xsol, fvec, success, info = hybrd(funcptr, x_init, args)
    assert np.isclose(xsol[0],np.sqrt(args[0]))
    assert np.isclose(xsol[1],np.sqrt(args[1]))

