module minpack
  use iso_c_binding, only: c_double, c_int, c_funptr, c_f_procpointer
  implicit none
  private
  public lmdif1_wrapper, hybrd1_wrapper
  
  abstract interface
    subroutine numba_callback(x, fvec, args)
      use iso_c_binding, only: c_double
      implicit none
      real(c_double), intent(in) :: x(*)
      real(c_double), intent(out) :: fvec(*)
      real(c_double), intent(in) :: args(*)
    end subroutine
  end interface

contains

  subroutine lmdif1_wrapper(cfcn, m, n, x, fvec, tol, maxfev, info, &
                            wa, lwa, args, k) bind(c)
    type(c_funptr), intent(in), value :: cfcn
    integer(c_int), intent(in) :: m, n
    real(c_double), intent(inout) :: x(n)
    real(c_double), intent(out) :: fvec(m)
    real(c_double), intent(in) :: tol
    integer(c_int), intent(in) :: maxfev
    integer(c_int), intent(out) :: info
    integer(c_int), allocatable :: iwa(:)
    integer(c_int), intent(in) :: lwa
    real(c_double), intent(in) :: wa(lwa)
    real(c_double), intent(in), target :: args(k)
    integer(c_int), intent(in) :: k
    
    procedure(numba_callback), pointer :: nb_callback_f
    
    allocate(iwa(n))
    
    call c_f_procpointer(cfcn,nb_callback_f)
    ! I adjusted lmdif1.f to also include maxfev as an argument
    call lmdif1(fcn_lmdif,m,n,x,fvec,tol,maxfev,info,iwa,wa,lwa)
    
    deallocate(iwa)
    
  contains
    
    subroutine fcn_lmdif(m, n, x, fvec, iflag)
      integer(c_int), intent(in) :: m, n
      real(c_double), intent(in) :: x(n)
      real(c_double), intent(out) :: fvec(m)
      integer(c_int), intent(inout) :: iflag
      
      call nb_callback_f(x, fvec, args)
      
    end subroutine
    
  end subroutine

  subroutine hybrd1_wrapper(cfcn, n, x, fvec, tol, maxfev, info, wa, &
                            lwa, args, k) bind(c)
    type(c_funptr), intent(in), value :: cfcn
    integer(c_int), intent(in) :: n
    real(c_double), intent(inout) :: x(n)
    real(c_double), intent(out) :: fvec(n)
    real(c_double), intent(in) :: tol
    integer(c_int), intent(in) :: maxfev
    integer(c_int), intent(out) :: info
    integer(c_int), intent(in) :: lwa
    real(c_double), intent(in) :: wa(lwa)
    real(c_double), intent(in), target :: args(k)
    integer(c_int), intent(in) :: k
    
    procedure(numba_callback), pointer :: nb_callback_f
    
    call c_f_procpointer(cfcn,nb_callback_f)
    ! I adjusted hybrd1.f to also include maxfev as an argument
    call hybrd1(fcn_hybrd,n,x,fvec,tol,maxfev,info,wa,lwa)
    
  contains
    
    subroutine fcn_hybrd(n,x,fvec,iflag)
      integer(c_int), intent(in) :: n
      real(c_double), intent(in) :: x(n)
      real(c_double), intent(out) :: fvec(n)
      integer(c_int), intent(inout) :: iflag
    
      call nb_callback_f(x, fvec, args)
      
    end subroutine
    
  end subroutine
  
end module