import ctypes as ct
from numba import njit, types
import numpy as np
import os

minpack_sig = types.void(types.CPointer(types.double),
                   types.CPointer(types.double),
                   types.CPointer(types.double))

rootdir = os.path.dirname(os.path.realpath(__file__))+'/'
minpack = ct.CDLL(rootdir+'minpack.so')
lmdif1 = minpack.lmdif1_wrapper
lmdif1.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, \
                   ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, \
                   ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p]
lmdif1.restype = None

@njit
def lmdif(funcptr, x_init, neqs, args, ftol = -1.0, xtol = 1.49012e-8, maxiter = 0):
    
    m = np.array(neqs,np.int32)
    n = np.array(x_init.size,np.int32)
    x = np.asarray(x_init,np.float64).copy()
    fvec = np.zeros((neqs,),np.float64)
    if ftol < 0.0:
        ftol_ = np.array(xtol,np.float64)
    else:
        ftol_ = np.array(ftol,np.float64)
    xtol_ = np.array(xtol,np.float64)
    if maxiter == 0:
        maxiter_ = np.array(200*(n + 1),np.int32)
    else:
        maxiter_ = np.array(maxiter,np.int32)
    info = np.array(0,np.int32)
    iwa = np.array(x_init.shape,np.int32)
    lwa = np.array((m*n+5*n+m)+2,np.int32)
    wa = np.zeros((lwa.item(),),np.float64)
    args = np.asarray(args,np.float64)
    k = np.array(len(args),np.int32)
    
    lmdif1(funcptr,m.ctypes.data,n.ctypes.data,x.ctypes.data, \
           fvec.ctypes.data,ftol_.ctypes.data, xtol_.ctypes.data, \
           maxiter_.ctypes.data, info.ctypes.data,iwa.ctypes.data, \
           wa.ctypes.data,lwa.ctypes.data,args.ctypes.data,k.ctypes.data)

    if 1 <= info <= 4:
        success = True
    else:
        success = False
           
    return x, fvec, success, info.item()


hybrd1 = minpack.hybrd1_wrapper
hybrd1.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, \
                   ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p]
hybrd1.restype = None    
    
@njit
def hybrd(funcptr, x_init, args, tol = 1.49012e-8):
    
    n = np.array(x_init.size,np.int32)
    x = np.asarray(x_init,np.float64).copy()
    fvec = np.zeros((n.item(),),np.float64)
    tol_ = np.array(tol,np.float64)
    info = np.array(0,np.int32)
    lwa = np.array((n*(3*n+13))/2+2,np.int32)
    wa = np.zeros((lwa.item(),),np.float64)
    args = np.asarray(args,np.float64)
    k = np.array(len(args),np.int32)
    
    hybrd1(funcptr,n.ctypes.data,x.ctypes.data, \
           fvec.ctypes.data,tol_.ctypes.data, \
           info.ctypes.data, \
           wa.ctypes.data,lwa.ctypes.data,args.ctypes.data,k.ctypes.data)

    if 1 <= info <= 4:
        success = True
    else:
        success = False
           
    return x, fvec, success, info.item()