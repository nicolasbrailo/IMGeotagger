__all__ = ["cefpython", "wx"]
__version__ = "31.2"
__author__ = "The CEF Python authors"

import ctypes, os

# If this is a debian package then package_dir returns:
#   /usr/lib/pymodules/python2.7/cefpython3
# The above path consists of symbolic links to the real directory:
#   /usr/share/pyshared/cefpython3

# If package was installed using PIP or setup.py then package
# dir is here:
#   /usr/local/lib/python2.7/dist-packages/cefpython3/

package_dir = os.path.dirname(os.path.abspath(__file__))

# This loads the libcef.so library for the subprocess executable.
os.environ["LD_LIBRARY_PATH"] = package_dir

# This env variable will be returned by cefpython.GetModuleDirectory().
os.environ["CEFPYTHON3_PATH"] = package_dir

# This loads the libcef.so library for the main python executable.
# The libffmpegsumo.so library does not need to be loaded here,
# it may cause issues to load it here in the browser process.
libcef_so = os.path.join(package_dir, "libcef.so")
ctypes.CDLL(libcef_so, ctypes.RTLD_GLOBAL)

import sys
if 0x02070000 <=  sys.hexversion < 0x03000000:
    from . import cefpython_py27 as cefpython
else:
    raise Exception("Unsupported python version: " + sys.version)
