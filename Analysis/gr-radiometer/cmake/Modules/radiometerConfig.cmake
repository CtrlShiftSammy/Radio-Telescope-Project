INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_RADIOMETER radiometer)

FIND_PATH(
    RADIOMETER_INCLUDE_DIRS
    NAMES radiometer/api.h
    HINTS $ENV{RADIOMETER_DIR}/include
        ${PC_RADIOMETER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    RADIOMETER_LIBRARIES
    NAMES gnuradio-radiometer
    HINTS $ENV{RADIOMETER_DIR}/lib
        ${PC_RADIOMETER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/radiometerTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(RADIOMETER DEFAULT_MSG RADIOMETER_LIBRARIES RADIOMETER_INCLUDE_DIRS)
MARK_AS_ADVANCED(RADIOMETER_LIBRARIES RADIOMETER_INCLUDE_DIRS)
