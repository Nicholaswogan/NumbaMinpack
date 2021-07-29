# NumbaMinpack

`NumbaMinpack` is a python wrapper to [Minpack](https://en.wikipedia.org/wiki/MINPACK), which is for solving systems of non-linear equations.

This package is very similar to `scipy.optimize.root` ([see here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html)), when you set `method = 'lm'` or `method = 'hybr'`. But, the problem with `scipy.optimize.root`, is that it can not be used within numba jit-compiled python functions. In contrast, `NumbaMinpack` can be used within a numba compiled function. For example, check out `comparison2scipy.ipynb`.

Right now, `NumbaMinpack` wraps the following Minpack algorithms 
- `lmdif` (Levenberg-Marquardt) with a finite-differenced, non-analytical, jacobian.
- `hybrd` (modified Powell method) with a finite-differenced, non-analytical, jacobian. 

## Installation
`NumbaMinpack` will probably only work on MacOS or Linux. You must have a fortran compiler (On Mac install with `brew install gcc`).

After satisfying the dependencies, install with the pip command below

```
python -m pip install git+git://github.com/Nicholaswogan/NumbaMinpack.git
```

## Basic usage

```python
from NumbaMinpack import lmdif, hybrd, minpack_sig
from numba import njit, cfunc
import numpy as np

# System of equations must look like this. Returns nothing!
@cfunc(minpack_sig)
def myfunc(x, fvec, args):
    fvec[0] = x[0]**2 - args[0]
    fvec[1] = x[1]**2 - args[1]
    
funcptr = myfunc.address # address in memory to myfunc

x_init = np.array([10.0,10.0]) # initial conditions
neqs = 2 # number of equations
args = np.array([30.0,8.0]) # data you want to pass to myfunc
xsol, fvec, success, info = lmdif(funcptr, x_init, neqs, args) # solve with lmdif
xsol, fvec, success, info = hybrd(funcptr, x_init, args) # OR solve with hybrd
# xsol = solution
# fvec = function evaluated at solution
# success = True/False
# info = an integer. See src/lmdif1.f for what it means.
```

Note, that either `lmdif` or `hybrd` can be called within a jit-compiled numba function:
```python
@njit
def test()
  return hybrd(funcptr, x_init, args)
sol = test() # this works!!! :)

@njit
def test_sp():
    sol_sp = scipy.optimize.root(myfunc_scipy,x_init,method='hybr')
    return sol_sp
sol_sp = test_sp() # this DOES NOT WORK :(
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

