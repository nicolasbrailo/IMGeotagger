try:
    # The setuptools package is not installed by default 
    # on a clean Ubuntu. Might be also a case on Windows.
    # Python Eggs and Wheels can be created only with setuptools.
    from setuptools import setup
    from setuptools.command.install import install as _install
    from setuptools.dist import Distribution
    print("[setup.py] Using setuptools")
except:
    from distutils.core import setup
    from distutils.command.install import install as _install
    from distutils.dist import Distribution
    print("[setup.py] Using distutils")

import sys
import os
import subprocess

def post_install():
    """ Post install tasks """
    print("[setup.py] post_install()")
    
    # Check if libudev.so.0 exists and if not, create
    # a symbolic link to libudev.so.1. See issues 145 
    # and 105 in the CEFPython Issue Tracker.
    # -- Sequence of these dirs does matter, on first
    # -- match searching should be stopped.
    libdirs = ["/lib/x86_64-linux-gnu", "/usr/lib64", 
               "/lib/i386-linux-gnu", "/usr/lib"]
    for libdir in libdirs:
        if os.path.exists(libdir+"/libudev.so.1") \
                and not os.path.exists(libdir+"/libudev.so.0"):
            libudev1 = "%s/libudev.so.1" % libdir
            libudev0 = "%s/libudev.so.0" % libdir
            print("[setup.py] ln -sf %s %s" % (libudev1, libudev0))
            subprocess.call("ln -sf %s %s" % (libudev1, libudev0), shell=True)
            break
    
    # Find package directory. 
    # Do not import from local cefpython3/ directory.
    del sys.path[0]
    sys.path.append('')
    import cefpython3
    package_dir = os.path.dirname(cefpython3.__file__)
        
    # Make sure this is not a local package imported
    print("[setup.py] package_dir = %s" % package_dir)
    assert not package_dir.startswith(
            os.path.dirname(os.path.abspath(__file__)))
    
    # Execute permissions for subprocess.exe and cefclient.exe
    subprocess_exe = os.path.join(package_dir, "subprocess")
    cefclient_exe = os.path.join(package_dir, "cefclient")
    print("[setup.py] chmod +x " + subprocess_exe)
    subprocess.call("chmod +x "+subprocess_exe, shell=True)
    print("[setup.py] chmod +x " + cefclient_exe)
    subprocess.call("chmod +x "+cefclient_exe, shell=True)

    # Write permissions for debug.log files
    commands = [
        "chmod 666 %s/debug.log" % package_dir,
        "chmod 666 %s/examples/debug.log" % package_dir,
        "chmod 666 %s/examples/wx/debug.log" % package_dir,
    ]
    for command in commands:
        print("[setup.py] %s" % command)
        subprocess.call(command, shell=True)

class install(_install):
    def run(self):
        _install.run(self)
        post_install()
        
class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

setup(
    distclass=BinaryDistribution,
    cmdclass={'install': install},
    name='cefpython3', # No spaces here, so that it works with deb packages.
    version='31.2',
    description='Python bindings for the Chromium Embedded Framework',
    license='BSD 3-Clause',
    author='Czarek Tomczak',
    author_email='czarek.tomczak@gmail.com',
    url='http://code.google.com/p/cefpython/',
    platforms=['linux-x86_64'],
    packages=['cefpython3', 'cefpython3.wx'],
    package_data={'cefpython3': [
        'examples/*.py',
        'examples/*.html',
        'examples/*.js',
        'examples/*.css',
        'examples/kivy-select-boxes/*.html',
        'examples/kivy-select-boxes/*.js',
        'examples/kivy-select-boxes/*.css',
        'examples/kivy-select-boxes/*.md',
        'examples/wx/*.py',
        'examples/wx/*.html',
        'examples/wx/*.png',
        'locales/*.pak',
        'wx/*.txt',
        'wx/images/*.png',
        '*.txt',
        'cefclient',
        'subprocess',
        '*.so',
        '*.pak',
        'debug.log',
        'examples/debug.log',
        'examples/wx/debug.log',
    ]}
)
