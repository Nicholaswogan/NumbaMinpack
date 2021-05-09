gfortran src/minpack.f90 src/dogleg.f src/dpmpar.f src/enorm.f \
src/fdjac1.f src/fdjac2.f src/hybrd.f src/hybrd1.f src/lmdif.f \
src/lmdif1.f src/lmpar.f src/qform.f src/qrfac.f src/qrsolv.f \
src/r1mpyq.f src/r1updt.f -shared -fPIC -o minpack.so -O3
mv minpack.so NumbaMinpack
rm minpack.mod