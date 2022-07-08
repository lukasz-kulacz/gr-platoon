find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_PLATOON gnuradio-platoon)

FIND_PATH(
    GR_PLATOON_INCLUDE_DIRS
    NAMES gnuradio/platoon/api.h
    HINTS $ENV{PLATOON_DIR}/include
        ${PC_PLATOON_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_PLATOON_LIBRARIES
    NAMES gnuradio-platoon
    HINTS $ENV{PLATOON_DIR}/lib
        ${PC_PLATOON_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-platoonTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_PLATOON DEFAULT_MSG GR_PLATOON_LIBRARIES GR_PLATOON_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_PLATOON_LIBRARIES GR_PLATOON_INCLUDE_DIRS)
