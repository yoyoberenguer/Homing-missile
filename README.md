# Homing missile

## 2D video game guided missile algorithm

## DEMO
```
Click on the release and install the demo
```

## Python Version
```
Run the program Homingmissile.py with your favorite python IDE 

Requirement: 
pip install numpy==1.19.3 pygame==2.0 opencv-python cython matplotlib

- Numpy
- Python > 3
- OpenCv
- pygame
```

## Keys
```
SPACE BAR : for shooting missiles 
RIGH      : spaceship move to the right
left      : spaceship move to the left
up        : spaceship move up 
down      : spaceship move down
ESC       : to exit 

Mouse position to control targer spaceship 
```

## Cython Version 

Amazing version with many particles and extremely fluid animation.

FOLDER     : Cython Version
SHORT DEMO : Homing-missile/Cython Version/Video.avi

Run the program HomingMissile.py with your favorite python IDE  ** 
** Program must be compiled first (see compilation section)

Cython version include the following features : 

- `MISSILE GUIDANCE`  
    Return the optimized angle a missile needs to follow in order to hit a target quicker. 
    The missile efficiency is limited with the variable max_rotation allowing the missile 
    to turn a certain amount of degrees each frames. 
    This features brings a bit more realism to the missile trajectory.
    
- `PURE PURSUIT ALGORITHM`
    This missile adjust its direction by small incremental steps always aiming toward
    the target position. This missile has a an on-board fuel tank limiting its maximal
    velocity and flying distance. The missile can be shot in any direction from the player position and
    fly outside the display before heading back toward the playable area in order to hit its target.
    The propulsion engine can be trigger at a later stage using the variable propulsion.
    A launch offset can be added to simulate a launch under the aircraft wings.
    If the target is destroyed before the missile collision, the missile will resume its course
    to the latest calculated target vector direction (prior target explosion)    
    
- `LEAD COLLISION` (proportional navigation) more effective, follow an optimal path
    Intercept theorem (Thales basic proportionality theorem)
    https://www.youtube.com/watch?v=T2fPKUfmnKo
    https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm

 - `PURE PURSUIT` with acceleration/deceleration
    Homing missile (guided missile) with automatic gradual acceleration/deceleration.
    this projectile is capable of very sharp angle.
    It can accelerate in straight trajectory and decelerate in the turns to increase manoeuvrability


Requirment :

```
pip install pygame==2.0 nump==1.19.3 opencv-python cython matplotlib

- python > 3.0
- numpy arrays
- pygame with SDL version 1.2 (SDL version 2 untested)
- Cython
- opencv-python
- matplotlib
- A compiler such visual studio, MSVC, CGYWIN setup correctly
  on your system.
  - a C compiler for windows (Visual Studio, MinGW etc) install on your system 
  and linked to your windows environment.
  Note that some adjustment might be needed once a compiler is install on your system, 
  refer to external documentation or tutorial in order to setup this process.
  e.g https://devblogs.microsoft.com/python/unable-to-find-vcvarsall-bat/
```

## Source Compilation :

```
In a command prompt and under the directory containing the source files (Cython Version folder)
C:\>python setup_Project.py build_ext --inplace

If the compilation fail, refers to the requirement section and make sure cython 
and a C-compiler are correctly install on your system. 
```

### Youtube video : 
https://youtu.be/9egTMLZeLjE

### RESOURCES:

https://www.youtube.com/watch?v=T2fPKUfmnKo

https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm

Image1                                           |                     Image2                                 
-------------------------------------------------|---------------------------------------------------
![alt text](https://github.com/yoyoberenguer/Homing-missile-/blob/master/Screendump439.png) | ![alt text](https://github.com/yoyoberenguer/Homing-missile-/blob/master/Screendump456.png) 
![alt text](https://github.com/yoyoberenguer/Homing-missile-/blob/master/Screendump121.png) | ![alt text](https://github.com/yoyoberenguer/Homing-missile-/blob/master/Screendump595.png)
