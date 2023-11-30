import pygame
from taisim2.input_handler import InputHandler
from pygame import image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from taisim2.logging_system import logger
import cv2
import numpy as np
import math
from taisim2.robot import Robot,Sensors
from taisim2.utils import rgb_to_ansi_escape, rgb_to_ansi_background,LEVEL1,LEVEL2,LEVEL3,LEVEL4,LEVEL5,LEVEL6,LEVEL7
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
# Texture variables
texture_id = None
# Camera variables
camera_distance = 10.0
# Ground dimensions
GROUND_SIZE = 10
# Car dimensions
CAR_SIZE = 0.2

class Simulator:
    render_id=0
    init=False
    pygame.init()
    logger.info("SIMULATOR : \033[92mSTART\033[0m")
    screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.OPENGL)#|HIDDEN)
    pygame.display.set_caption("Window 1")
    screen.fill((255,0,0))
    #pygame.event.set_grab(True)
    #slider = HorizontalSlider(screen,window_width=WINDOW_WIDTH,window_height=WINDOW_HEIGHT,slider_width=250,slider_height=20,slider_x=200,slider_y=500,slider_color=(100, 100, 100),
    #handle_color=(255, 0, 0),text_color=(0, 0, 0),max_positions=9,slider_value=0.5)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)
    clock = pygame.time.Clock()
    
    def isRunning():
        
        
        if not Simulator.init:
            print(Sensors.items)
            arch_color=rgb_to_ansi_background(0.8,0.8,0)
            print(f"<{arch_color}SIMUALATION ARCHITECTURE\033[0m>")
            Simulator.init=True
            if len(Robot.name):
                for j in range(len(Robot.name)):
                    
                    sensor_color=rgb_to_ansi_background(0.0,0.3,1)
                    color=rgb_to_ansi_background(Robot.r[j],Robot.g[j],Robot.b[j])
                    print(f"        \033[33m|")
                    print(f"        \033[33m|")
                    print(f"        \033[33m\u251C---\u252C\033[0m<{color}{Robot.name[j]}\033[0m> ")
                    
                    for i in range(len(Robot.robot_sensors)):
                        if Robot.name[j]==Robot.robot_sensors[i][0]:
                            
                                print("\033[33m        |   |")
                                print(f"\033[33m        |   \u251C--------\033[0m<{sensor_color}%s\033[0m> \033[92m%s\033[0m"%(Robot.robot_sensors[i][1],Robot.robot_sensors[i][2]))
                                
                color=rgb_to_ansi_background(Robot.r[InputHandler.selected],Robot.g[InputHandler.selected],Robot.b[InputHandler.selected])
                print(f"\033[0m<{color}{Robot.name[InputHandler.selected]}\033[0m> SELECtED for Remote Controll")
        for event in pygame.event.get():
            InputHandler.handle_mouse(event)     
            #button.handle_event(event)
        #Simulator.slider.draw_slider()
        InputHandler.handle_keys()
        Simulator.render_id=0  
        Simulator.clock.tick(60)
        return True
    def track(path):
        """
        Load the image file and create a texture from it.
        """
        global texture_id
        
        texture_surface = image.load(path)  # Replace 'ground_texture.jpg' with your own image file
        logger.info("TRACK SET : \033[92m%s\033[0m",path)
        texture_data = pygame.image.tostring(texture_surface, "RGB", 3)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_surface.get_width(), texture_surface.get_height(),
                    0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    def render():
        """
        Renders the scene using OpenGL.
        """
        
        

        glViewport(0, 0, WINDOW_WIDTH , WINDOW_HEIGHT)  # Left half of the screen
        glScissor(0, 0, WINDOW_WIDTH , WINDOW_HEIGHT)  # Set scissor rectangle
        glEnable(GL_SCISSOR_TEST)  # Enable scissor test
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if(InputHandler.check_selected()):
            InputHandler.car_x=Robot.x[InputHandler.selected]
            InputHandler.car_y=Robot.y[InputHandler.selected]
            InputHandler.car_rotation=Robot.rotation[InputHandler.selected]
            color=rgb_to_ansi_background(Robot.r[InputHandler.selected],Robot.g[InputHandler.selected],Robot.b[InputHandler.selected])
            print(f"\033[0m<{color}{Robot.name[InputHandler.selected]}\033[0m> SELECTED for remote control")
        gluLookAt(
            camera_distance * math.cos(InputHandler.camera_rotation), -camera_distance * math.sin(InputHandler.camera_rotation), 3.0 * InputHandler.camera_zoom,
            InputHandler.car_x, InputHandler.car_y, 0.0,
            0.0, 0.0, 1.0
        )
        draw_ground()
        
        #robot=Robot(name="hello",robot_type="drone",x=InputHandler.car_x,y=InputHandler.car_y,size=0.2,rotation=InputHandler.car_rotation)
        if Robot.count:
            for i in range(Robot.count):
                
                
                if i==InputHandler.selected:
                    Robot.x[i]=InputHandler.car_x
                    Robot.y[i]=InputHandler.car_y
                
                    Robot.rotation[i]=InputHandler.car_rotation
                glPushMatrix()
                draw_cuboid(i,1)
                glPopMatrix()
                Robot.draw_text(Robot.name[i],Robot.x[i],Robot.y[i],1,0.001,rect_color=(Robot.r[i],Robot.g[i],Robot.b[i],0.5))
            for i in range(len(Sensors.items)):
                glPushMatrix()
                draw_camera(Sensors.items[i][0],Sensors.items[i][1],Sensors.items[i][2],Sensors.items[i][3],Sensors.items[i][4],Sensors.items[i][5],Sensors.items[i][6])
                glPopMatrix()
        
    
        
        
        pixels = glReadPixels(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE)
        #glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color to black
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable(GL_SCISSOR_TEST)  # Disable scissor test after rendering
        image_data = np.frombuffer(pixels, dtype=np.uint8).reshape(WINDOW_HEIGHT, WINDOW_WIDTH, 3)
        image_data = cv2.flip(image_data, 0)  # Flip the image due to OpenGL's coordinate system
        
        glFlush()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        
        #pygame.display.flip()
        return image_data


def draw_camera(x,y,z,i,xy,yz,zx):
    cuboid_vertices = [
    [-0.03, -0.03, 0.02],    # Bottom left near
    [0.03, -0.03, 0.02],     # Bottom right near
    [0.03, 0.03, 0.02],      # Top right near
    [-0.03, 0.03, 0.02],     # Top left near
    [-0.03, -0.03, 0.05],  # Bottom left far
    [0.03, -0.03, 0.05],   # Bottom right far
    [0.03, 0.03, 0.05],    # Top right far
    [-0.03, 0.03, 0.05]    # Top left far
]
    pyramid_vertices = [
        
    [0.0, 0.0, 0.1],   # Apex of the pyramid
    [0.2, 0.2, 0.5],
    [-0.2, 0.2, 0.5],
    [-0.2, -0.2, 0.5],  # Base vertices
    
    
    [0.2, -0.2, 0.5]
]

# Define the cuboid faces
    cuboid_faces = [
    [0, 1, 2, 3],  # Bottom face
    [4, 5, 6, 7],  # Top face
    [0, 4, 5, 1],  # Near face
    [1, 5, 6, 2],  # Right face
    [2, 6, 7, 3],  # Far face
    [3, 7, 4, 0]   # Left face
]
    glTranslatef(+x+Robot.x[i], +y+Robot.y[i], +z+Robot.z[i])
    glRotatef(Robot.rotation[i]+xy, 0.0, 0.0, 1.0)  # Rotate around z-axis (upward direction)
    glRotatef(yz, 1.0, 0.0, 0.0)
    glRotatef(zx,0,1,0)
    glRotatef(90, 0.0, 1.0, 0.0)  # Rotate around z-axis (upward direction)
    glBegin(GL_QUADS)
    
    glColor3f(1, 1, 1)  # Magenta color for the car
    for face in cuboid_faces:
        
        for vertex_id in face:
            glVertex3fv(cuboid_vertices[vertex_id])
    glEnd()
   
    glColor3f(0.0, 0.0, 0.0)  # Set color to black
   
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Set polygon mode to draw lines
    glLineWidth(4.0)  # Set line width if desired

    for face in cuboid_faces:
        glBegin(GL_LINE_LOOP)
        for vertex_id in face:
            glVertex3fv(cuboid_vertices[vertex_id])
        glEnd()
    glBegin(GL_QUADS)
    colors=[[1.0, 1.0, 1.0],[1,0,0],[0,1,0],[0,0,1],[1,1,0]]  # Set color to black
    for surface in [
        [1, 2, 3, 4],  # Base
        [0, 1, 2],     # Triangle 1
        [0, 2, 3],     # Triangle 2
        [0, 3, 4],     # Triangle 3
        [0, 4, 1]      # Triangle 4
    ]:
        for i,vertex in enumerate(surface):
            glColor3f(colors[i][0],colors[i][1],colors[i][2]) 
            glVertex3fv(pyramid_vertices[vertex])
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Reset to fill mode
    
    glColor3f(Robot.r[i], Robot.b[i], Robot.g[i])  # Reset to original color
def draw_ground():
    """
    Draws the ground with the applied texture.
    """
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-GROUND_SIZE / 2, -GROUND_SIZE / 2, 0.0)  # Bottom left
    glTexCoord2f(1.0, 0.0)
    glVertex3f(GROUND_SIZE / 2, -GROUND_SIZE / 2, 0.0)  # Bottom right
    glTexCoord2f(1.0, 1.0)
    glVertex3f(GROUND_SIZE / 2, GROUND_SIZE / 2, 0.0)  # Top right
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-GROUND_SIZE / 2, GROUND_SIZE / 2, 0.0)  # Top left
    glEnd()
    glDisable(GL_TEXTURE_2D)


def draw_cuboid(i,ok):
    cuboid_vertices = [
    [-Robot.size[i], -Robot.size[i]/2, 0.02],    # Bottom left near
    [Robot.size[i], -Robot.size[i]/2, 0.02],     # Bottom right near
    [Robot.size[i], Robot.size[i]/2, 0.02],      # Top right near
    [-Robot.size[i], Robot.size[i]/2, 0.02],     # Top left near
    [-Robot.size[i], -Robot.size[i]/2, 0.05],  # Bottom left far
    [Robot.size[i], -Robot.size[i]/2, 0.05],   # Bottom right far
    [Robot.size[i], Robot.size[i]/2, 0.05],    # Top right far
    [-Robot.size[i], Robot.size[i]/2, 0.05]    # Top left far
]

# Define the cuboid faces
    cuboid_faces = [
    [0, 1, 2, 3],  # Bottom face
    [4, 5, 6, 7],  # Top face
    [0, 4, 5, 1],  # Near face
    [1, 5, 6, 2],  # Right face
    [2, 6, 7, 3],  # Far face
    [3, 7, 4, 0]   # Left face
]
    glTranslatef(Robot.x[i], Robot.y[i], Robot.z[i])
    glRotatef(Robot.rotation[i], 0.0, 0.0, 1.0)  # Rotate around z-axis (upward direction)
    glBegin(GL_QUADS)
    
    glColor3f(Robot.r[i], Robot.g[i], Robot.b[i])  # Magenta color for the car
    for face in cuboid_faces:
        
        for vertex_id in face:
            glVertex3fv(cuboid_vertices[vertex_id])
    glEnd()
    mean =(Robot.r[i]+Robot.b[i]+Robot.g[i])/3
    if (mean)>=0.3:
        glColor3f(0.0, 0.0, 0.0)  # Set color to black
    else:
        glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Set polygon mode to draw lines
    glLineWidth(4.0)  # Set line width if desired

    for face in cuboid_faces:
        glBegin(GL_LINE_LOOP)
        for vertex_id in face:
            glVertex3fv(cuboid_vertices[vertex_id])
        glEnd()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Reset to fill mode
    if ok==1:
        glColor3f(Robot.r[i], Robot.g[i], Robot.b[i])  # Reset to original color
    else:
        glColor3f(Robot.r[i], Robot.b[i], Robot.g[i])  # Reset to original color

