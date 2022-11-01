# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""


"""
Setup.py file

Configure the project, build the package and upload the package to PYPI


python_version setup.py sdist bdist_wheel (to include the source)

[TEST PYPI]
repository = https://test.pypi.org/

[PRODUCTION]
repository = https://upload.pypi.org/legacy/
"""
# twine upload --repository testpypi dist/*

import setuptools
try:
    import Cython
except ImportError:
    raise ImportError("\n<Cython> library is missing on your system."
          "\nTry: \n   C:\\pip install Cython")

try:
    import numpy
except ImportError:
    raise ImportError("\n<numpy> library is missing on your system."
          "\nTry: \n   C:\\pip install numpy")


try:
    import pygame
except ImportError:
    raise ImportError("\n<pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame")


from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import Extension
import platform
import warnings
import sys

print("\n---PYTHON COPYRIGHT---\n")
print(sys.copyright)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ImportWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# NUMPY IS REQUIRED
try:
    import numpy
except ImportError:
    raise ImportError("\n<numpy> library is missing on your system."
                      "\nTry: \n   C:\\pip install numpy on a window command prompt.")


with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# version 1.0.1 Yank, latest version 1.0.2
# pypitest latest version 1.0.17

OPENMP = False
OPENMP_PROC = ""   # "-lgomp"
__VERSION__ = "1.0.8"  # check the file shader.pyx and make sure the version is identical
LANGUAGE = "c"
ext_link_args = ""

py_requires = "HomingMissile requires python3 version 3.6 or above."
py_minor_versions = [x for x in range(6, 11)]

if hasattr(sys, 'version_info'):
    try:
        if not hasattr(sys.version_info, "major") \
                or not hasattr(sys.version_info, "minor"):
            raise AttributeError
        py_major_ver = sys.version_info.major
        py_minor_ver = sys.version_info.minor
    except AttributeError:
        raise SystemExit(py_requires)
else:
    raise SystemExit(py_requires)

if py_major_ver != 3 or py_minor_ver not in py_minor_versions:
    raise SystemExit(
        "HomingMissile support python3 versions 3.6 or above got version %s"
        % str(py_major_ver)+"."+str(py_minor_ver))

if hasattr(platform, "architecture"):
    arch = platform.architecture()
    if isinstance(arch, tuple):
        proc_arch_bits = arch[0].upper()
        proc_arch_type = arch[1].upper()
    else:
        raise AttributeError("Platform library is not install correctly")
else:
    raise AttributeError("Platform library is missing attribute <architecture>")


if hasattr(platform, "machine"):
    machine_type = platform.machine().upper()
else:
    raise AttributeError("Platform library is missing attribute <machine>")

if hasattr(platform, "platform"):
    plat = platform.platform().upper()

else:
    raise AttributeError("Platform library is missing attribute <platform>")

ext_compile_args = []
if plat.startswith("WINDOWS"):
    ext_compile_args = ["/openmp" if OPENMP else "", "/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"]


elif plat.startswith("LINUX"):
    if OPENMP:
        ext_compile_args = \
            ["-DPLATFORM=linux", "-march=i686" if proc_arch_bits == "32BIT" else "-march=x86-64",
             "-m32" if proc_arch_bits == "32BIT" else "-m64", "-O3", "-Wall", OPENMP_PROC, "-static"]
        ext_link_args = [OPENMP_PROC]
    else:
        ext_compile_args = \
            ["-DPLATFORM=linux", "-march=i686" if proc_arch_bits == "32BIT" else "-march=x86-64",
             "-m32" if proc_arch_bits == "32BIT" else "-m64", "-O3", "-Wall", "-static"]
        ext_link_args = ""
else:
    raise ValueError("HomingMissile can be build on Windows and Linux systems only.")

for r in ext_compile_args:
    if r == "":
        ext_compile_args.remove(r)

print("\n---COMPILATION---\n")
print("SYSTEM                : %s " % plat)
print("BUILD                 : %s " % proc_arch_bits)
print("FLAGS                 : %s " % ext_compile_args)
print("EXTRA LINK FLAGS      : %s " % ext_link_args)
print("LANGUAGE              : %s " % LANGUAGE)
print("MULTITPROCESSING      : %s " % OPENMP)
print("MULTITPROCESSING FLAG : %s " % OPENMP_PROC)

print("\n")
print("PYTHON VERSION        : %s.%s " % (sys.version_info.major, sys.version_info.minor))
print("SETUPTOOLS VERSION    : %s " % setuptools.__version__)
print("CYTHON VERSION        : %s " % Cython.__version__)
print("NUMPY VERSION         : %s " % numpy.__version__)
print("PYGAME VERSION        : %s " % pygame.__version__)

try:
    print("SDL VERSION           : %s.%s.%s " % pygame.version.SDL)
except:
    pass  # ignore SDL versioning issue

print("\n*** BUILDING HOMINGMISSILE VERSION ***  : %s \n" % __VERSION__)

# define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
setuptools.setup(
    name="HomingMissile",
    cmdclass={"build_ext": build_ext},
    version= __VERSION__,
    author="Yoann Berenguer",
    author_email="yoyoberenguer@hotmail.com",
    description="Homing Missiles for 2D video game and arcade game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoyoberenguer/HomingMissile",
    # packages=setuptools.find_packages(),
    packages=['HomingMissile'],
    ext_modules=[
        Extension("Weapon", ["Weapon.pyx"],
                  extra_compile_args=ext_compile_args, extra_link_args=ext_link_args,
                  language=LANGUAGE),
        Extension("XML_parsing", ["XML_parsing.pyx"],
                  extra_compile_args=ext_compile_args, extra_link_args=ext_link_args,
                  language=LANGUAGE),
        Extension("SpriteSheet", ["SpriteSheet.pyx"],
                  extra_compile_args=ext_compile_args, extra_link_args=ext_link_args,
                  language=LANGUAGE),
        Extension("Sprites", ["Sprites.pyx"],
                  extra_compile_args=ext_compile_args, extra_link_args=ext_link_args,
                  language=LANGUAGE),
        Extension("SoundServer", ["SoundServer.pyx"],
                  extra_compile_args=ext_compile_args, extra_link_args=ext_link_args,
                  language=LANGUAGE),
        Extension("MissileParticleFX", ["MissileParticleFX.pyx"],
                  extra_compile_args=ext_compile_args, extra_link_args=ext_link_args,
                  language=LANGUAGE),
    ],
    include_dirs=[numpy.get_include(), 'Include']
)
