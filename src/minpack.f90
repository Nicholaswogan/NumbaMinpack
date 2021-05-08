module minpack
  use iso_c_binding, only: c_double, c_int, c_funptr, c_f_procpointer
  implicit none
  
  procedure(numba_callback1), pointer :: nb_callback_f
  
  integer(c_int) :: mod_k
  real(c_double), allocatable :: mod_args(:)
  
  abstract interface
    subroutine numba_callback1(x, fvec, args)
      use iso_c_binding, only: c_double
      implicit none
      real(c_double), intent(in) :: x(*)
      real(c_double), intent(out) :: fvec(*)
      real(c_double), intent(in) :: args(*)
    end subroutine
  end interface

contains

  subroutine lmdif1_wrapper(cfcn, m, n, x, fvec, tol, info, iwa, wa, lwa, args, k) bind(c)
    type(c_funptr), intent(in), value :: cfcn
    integer(c_int), intent(in) :: m, n
    real(c_double), intent(inout) :: x(n)
    real(c_double), intent(out) :: fvec(m)
    real(c_double), intent(in) :: tol
    integer(c_int), intent(out) :: info
    integer(c_int), intent(in) :: iwa(n)
    integer(c_int), intent(in) :: lwa
    real(c_double), intent(in) :: wa(lwa)
    real(c_double), intent(in) :: args(k)
    integer(c_int), intent(in) :: k
    
    mod_k = k
    allocate(mod_args(k))
    mod_args = args
    
    call c_f_procpointer(cfcn,nb_callback_f)
    call lmdif1(fcn,m,n,x,fvec,tol,info,iwa,wa,lwa)
    
    deallocate(mod_args)
    
  end subroutine
  
  subroutine fcn(m, n, x, fvec, iflag)
    implicit none
    integer(c_int), intent(in) :: m, n
    real(c_double), intent(in) :: x(n)
    real(c_double), intent(out) :: fvec(m)
    integer(c_int), intent(inout) :: iflag
    
    call nb_callback_f(x, fvec, mod_args)

  end subroutine
  
  
  
end module