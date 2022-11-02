# Homing Missile Library 


The project is under the `GNU GENERAL PUBLIC LICENSE Version 3`

---
## Building project from source
1) Download the latest release from here:

   example ==> https://github.com/yoyoberenguer/Homing-missile/releases/tag/v1.0.2 
2) Decompress the archive and enter the project directory 
   ```script
   c:\>cd Homing-missile-1.0.2
   C:\>python setup.py build_ext --inplace --force
   ```
   
## Run the demo 

**Key**                     | Assignement 
----------------------------|-----------------------------------------------------
**ARROW KEYS**              | (LEFT, RIGHT, UP and DOWN) for spaceship direction
**SPACEBAR**                | Fire missiles
**PAUSE/BREAK**             | Pause the demo for 2 secs
**ESC**                     | to quit
**Mouse**                   | Move target

In `Homing-missile-1.0.2`
```script
C:\>cd HomingMissile 
C:\>python homingmissile.py
```

## Preview

![alt text](https://github.com/yoyoberenguer/Homing-missile/blob/master/HomingMissile/Assets/HomingMissile1.PNG)


![alt text](https://github.com/yoyoberenguer/Homing-missile/blob/master/HomingMissile/Assets/HomingMissile2.PNG)

## Missile attributes definition

The XML file `Weapon.xml` contains 4 different missile type:
- STINGER
- BUMBLEBEE
- WASP 
- HORNET

```xml
<?xml version="1.0"?>
<class>
    <category name = "MISSILE">
        <modes>
            <mode name = "GUIDED">
                <weapon name="STINGER"
                        type="Missile"
                        image="STINGER_IMAGE"
                        sprite_orientation="90"
                        sprite_rotozoom ="STINGER_ROTATE_BUFFER"
                        propulsion_sound_fx="STINGER_EXHAUST_SOUND"
                        missile_trail_fx="MISSILE_TRAIL_DICT2"
                        missile_trail_fx_blend = "pygame.BLEND_RGB_ADD"
                        animation='None'
                        range='SCREENRECT.h'
                        bingo_range = '(100, 120)'
                        velocity='-15'
                        damage='1050'
                        timestamp='0'
                        reloading_time='2'
                        detonation_dist='None'
                        max_rotation='10'>
```

The file Weapon.pyx contains all the missile class such as 
- HomingMissile
  ```
  PURE PURSUIT ALGORITHM
  Guided ballistic missile :
  This missile adjust its direction by adding small degrees values (turn radius) until
  reaching the optimal angle difference (0 degrees).
  The missile in on collision course when the angle between the missile heading and the
  target heading difference is approximately null.        
  ```
- InterceptMissile
  ```
  LEAD COLLISION (proportional navigation) more effective, follow an optimal path
  Intercept theorem (Thales basic proportionality theorem)
  https://www.youtube.com/watch?v=T2fPKUfmnKo
  https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm
  ```
- AdaptiveMissile
  ```
  Homing missile (guided missile) with automatic gradual acceleration/deceleration.
  This projectile is capable of very sharp angle.
  It can accelerate in straight trajectory and decelerate in the turns to increase manoeuvrability
  ```
  
## How to shoot a missile in your code 

Check HomingMissile.py to see how to use the missile library.

Below an example with the class `HomingMissile` using the missile STINGER

```python
extra = ExtraAttributes(
   {'target': target,
    'shoot_angle': 90,
    'ignition': False,
    'offset': (30, 0)})

s = HomingMissile(
   gl_=GL,
   group_=(GL.ALL, GL.PLAYER_PROJECTILE),
   weapon_features_=STINGER_FEATURES,
   extra_attributes=extra,
   timing_=800,
)
```
and below for the class `InterceptMissile` using the 
missile BUMBLEBEE

```python
extra = ExtraAttributes(
   {'target': target,
    'shoot_angle': 90,
    'ignition': False,
    'offset': (30, 0)})

s = InterceptMissile(
   gl_=GL,
   group_=(GL.ALL, GL.PLAYER_PROJECTILE),
   weapon_features_=BUMBLEBEE_FEATURES,
   extra_attributes=extra,
   timing_=800,
)
```


## Building Cython & C 

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
*Then compile the code (e.g :)*
```cmdline
C:\...HomingMissile\python setup.py build_ext --inplace
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

