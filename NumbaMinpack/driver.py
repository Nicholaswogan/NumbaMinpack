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
                   ct.c_void_p, ct.c_void_p, ct.c_void_p]
lmdif1.restype = None

@njit
def lmdif(funcptr, x_init, neqs, args, tol = 1.49012e-8, maxfev = 0):
    """Solve for least squares with MINPACK's Levenberg-Marquardt routine.

    Parameters
    ----------
    funcptr : int
        Address (pointer) to the function defining the system of equtions.
    x_init : np.array([np.float64])
        Initial solution guess
    neqs : np.int32
        Number of equations (len(fvec), in funcptr).
    args : np.array([np.float64])
        Arguments to pass to function defining the system of equations.
    tol : np.float64
        Relative solution tolerance.
    maxfev : np.int32
        Maximum number of calls to the function defining the system of equations

    Returns
    -------
    x : np.array([np.float64])
        Solution to the system of equations
    fvec : np.array([np.float64])
        funcptr evaluated at the solution, x
    success : bool
        True if hybrd did not reaturn an error
    info : int
        Integer giving more information about why algorithm stopped.
        See lmdif1.f
    """
    
    m = np.array(neqs,np.int32)
    n = np.array(x_init.size,np.int32)
    x = np.asarray(x_init,np.float64).copy()
    fvec = np.zeros((neqs,),np.float64)
    tol_ = np.array(tol,np.float64)
    maxfev1 = np.array(maxfev,np.int32)
    if maxfev1 == 0:
        maxfev_ = np.array(200*(n + 1),np.int32)
    else:
        maxfev_ = maxfev1
    info = np.array(0,np.int32)
    iwa = np.array(x_init.shape,np.int32)
    lwa = np.array((m*n+5*n+m)+2,np.int32)
    wa = np.zeros((lwa.item(),),np.float64)
    args = np.asarray(args,np.float64)
    k = np.array(len(args),np.int32)
    
    lmdif1(funcptr,m.ctypes.data,n.ctypes.data,x.ctypes.data, \
           fvec.ctypes.data,tol_.ctypes.data, \
           maxfev_.ctypes.data, info.ctypes.data,iwa.ctypes.data, \
           wa.ctypes.data,lwa.ctypes.data,args.ctypes.data,k.ctypes.data)

    if 1 <= info <= 4:
        success = True
    else:
        success = False
           
    return x, fvec, success, info.item()


hybrd1 = minpack.hybrd1_wrapper
hybrd1.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, \
                   ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, \
                   ct.c_void_p]
hybrd1.restype = None    
    
@njit
def hybrd(funcptr, x_init, args, tol = 1.49012e-8, maxfev = 0):
    """Find the roots of a multivariate function using MINPACK’s hybrd
    routine (modified Powell method).

    Parameters
    ----------
    funcptr : int
        Address (pointer) to the function defining the system of equtions.
    x_init : np.array([np.float64])
        Initial solution guess
    args : np.array([np.float64])
        Arguments to pass to function defining the system of equations.
    tol : np.float64
        Relative solution tolerance.
    maxfev : np.int32
        Maximum number of calls to the function defining the system of equations

    Returns
    -------
    x : np.array([np.float64])
        Solution to the system of equations
    fvec : np.array([np.float64])
        funcptr evaluated at the solution, x
    success : bool
        True if hybrd did not reaturn an error
    info : int
        Integer giving more information about why algorithm stopped.
        See hybrd1.f
    """

    
    n = np.array(x_init.size,np.int32)
    x = np.asarray(x_init,np.float64).copy()
    fvec = np.zeros((n.item(),),np.float64)
    tol_ = np.array(tol,np.float64)
    maxfev1 = np.array(maxfev,np.int32)
    if maxfev1 == 0:
        maxfev_ = np.array(200*(n + 1),np.int32)
    else:
        maxfev_ = maxfev1
    info = np.array(0,np.int32)
    lwa = np.array((n*(3*n+13))/2+2,np.int32)
    wa = np.zeros((lwa.item(),),np.float64)
    args = np.asarray(args,np.float64)
    k = np.array(len(args),np.int32)
    
    hybrd1(funcptr,n.ctypes.data,x.ctypes.data, \
           fvec.ctypes.data,tol_.ctypes.data, \
           maxfev_.ctypes.data, info.ctypes.data, \
           wa.ctypes.data,lwa.ctypes.data,args.ctypes.data,k.ctypes.data)

    if info == 1:
        success = True
    else:
        success = False
           
    return x, fvec, success, info.item()