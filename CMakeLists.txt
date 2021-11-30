cmake_minimum_required(VERSION 3.4.0)
project(NumbaMinpack LANGUAGES Fortran)

option(SKBUILD "Should be ON of being build by skbuild, 
and OFF of being build by regular cmake" OFF)

if (NOT CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE)
endif()

add_library(minpack SHARED 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/minpack.f90 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/dogleg.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/dpmpar.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/enorm.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/fdjac1.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/fdjac2.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/hybrd.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/hybrd1.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/lmdif.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/lmdif1.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/lmpar.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/qform.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/qrfac.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/qrsolv.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/r1mpyq.f 
            ${CMAKE_CURRENT_SOURCE_DIR}/src/r1updt.f)
            
set_target_properties(minpack PROPERTIES PREFIX "lib")

if (SKBUILD)
  install(TARGETS minpack DESTINATION NumbaMinpack)
else()
  install(TARGETS minpack DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/NumbaMinpack/)
endif()