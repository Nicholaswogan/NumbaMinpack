
from setuptools import setup
from subprocess import call

sources = ['src/minpack.f90',
           'src/dpmpar.f',
           'src/enorm.f',
           'src/fdjac2.f',
           'src/lmdif.f',
           'src/lmdif1.f',
           'src/lmpar.f',
           'src/qrfac.f',
           'src/qrsolv.f']
           
flags = '-shared -fPIC -o NumbaMinpack/minpack.so -O3'.split()
    
cmd = ['gfortran']+sources+flags
call(cmd)
call('rm minpack.mod'.split())

setup(name = 'NumbaMinpack',
      packages=['NumbaMinpack'],
      version='0.1',
      include_package_data=True)
