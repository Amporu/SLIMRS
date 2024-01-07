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

## Architecture

![base_logo_transparent_background](/src/taisim2/data/classes_s84mxYm3jT.png)
![base_logo_transparent_background](/src/taisim2/data/packages_rIfYiGojz3.png)

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
ATENTION!!!
when depth=True 
```python frame,depth_frame=example_camera.read(depth=True)```
we get both the color and the depth frame 
![base_logo_transparent_background](/src/taisim2/data/image_JNsoaNVNyE.png.webp)
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
![base_logo_transparent_background](/src/taisim2/data/image_ZcpQdgVtWc.png.webp)

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
from taisim2.simulator import Simulator,Robot,LEVEL1
from taisim2.sensors import Camera,GPS,COMPASS
import cv2
# Window dimensions
def main():
    
    #initialize robots
    example_robot=Robot(tag="helloOpenCV",x=0,y=-10,z=-0,size=0.3,rotation=0)    
    little_tank=Robot(tag="TANK",y=5)
    drone=Robot(tag="drone", z=5,x=0.2)
    #initialize cameras
    
    camera1=Camera(robot=example_robot, tag="Example Camera",near_clip=0.1,far_clip=100)
    camera2=Camera(robot=little_tank, tag="Left Camera",pos_x=0,pos_y=0,pos_z=0.1,rotationXY=90,fov=60,frame_width=640,frame_height=480)
    drone_camera=Camera(robot=drone,tag="BirdEyeView",pos_z=-0.2,rotationZX=90,far_clip=300)
    gps=GPS(robot=example_robot,tag="example_gps")
    compass=COMPASS(robot=example_robot, tag="example COMPASS")
   
    #Set the track
    #Simulator.track(LEVEL1)
    Simulator.track("logo.jpg")

    while Simulator.isRunning():  #check if the simulator is still running
        Simulator.render()   # Render
        frame=camera1.read() #if we don't have depth=True , we return only the color frame
        drone_frame=drone_camera.read()
        color_frame, depth_frame =camera2.read(depth=True) #with depth=True we return the color and depth frame
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame, alpha=255), cv2.COLORMAP_JET)

        x,y,z =gps.read()
        angle =compass.read()

        drone.move(linear_velocity=0,angular_velocity=-0.5,altitude=5)

        cv2.imshow("frontal_camera",frame)
        cv2.imshow("left_frame",color_frame)
        cv2.imshow("depth_frame",depth_colormap)
        cv2.imshow("drone_view",drone_frame)
          
if __name__ == '__main__':
    main()

#-----------------------------------------------------------------------------
```
![base_logo_transparent_background](/src/taisim2/data/image_Zmw3mXVfZp.png.webp)

# Simulator Examples
TAISIM2 is suitable for a range of computer vision applications, including but not limited to:

Lane Keeping: Test and develop algorithms for keeping a vehicle within the boundaries of a lane.
Line Following: Test and develop the simplest algorithm for following a line.
Maze Running: Develop and evaluate navigation algorithms capable of finding a path through complex environments.
Agricultural Crop Following: Ideal for tasks like crop identification, health monitoring, or autonomous navigation between crop rows.
Future Development Plans
the Python version of the simulator will serve as a POC soo what I want to do Is migrate the code to C , build it as a shared library (.dll , .so) and making it available to C,C++,Python, Java Users
