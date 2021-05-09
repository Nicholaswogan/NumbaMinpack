# NumbaMinpack

`NumbaMinpack` is a light-weight python wrapper to the Levenberg-Marquardt root-finding algorithm in [Minpack](https://en.wikipedia.org/wiki/MINPACK). It very similar to `scipy.optimize.root` ([see here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html)), when you set `method = 'lm'`. But, the problem with `scipy.optimize.root`, is that it can not be used within `numba` jit-compiled python functions. In contrast, `NumbaMinpack` can be used within a numba compiled function. Also, it is much faster than `scipy.optimize.root`, because the python interpreter is never invoked during a non-linear solve. For example, check out `comparison2scipy.ipynb`.

## Installation
`NumbaMinpack` will probably only work on MacOS or Linux. You must have `gfortran` installed. On Mac install with `brew install gcc`. You must also have python >3.6.0 with `numpy` and `numba`.

After satisfying the dependencies, install with the pip command below

```
python -m pip install git+git://github.com/Nicholaswogan/NumbaMinpack.git
```

## Basic usage

```python
from NumbaMinpack import lmdif, minpack_sig
from numba import njit, cfunc
import numpy as np

# System of equations must look like this. Returns nothing!
@cfunc(minpack_sig)
def myfunc(x, fvec, args):
    fvec[0] = x[0]**2 - args[0]
    fvec[1] = x[1]**2 - args[1]
    
funcptr = myfunc.address # pointer to myfunc

@njit
def test():
    x_init = np.array([10.0,10.0]) # initial conditions
    neqs = 2 # number of equations
    args = np.array([30.0,8.0]) # data you want to pass to myfunc
    sol = lmdif(funcptr, x_init, neqs, args) # solve
    return sol
    
xsol, fvec, success, info = test()
# xsol = solution
# fvec = function evaluated at solution
# success = True/False
# info = an integer. See src/lmdif1.f for what it means.
```

## Warning

Using `NumbaMinpack` is like using C or Fortran: **You will not** be notified if you write or read beyond an array. For example,

```python
@cfunc(minpack_sig)
def myfunc(x, fvec, args):
    fvec[0] = x[0]**2 - args[0]
    fvec[1] = x[1]**2 - args[1]
funcptr = myfunc.address

x_init = np.array([10.0,10.0])
neqs = 2 
args = np.array([30.0]) # Array is too short!!!! 
sol = lmdif(funcptr, x_init, neqs, args) 
```

Notice, that `args`, is only length 1, but in `myfunc` we try to access `args` assuming it as 2 elements. **No error** will be thrown, and you will read from beyond the end of `args`, and the solution will be garbage. If you read far enough beyond then end an array, it will probably crash your program.

