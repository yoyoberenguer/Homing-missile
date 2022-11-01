# distutils: extra_compile_args = -fopenmp
# distutils: extra_link_args = -fopenmp
# encoding: utf-8


"""
                 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

Copyright Yoann Berenguer
"""


# USE :
# python setup_Project.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
from Cython.Compiler.Main import default_options

ext_modules = [

    Extension("Sprites", ["Sprites.pyx"],
              include_dirs=[numpy.get_include()],
            ),
    Extension("Weapon", ["Weapon.pyx"],
              include_dirs=[numpy.get_include()],
            ),
    Extension("Enemy", ["Enemy.py"],
              include_dirs=[numpy.get_include()],
              ),


    Extension("Var", ["Var.py"],
              include_dirs=[numpy.get_include()]),


    Extension("MissileParticleFx", ["MissileParticleFx.pyx"],
              include_dirs=[numpy.get_include()],
              ),

    Extension("SoundServer", ["SoundServer.pyx"],
              include_dirs=[numpy.get_include()],
             ),

    Extension("Player", ["Player.py"],
              include_dirs=[numpy.get_include()],
              ),

    Extension("XML_parsing", ["XML_parsing.pyx"],
              include_dirs=[numpy.get_include()],
              ),

    Extension("SpriteSheet", ["SpriteSheet.pyx"],
              include_dirs=[numpy.get_include()],
              extra_compile_args=['/openmp'],
              extra_link_args=['/openmp']),

    Extension("Textures", ["Textures.py"],
              include_dirs=[numpy.get_include()],
              ),

]

setup(
    name="HOMING_MISSILE",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    include_dirs=[numpy.get_include()]
)
