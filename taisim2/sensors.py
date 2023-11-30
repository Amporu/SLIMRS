from taisim2.simulator import Simulator, WINDOW_HEIGHT,WINDOW_WIDTH, CAR_SIZE,draw_ground
from taisim2.simulator import draw_cuboid
from taisim2.input_handler import InputHandler
from taisim2.robot import Robot,Sensors
import cv2
import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Camera:
    def __init__(self,robot,tag,pos_x=0,pos_y=0,pos_z=0.1,frame_width=640,frame_height=480,format="BGR",rotationXY=0,rotationYZ=0,rotationZX=0,fov=45,near_clip=0.1,far_clip=100):
        self.type="CAMERA"
        self.nickname=tag
        self.robot=robot
        self.x=pos_x
        self.y=pos_y
        self.z=pos_z
        self.frame_width=frame_width
        self.frame_height=frame_height
        self.format=format
        self.rotationXY=rotationXY
        self.rotationYZ=rotationYZ
        self.rotationZX=rotationZX
        self.fov=fov
        self.near_clip=near_clip
        self.far_clip=far_clip
        Robot.robot_sensors.append([self.robot.name,self.type,tag,self.robot.robot_type])
        #x y z rx ry rz ,yaw,pitch,roll or whatever, I dont know english that good
        Sensors.items.append([self.x,self.y,self.z,self.robot.count-1,self.rotationXY,rotationYZ,rotationZX])
        
       #print(Robot.robot_sensors)
    
    
    def read(self,depth=False):
        Simulator.render_id=Simulator.render_id+1
        id=Simulator.render_id
        # Create variables for FBO size
        fbo_width = self.frame_width  # Define FBO width
        fbo_height = self.frame_height  # Define FBO height

        # Create and bind a Framebuffer Object (FBO)
        fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        
        # Create a texture for off-screen rendering
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, fbo_width, fbo_height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)
        depth_buffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depth_buffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, fbo_width, fbo_height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buffer)
        glEnable(GL_DEPTH_TEST)

        # Check if FBO is complete
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Framebuffer is not complete!")
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            return None
        gluPerspective(self.fov, fbo_width / fbo_height, self.near_clip, self.far_clip)
        # Set the viewport and render to the FBO
        glViewport(0, 0, fbo_width, fbo_height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Render your scene here using the desired viewport and rendering code

        # Read pixels from the FBO
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        camera_x = Robot.x[self.robot.count-1]+self.x + CAR_SIZE * math.cos(math.radians(Robot.rotation[self.robot.count-1]))
        camera_y = Robot.y[self.robot.count-1]+self.y + CAR_SIZE * math.sin(math.radians(Robot.rotation[self.robot.count-1]))
        camera_look_x = camera_x + math.cos(math.radians(Robot.rotation[self.robot.count-1]))
        camera_look_y = camera_y + math.sin(math.radians(Robot.rotation[self.robot.count-1]))
        gluLookAt(
            camera_x, camera_y,0.1+self.z+Robot.z[self.robot.count-1],  # Camera position (slightly above the car)
            camera_look_x, camera_look_y,0.1+self.z+Robot.z[self.robot.count-1],  # Look-at point (in the car's direction)
            0.0, 0.0, 1.0
        )
        
        
        draw_ground()
        if Robot.count:
            for i in range(Robot.count):
                if i==InputHandler.selected:
        
                    Robot.x[i]=InputHandler.car_x
                    Robot.y[i]=InputHandler.car_y
                
                    Robot.rotation[i]=InputHandler.car_rotation
                
                glPushMatrix()
                
                draw_cuboid(i,0)
                glPopMatrix()
        glDisable(GL_DEPTH_TEST)
        
        if depth==True:
            
            depth_pixels = glReadPixels(0, 0, fbo_width, fbo_height, GL_DEPTH_COMPONENT, GL_FLOAT)
            depth_data = np.frombuffer(depth_pixels, dtype=np.float32).reshape(fbo_height, fbo_width)
        
            depth_data = cv2.flip(depth_data, 0)  # 0 for vertical flip
                    
        pixels = glReadPixels(0, 0, fbo_width, fbo_height, GL_BGR, GL_UNSIGNED_BYTE)

        # Unbind FBO and clean up
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDeleteFramebuffers(1, [fbo])
        glDeleteTextures(1, [texture])
        glBindRenderbuffer(GL_RENDERBUFFER,0)
        glDeleteRenderbuffers(1,[depth_buffer])

        # Process the pixels (if needed) and return the image data
        #print(id)
        image_data = np.frombuffer(pixels, dtype=np.uint8).reshape(fbo_height, fbo_width, 3)
        
        image_data = cv2.flip(image_data, 0)  # 0 for vertical flip
        (w, h), _ = cv2.getTextSize("Robot: "+str(Robot.name[self.robot.count-1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 1)
        cv2.rectangle(img=image_data,pt1=(10,10),pt2=(10+w,20+h//2),color=(int(Robot.b[self.robot.count-1]*255),int(Robot.g[self.robot.count-1]*255),int(Robot.r[self.robot.count-1]*255)),thickness=-1)
        
        cv2.putText(image_data, "Robot: "+str(Robot.name[self.robot.count-1]), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1)
        (w, h), _ = cv2.getTextSize("TAG: "+str(self.nickname), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 1)
        cv2.rectangle(img=image_data,pt1=(10,30),pt2=(10+w,40+h//2),color=(0,255,0),thickness=-1)
        cv2.putText(image_data, "TAG: "+str(self.nickname), (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1)
        #image_data= cv2.rectangle(img=image_data,pt1=(0,0),pt2=(100,400),color=(255,0,0),thickness=-1)
        if self.format=="RGB":
            image_data=cv2.cvtColor(image_data,cv2.COLOR_BGR2RGB)
        if self.format=="GRAY":
            image_data=cv2.cvtColor(image_data,cv2.COLOR_BGR2GRAY)
        if depth==False:
            return image_data
        if depth==True:
            return image_data,depth_data



class GPS:
    def __init__(self,robot,name):
        self.robot=robot
        self.x=robot.x
        self.y=robot.y
        
        self.type="GPS"

        Robot.robot_sensors.append([self.robot.name,self.type,name,self.robot.robot_type])
    def read(self):
        return Robot.x[self.robot.count-1],Robot.y[self.robot.count-1],Robot.z[self.robot.count-1]
class COMPASS:
    def __init__(self,robot,name):
        self.robot=robot
        self.rotation=robot.rotation
        
        self.type="COMPASS"

        Robot.robot_sensors.append([self.robot.name,self.type,name,self.robot.robot_type])
    def read(self):
        return abs(Robot.rotation[self.robot.count-1]%360)
