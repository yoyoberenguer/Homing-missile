# Homing Missile Library 


*New Version 1.0.8


```
pip install PygameShader==1.0.8
```


The project is under the `GNU GENERAL PUBLIC LICENSE Version 3`

---
## Demo

In the PygameShader `Demo` directory 

(press ESC to quit the demo)

```bash
C:\>python demo_fire.py
C:\>python demo_transition.py
C:\>python demo_wave.py
```
*if cupy and CUDA are installed correctly on your system you can run the GPU shaders*
```bash
C:\>python gpu_chromatic.py
C:\>python gpu_zoom.py
C:\>python gpu_wave.py

```
---

## Installation from pip
Check the link for newest version https://pypi.org/project/PygameShader/

* Available python build 3.6, 3.7, 3.8, 3.9, 3.10 and source build
* Compatible WINDOWS and LINUX for platform x86, x86_64
```
pip install PygameShader 
```

* Checking the installed version 
  (*Imported module is case sensitive*) 
```python
>>>from PygameShader.shader import __VERSION__
>>>__VERSION__
```
---
## Installation from source code

*Download the source code and decompress the Tar or zip file*
* Linux
```bash
tar -xvf source-1.0.8.tar.gz
cd PygameShader-1.0.8
python3 setup.py bdist_wheel
cd dist 
pip3 install PygameShader-xxxxxx 
```
* Windows 

*Decompress the archive and enter PygameShader directory* 
```bash
python setup.py bdist_wheel 
cd dist
pip install PygameShader-xxxxxx
```

---

## Building Cython & C code 

#### When do you need to compile the cython code ? 

Each time you are modifying any of the pyx files such as 
shader.pyx, shader.pxd, __init__.pxd or any external C code if applicable

1) open a terminal window
2) Go in the main project directory where (shader.pyx & 
   shader.pxd files are located)
3) run : `C:\>python setup_shader.py build_ext --inplace --force`

If you have to compile the code with a specific python 
version, make sure to reference the right python version 
in (`python38 setup_shader.py build_ext --inplace`)

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

*Edit the file setup_shader.py and check the variable OPENMP.*
*You can enable or disable multi-processing*
```python
# Build the cython code with mutli-processing (OPENMP) 
OPENMP = True
```
*Save the change and build the cython code with the following instruction:*
```bash
C:\PygameShader\PygameShader\python setup_shader.py build_ext --inplace --force
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
- A C compiler for windows (Visual Studio, MinGW etc)
---
## OPENMP for Linux and Windows

The pip packages (including LINUX architectures i686 and x86_64), are build by default with multiprocessing for 
the CPU's shader. If you need to build the package without multiprocessing, you can change the flag OPENMP  
in the setup.py file such as :

To build the package without multiprocessing (OPENMP=False)


*in the setup.py file*
```bash
# True enable the multiprocessing
OPENMP = False
OPENMP_PROC = "-fopenmp" 
__VERSION__ = "1.0.8" 
LANGUAGE = "c++"
ext_link_args = ""


```
*Then compile the code (e.g : Version 1.0.8, 64-bit python3.7)*
```cmdline
C:\PygameShader\python setup.py bdist_wheel 
cd dist
pip install PygameShader-1.0.8-cp37-cp37m-win_amd64.whl
```

*The same variable `OPENMP` exist also in the setup_config.py file when building the Cython code*

* Building PygameShader package will automatically check and compile the source code, you do not 
need to build manually the Cython code.
---

## Credit
Yoann Berenguer 

## Dependencies :
```
numpy >= 1.18
pygame >=2.0.0
cython >=0.29.21
*Cupy   
```
(*) Used for GPU shader (not compulsory during installation). In order to use the GPU shaders 
you would need to have a NVIDIA graphic card, CUDA and CUPY install sucessfully on your platform. 

## License :

GNU GENERAL PUBLIC LICENSE Version 3

Copyright (c) 2019 Yoann Berenguer

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.


## Testing: 
```python
>>> import PygameShader
>>> from PygameShader.tests.test_shader import run_testsuite
>>> run_testsuite()
```
