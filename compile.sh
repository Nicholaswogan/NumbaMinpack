gfortran src/minpack.f90 src/dpmpar.f src/enorm.f src/fdjac2.f src/lmdif.f \
src/lmdif1.f src/lmpar.f src/qrfac.f src/qrsolv.f -shared -fPIC -o minpack.so -O3
mv minpack.so NumbaMinpack
rm minpack.mod