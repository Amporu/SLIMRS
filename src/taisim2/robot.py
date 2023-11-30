from OpenGL.GL import *
from OpenGL.GLUT import *
from taisim2.input_handler import InputHandler
import numpy as np
import math
import random
class Sensors:
    items=[]
class Robot:
    x=[]
    y=[]
    z=[]
    rotation=[]
    name=[]
    size=[]
    count=0
    robot_sensors=[]
    r=[]
    g=[]
    b=[]
    
    
    type=[]
    def __init__(self,tag,x=0,y=0,z=0,size=0.3,rotation=0):
        

        Robot.r.append(random.random())
        Robot.g.append(random.random())
        Robot.b.append(random.random())
        self.robot_id=Robot.count
        
        Robot.count=Robot.count+1
        Robot.type.append("robot")
        Robot.name.append(tag)
        Robot.x.append(x)
        Robot.y.append(y)
        Robot.z.append(z)
        Robot.size.append(size)
        Robot.rotation.append(rotation)
        self.x=x
        self.y=y
        self.z=z
        self.name=tag
        self.robot_type="robot"
        self.count=Robot.count
        self.rotation=rotation
        
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(Robot.rotation[self.count-1], 0.0, 0.0, 1.0)  # Rotate around z-axis (upward direction)
        glBegin(GL_QUADS)
        glColor3f(1.0, 0, 1.0)  # Magenta color for the car
        glVertex3f(-Robot.size[self.count-1], -Robot.size[self.count-1], 0.1)  # Bottom left
        glVertex3f(Robot.size[self.count-1], -Robot.size[self.count-1], 0.1)  # Bottom right
        glVertex3f(Robot.size[self.count-1], Robot.size[self.count-1], 0.1)  # Top right
        glVertex3f(-Robot.size[self.count-1], Robot.size[self.count-1], 0.1)  # Top left
        
        glEnd()
    
       
        
        """
        Draws the car using OpenGL.
        """
        
        glPopMatrix()
        Robot.draw_text(self.name,self.x,self.y,1,0.001)
    def move(self,linear_velocity=0,angular_velocity=0,altitude=0):
        Robot.rotation[self.count-1]+=angular_velocity
        Robot.x[self.count-1]+=linear_velocity*math.cos(math.radians(Robot.rotation[self.count-1]))
        Robot.y[self.count-1]+= linear_velocity * math.sin(math.radians(Robot.rotation[self.count-1]))
        Robot.z[self.count-1]=altitude
        pass
    def draw_text(text, x, y, z, size, rect_color=(0.0, 0.0, 1.0,0.5)):
        # Calculate the dimensions of the text in pixels (you may need to adjust this)
        text_width_pixels = len(text) * 0.1
        text_height_pixels = 1

        # Calculate the vertices for the rectangle
        rect_left = 0
        rect_right = len(text) * 0.5*(InputHandler.camera_zoom)
        rect_bottom = -text_height_pixels /8
        rect_top = text_height_pixels /2*InputHandler.camera_zoom
        camera_distance=10
        # Calculate the direction vector from camera to (0, 0, 1)
        camera_position = np.array([float(x), float(y), float(z)])
        target_position = np.array([camera_distance * math.cos(InputHandler.camera_rotation), -camera_distance * math.sin(InputHandler.camera_rotation), 3*InputHandler.camera_zoom])
        direction = target_position - camera_position
        direction /= np.linalg.norm(direction)

        # Calculate the rotation matrix to align text and background with the camera
        up_vector = np.array([0.0, 0.0, 1.0])
        right_vector = np.cross(up_vector, direction)
        up_vector = np.cross(direction, right_vector)
        rotation_matrix = np.column_stack((right_vector, up_vector, direction, [0.0, 0.0, 0.0]))
        rotation_matrix = np.vstack((rotation_matrix, [0.0, 0.0, 0.0, 1.0]))

        glPushMatrix()
        glTranslatef(x, y, z)

        # Apply the rotation matrix to face the camera
        glMultMatrixf(rotation_matrix.T)

        # Draw the rectangle as the background
        glColor4f(*rect_color)
        glBegin(GL_QUADS)
        glVertex3f(rect_left, rect_bottom,-1)
        glVertex3f(5*rect_right//6, rect_bottom,-1)
        glVertex3f(5*rect_right//6, rect_top,-1)
        glVertex3f(rect_left, rect_top,-1)
        glEnd()

        # Scale the background and text
        glScalef(size*InputHandler.camera_zoom*4, size*InputHandler.camera_zoom*4, size*InputHandler.camera_zoom*4)

        # Use the shader program
        glColor3f(1.0, 1.0, 1.0)  # Set the text color (white in this example)
        for char in text:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))

        glPopMatrix()
