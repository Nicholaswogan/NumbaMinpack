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
                   ct.c_void_p, ct.c_void_p]
lmdif1.restype = None

@njit
def lmdif(funcptr, x_init, neqs, args, rtol = 1.0e-8):
    m = np.array(neqs,np.int32)
    n = np.array(x_init.size,np.int32)
    x = np.asarray(x_init,np.float64).copy()
    fvec = np.zeros((neqs,),np.float64)
    tol = np.array(rtol,np.float64)
    info = np.array(0,np.int32)
    iwa = np.array(x_init.shape,np.int32)
    lwa = np.array((m*n+5*n+m)*2,np.int32)
    wa = np.zeros((lwa.item(),),np.float64)
    args = np.asarray(args,np.float64)
    k = np.array(len(args),np.int32)
    
    lmdif1(funcptr,m.ctypes.data,n.ctypes.data,x.ctypes.data, \
           fvec.ctypes.data,tol.ctypes.data,info.ctypes.data,iwa.ctypes.data, \
           wa.ctypes.data,lwa.ctypes.data,args.ctypes.data,k.ctypes.data)

    if info < 1 or info > 5:
        success = False
    else:
        success = True
           
    return x, fvec, success, info.item()