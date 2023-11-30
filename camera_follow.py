

from taisim2.simulator import Simulator,Robot,InputHandler
from taisim2.virtual_Sensors import Camera,GPS,COMPASS

import cv2
# Window dimensions

def main():
    #initialize robots
    example_robot=Robot(tag="helloOpenCV",x=0,y=-10,z=0,size=0.3,rotation=0)
    tank1=Robot(tag="Tornado",size=0.2)
    car=Robot(tag="LineFollower",x=-5,size=0.2)
    drone=Robot(tag="EAGLE BOT",x=3)

    #initialize cameras
    camera1=Camera(tank1,tag="birdy",rotationXY=90)
    camera4=Camera(tank1,tag="birdy",rotationXY=-90)
    camera5=Camera(tank1,tag="halo",rotationXY=0)
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
    Simulator.track('taisim2/taisim.png')
    
    
    while Simulator.isRunning():#check if the simulator is still running
        world=Simulator.render()# Render 
        frame,depth_data=camera5.read(depth=True)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_data, alpha=255), cv2.COLORMAP_JET)
        #print(depth_data)
        cv2.imshow("frame",frame)
        cv2.imshow("depth",depth_colormap)

if __name__ == '__main__':
    main()
