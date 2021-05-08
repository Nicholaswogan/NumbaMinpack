
from setuptools import setup
from numpy.distutils.command.build_ext import build_ext

from subprocess import call

sources = ['src/VolcGasesFort.f90',
           'src/minpack/dpmpar.f',
           'src/minpack/enorm.f',
           'src/minpack/fdjac2.f',
           'src/minpack/lmder.f',
           'src/minpack/lmder1.f',
           'src/minpack/lmdif.f',
           'src/minpack/lmpar.f',
           'src/minpack/qrfac.f',
           'src/minpack/qrsolv.f',
           'src/VolcGasesFort_wrapper.f90']
    
cmd = ['gfortran']+sources+'-shared -fPIC -o VolcGases/VolcGasesFort.so -O3'.split()
call(cmd)

setup(name = 'VolcGases',
      packages=['VolcGases'],
      version='2.2',
      include_package_data=True)
