
from setuptools import setup
from subprocess import call

sources = ['src/minpack.f90',
           'src/dogleg.f',
           'src/dpmpar.f',
           'src/enorm.f',
           'src/fdjac1.f',
           'src/fdjac2.f',
           'src/hybrd.f',
           'src/hybrd1.f',
           'src/lmdif.f',
           'src/lmdif1.f',
           'src/lmpar.f',
           'src/qform.f',
           'src/qrfac.f',
           'src/qrsolv.f',
           'src/r1mpyq.f',
           'src/r1updt.f']
           
flags = '-shared -fPIC -o NumbaMinpack/minpack.so -O3'.split()
    
cmd = ['gfortran']+sources+flags
err = call(cmd)
if err:
    raise Exception('Failed to compile Fortran. Make sure you have gfortran installed correctly.')
call('rm minpack.mod'.split())

setup(name = 'NumbaMinpack',
      packages=['NumbaMinpack'],
      version='0.1',
      include_package_data=True)
