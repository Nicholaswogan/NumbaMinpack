# NumbaMinpack

`NumbaMinpack` is a light-weight python wrapper to the Levenberg-Marquardt root-finding algorithm in [Minpack](https://en.wikipedia.org/wiki/MINPACK). It almost identical to `scipy.optimize.root` ([see here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html)), when you set `method = 'lm'`. But, the problem with `scipy.optimize.root`, is that it can not be used within `numba` jit-compiled python code. In contrast, `NumbaMinpack` can be used within a numba compiled function, and it is also much faster than `scipy.optimize.root`, because the python interpreter is never invoked during a non-linear solve. 

Check out `comparison2scipy.ipynb`.

## installation
`NumbaMinpack` will probably only work on MacOS or Linux. You must have `gfortran` installed. On Mac install with `brew install gcc`. You must also have python >3.6.0 with `numpy` and `numba` installed.

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
    args = np.array([30.0,8.0]) # arguments you want to pass to myfunc
    sol = lmdif(funcptr, x_init, neqs, args) # solve
    return sol
    
xsol, fvec, success, info = test()
# xsol = solution
# fvec = function evaluated at solution
# success = True/False
# info = an integer. See src/lmdif1.f for what it means.
```

