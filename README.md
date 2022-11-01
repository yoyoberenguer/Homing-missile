# Homing Missile Library 


The project is under the `GNU GENERAL PUBLIC LICENSE Version 3`

---

## Building Cython & C code 

#### When do you need to compile the cython code ? 

The first time compilation and each time you are modifying any 
of the pyx files such as Sprites.pyx, Sprites.pxd, *.pyx and *.pxd __init__.pxd 
or any external C code if applicable

1) open a terminal window
2) Go in the main project directory `HomingMissile` where (setup.py & requirements.txt
   are located)
3) run : `C:\>python setup.py build_ext --inplace --force`

If you have to compile the code with a specific python 
version, make sure to reference the right python version 
in (`python38 setup.py build_ext --inplace`)

If the compilation fail, refers to the requirement section and 
make sure Cython and a C-compiler are correctly install on your
 system.
- A compiler such visual studio, MSVC, CGYWIN setup correctly on 
  your system.
  - a C compiler for windows (Visual Studio, MinGW etc) install 
  on your system and linked to your Windows environment.
  Note that some adjustment might be needed once a compiler is 
  install on your system, refer to external documentation or 
  tutorial in order to setup this process.e.g :
    
https://devblogs.microsoft.com/python/unable-to-find-vcvarsall-bat/

*Edit the file setup.py and check the variable OPENMP.*
*You can enable or disable multi-processing*
```python
# Build the cython code with mutli-processing (OPENMP) 
OPENMP = True
```
*Save the change and build the cython code with the following instruction:*
```bash
C:\...HomingMissile\python setup.py build_ext --inplace --force
````
*If the project build successfully, the compilation will end up with the following lines*
```
Generating code
Finished generating code
```
If you have any compilation error(s) refer to the section ```Building cython code```, make sure 
your system has the following program & libraries installed. Check also that the code is not 
running in a different thread.  
- Pygame version >3
- numpy >= 1.18
- cython >=0.29.21 (C extension for python) 
- PygameShader>=1.0.8 
- A C compiler for windows (Visual Studio, MinGW etc)
---
## OPENMP for Linux and Windows

If you need to build the package with multiprocessing, you can change the flag OPENMP  
in the setup.py file such as :

To build the package with multiprocessing (OPENMP=True)

*in the setup.py file*
```bash
# True enable the multiprocessing
OPENMP = True
OPENMP_PROC = "-fopenmp" 
LANGUAGE = "c"
ext_link_args = ""


```
*Then compile the code (e.g : Version 1.0.0, 64-bit python3.7)*
```cmdline
C:\...HomingMissile\python setup.py bdist_wheel 
cd dist
pip install HomingMissile-1.0.0-xxxx-win_amd64.whl
```

---

## Credit
Yoann Berenguer 

## Dependencies :
```
numpy >= 1.18
pygame >=2.0.0
cython >=0.29.21
PygameShader>=1.0.8
   
```


## License :

GNU GENERAL PUBLIC LICENSE Version 3

Copyright (c) 2019 Yoann Berenguer

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

