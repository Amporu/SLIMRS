import pygame
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
class InputHandler:
    car_rotation=0
    car_x=0
    car_y=0
    camera_rotation=0
    camera_zoom=1.0
    selected=0
    old_selected=0
    def check_selected():
        if InputHandler.selected==InputHandler.old_selected:
            return False
        else:
            InputHandler.old_selected=InputHandler.selected
            return True
    def handle_keys():
        """
        Handles keyboard input to control the car's movement and rotation.
        """
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            InputHandler.car_x += 0.1 * math.cos(math.radians(InputHandler.car_rotation))
            InputHandler.car_y += 0.1 * math.sin(math.radians(InputHandler.car_rotation))
        if keys[pygame.K_s]:
            InputHandler.car_x -= 0.1 * math.cos(math.radians(InputHandler.car_rotation))
            InputHandler.car_y -= 0.1 * math.sin(math.radians(InputHandler.car_rotation))
        if keys[pygame.K_a]:
            InputHandler.car_rotation += 1.0
        if keys[pygame.K_d]:
            InputHandler.car_rotation -= 1.0
        if keys[pygame.K_q]:
        
            pygame.quit()
            sys.exit()
        if keys[pygame.K_1]:
            InputHandler.selected=0
            #print(InputHandler.selected)
        if keys[pygame.K_2]:
            InputHandler.selected=1
            #print(InputHandler.selected)
        if keys[pygame.K_3]:
            InputHandler.selected=2
            #print(InputHandler.selected)
            pass
        if keys[pygame.K_4]:
            
            InputHandler.selected=3
            #print(InputHandler.selected)
            pass
        if keys[pygame.K_5]:
            
            selected=4
            #print(InputHandler.selected)
            pass
        if keys[pygame.K_6]:
            
            selected=5
            #print(InputHandler.selected)
            pass
        if keys[pygame.K_7]:
            
            selected=6
            #print(InputHandler.selected)
            pass
        if keys[pygame.K_8]:
            
            selected=7
            #print(InputHandler.selected)
            pass
        if keys[pygame.K_9]:
            
            selected=8
            #print(InputHandler.selected)
            pass
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def handle_mouse(event):
        """
        Handles mouse input to control the camera's rotation and zoom.
        """
        if event.type == pygame.QUIT:
                pygame.quit()
                return
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 4:
                # Scroll up, zoom in
                InputHandler.camera_zoom *= 1.1
            elif event.button == 5:
                # Scroll down, zoom out
                InputHandler.camera_zoom *= 0.9
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                # Left button pressed, rotate
                InputHandler.camera_rotation += event.rel[0] * 0.01