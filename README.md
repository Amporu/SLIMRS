<p align="center">
<a href="https://www.linkedin.com/in/adrian-ionu%C8%9B-%C8%9Bucudean-37aa59244">
    <img src="https://img.shields.io/badge/-LinkedIn-blue">
</a>
<a href="https://www.reddit.com/r/TAISIM/">
    <img src="https://img.shields.io/badge/-Reddit-red">
</a>
<a href="mailto:Tucudean.Adrian.Ionut@outlook.com">
    <img src="https://img.shields.io/badge/-Email-darkgreen?style=flat-square&logo=#0078D4&logoColor=black">
</a>

<a href="[https://pypi.org/user/TucuAI/](https://static.pepy.tech/personalized-badge/taisim?period=total&units=abbreviation&left_color=black&right_color=orange&left_text=Downloads)">
    <img src="https://img.shields.io/badge/PyPi-TucuAI-blueviolet">
</a>

<br/> 



</p>

![base_logo_transparent_background](/src/taisim2/data/logo.jpg)

TAISIM is a Python-based simulator designed for testing and developing computer vision applications. With a primary focus on autonomous driving systems that rely on virtual sensor inputs, it provides a versatile platform for a variety of tasks, from lane keeping to complex navigation in agricultural environments.

## Latest Release

<p align="center">

[![Downloads](https://static.pepy.tech/badge/taisim2)](https://pepy.tech/project/taisim2)
<a href="https://github.com/Amporu/Taisim/releases">
    <img src="https://img.shields.io/badge/-0.1.0-important">
 
<br/> 
    
</p>
    
## Dependencies
  * OpenCV
  * Pygame
  * PyOpenGL
  * NumPy
## Key Features


[![Linux](https://img.shields.io/badge/linux-black?style=for-the-badge&logo=Linux)](https://github.com/Amporu)
    
[![Windows](https://img.shields.io/badge/Windows-black?style=for-the-badge&logo=Windows)](https://github.com/Amporu)
    
[![MacOS](https://img.shields.io/badge/MacOS-black?style=for-the-badge&logo=MacOS)](https://github.com/Amporu)

# Installation:
To install via pip use:
```sh
pip install taisim2 #Python2.x
pip3 install taisim2 #Python3.x
```
# Basic Usage Single-Robot example
Robot Initialization
```pyhton
example_robot=Robot(tag="helloOpenCV")
```
## Sensor Atachment
```pyhon
example_camera=Camera(robot=example_robot,tag="car camera",pos_x=0,pos_y=1)

example_gps=GPS(robot=example_robot,tag="t1 GPS")

example_compass=COMPASS(example_robot,"my compass")
```
## Sensor read
```python
#inside a loop

frame=example_camera.read() $only color
frame,depth_frame=example_camera.read(depth=True) color and depth frame
x,y,z=example_gps.read()# localization
angle=example.compass.read()# orientation
```
## Robot movement
```python
example_robot.move(linear_velocity=0.1,angular_velocity0.1,altitude0.1)
```
# Lets jump to the Multi-Robot&Sensor part
The usage of the package is very easy and it was designed so if you know OpenCV, you are comfortable working with TAISIM2.

Every robot has a tag, initial position, initial rotation and size.
```python

example_robot=Robot(tag="helloOpenCV",x=0,y=-10,z=0,size=0.3,rotation=0)

tank1=Robot(tag="Tornado",size=0.2)

car=Robot(tag="LineFollower",x=-5,size=0.2)

drone=Robot(tag="EAGLE BOT",x=3)
```
## Sensor Initialization
Every sensor is position is relative to its robot position.
```python3
#each sensor is customisable and gets atached to a robot
#initialize camera
camera1=Camera(tank1,tag="birdy",)
camera2=Camera(example_robot,tag="FPV",frame_width=600,frame_height=600)
camera3=Camera(car,tag="car camera",pos_x=0,pos_y=1)

#initialize gps
gps=GPS(tank1,tag="t1 GPS")
gps1=GPS(drone,tag="drone GPS")
gps2=GPS(example_robot,tag="GPS")

#initialize compass
compass1=COMPASS(drone,tag="compass")
compass1=COMPASS(tank1,tag="imu")
Simulation Architecture
```
Based on the initialization the simulator would generate at the beginning of the program a simulation architecture.

The architecture hierarchy will be displayed in the terminal (for our example it will look like this):

This architecture will display all robots with all sensors and their tags in order to distinguish them properly

## Render the Simulator Enviournment
```python3
while Simulator.isRunning():
      Simulator.render()
```
It will create a window that will display our track , robots and tags.

## EXAMPLE CODE
For the example above this is how the code looks like:
```python
from taisim2.simulator import Simulator,Robot,InputHandler
from taisim2.virtual_sensors import Camera,GPS,COMPASS
import cv2
  
def main():
    
    #initialize robots
    example_robot=Robot(tag="helloOpenCV",x=0,y=-10,z=0,size=0.3,rotation=0)    
    tank1=Robot(tag="Tornado",size=0.2)
    car=Robot(tag="LineFollower",x=-5,size=0.2)
    drone=Robot(tag="EAGLE BOT",x=3)

    #initialize cameras
    camera1=Camera(tank1,tag="birdy",)
    camera2=Camera(example_robot,tag="FPV",frame_width=600,frame_height=600)
    camera3=Camera(car,tag="car camera",pos_x=0,pos_y=1)
    
    #initialize gps
    gps=GPS(tank1,"t1 GPS")
    gps1=GPS(drone,"drone GPS")
    gps2=GPS(example_robot,"GPS")

    #initialize compass
    compass1=COMPASS(drone,"compass")
    compass1=COMPASS(tank1,"imu")
    
    #Set the track
    Simulator.track('taisim2/logo.png')

    while Simulator.isRunning():  #check if the simulator is still running
        world=Simulator.render()   # Render
        example_robot.move(1,1,0)   
if __name__ == '__main__':
    main()
#-----------------------------------------------------------------------------
```
# Simulator Examples
TAISIM2 is suitable for a range of computer vision applications, including but not limited to:

Lane Keeping: Test and develop algorithms for keeping a vehicle within the boundaries of a lane.
Line Following: Test and develop the simplest algorithm for following a line.
Maze Running: Develop and evaluate navigation algorithms capable of finding a path through complex environments.
Agricultural Crop Following: Ideal for tasks like crop identification, health monitoring, or autonomous navigation between crop rows.
Future Development Plans
the Python version of the simulator will serve as a POC soo what I want to do Is migrate the code to C , build it as a shared library (.dll , .so) and making it available to C,C++,Python, Java Users
