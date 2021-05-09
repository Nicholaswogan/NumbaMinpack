
from setuptools import setup
from subprocess import call

sources = ['src/minpack.f90',
           'src/minpack/dpmpar.f',
           'src/minpack/enorm.f',
           'src/minpack/fdjac2.f',
           'src/minpack/lmdif.f',
           'src/minpack/lmdif1.f',
           'src/minpack/lmpar.f',
           'src/minpack/qrfac.f',
           'src/minpack/qrsolv.f']
           
flags = '-shared -fPIC -o NumbaMinpack/minpack.so -O3'.split()
    
cmd = ['gfortran']+sources+flags
call(cmd)

setup(name = 'NumbaMinpack',
      packages=['NumbaMinpack'],
      version='0.1',
      include_package_data=True)
