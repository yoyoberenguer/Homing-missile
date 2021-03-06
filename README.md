# Homing missile

## 2D video game guided missile algorithm

## New version
```
Install the program using Setup_HomingMissile.exe
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
```
Amazing version with many particles and extremely fluid animation.

FOLDER     : Cython Version
SHORT DEMO : Homing-missile/Cython Version/Video.avi

Run the program HomingMissile.py with your favorite python IDE  ** 
** Program must be compiled first (see compilation section)

Cython version include the following features : 

- MISSILE GUIDANCE
    
    RETURN THE OPTIMIZED ANGLE A MISSILE NEEDS TO FOLLOW IN ORDER TO HIT A TARGET QUICKER.
    THE MISSILE EFFICIENCY IS LIMITED WITH THE VARIABLE max_rotation ALLOWING THE MISSILE 
    TO TURN A CERTAIN AMOUNT OF DEGREES EACH FRAMES. 
    THIS FEATURES BRINGS A BIT MORE REALISM TO THE MISSILE TRAJECTORY.
    
- PURE PURSUIT ALGORITHM

    Guided ballistic missile :
        This missile adjust its direction by small incremental steps always aiming toward
        the target position. This missile has a an on-board fuel tank limiting its maximal
        velocity and flying distance. It can be shot in any direction from the player position and
        fly outside the display before heading back to the playable area in order to hit the target.
        The propulsion engine can be trigger at a later stage using the variable propulsion.
        A launch offset can be added to simulate a launch under the aircraft wings.
        If the target is destroyed before the missile collision, it will resume its course
        to the latest calculated vector direction (prior target explosion)    
    
- LEAD COLLISION (proportional navigation) more effective, follow an optimal path

        Intercept theorem (Thales basic proportionality theorem)
        https://www.youtube.com/watch?v=T2fPKUfmnKo
        https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm

 - PURE PURSUIT ALGORITHM
 
        HOMING MISSILE (GUIDED MISSILE) WITH AUTOMATIC GRADUAL ACCELERATION/DECELERATION.
        THIS PROJECTILE IS CAPABLE OF VERY SHARP ANGLE.
        IT CAN ACCELERATE IN STRAIGHT TRAJECTORY AND DECELERATE IN THE TURNS TO INCREASE MANOEUVRABILITY
```

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
