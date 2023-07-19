from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from pygame import image
from pygame.locals import *
import math
import numpy as np

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Ground dimensions
GROUND_SIZE = 10

# Car dimensions
CAR_SIZE = 0.2

# Car position
car_x = 0.0
car_y = 0.0

# Car rotation
car_rotation = 0.0

# Texture variables
texture_id = None

# Camera variables
camera_distance = 10.0
camera_rotation = 0.0
camera_zoom = 1.0

def track():
    """
    Load the image file and create a texture from it.
    """
    global texture_id

    texture_surface = image.load('taisim.png')  # Replace 'ground_texture.jpg' with your own image file
    texture_data = pygame.image.tostring(texture_surface, "RGB", 3)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_surface.get_width(), texture_surface.get_height(),
                 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

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

def draw_car():
    """
    Draws the car using OpenGL.
    """
    glBegin(GL_QUADS)
    glColor3f(1.0, 0, 1.0)  # Magenta color for the car
    glVertex3f(-CAR_SIZE / 2, -CAR_SIZE / 2, 0.1)  # Bottom left
    glVertex3f(CAR_SIZE / 2, -CAR_SIZE / 2, 0.1)  # Bottom right
    glVertex3f(CAR_SIZE / 2, CAR_SIZE / 2, 0.1)  # Top right
    glVertex3f(-CAR_SIZE / 2, CAR_SIZE / 2, 0.1)  # Top left
    glEnd()

def render():
    """
    Renders the scene using OpenGL.
    """
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    gluLookAt(
        camera_distance * math.cos(camera_rotation), -camera_distance * math.sin(camera_rotation), 3.0 * camera_zoom,
        car_x, car_y, 0.0,
        0.0, 0.0, 1.0
    )

    draw_ground()

    glPushMatrix()
    glTranslatef(car_x, car_y, 0.0)
    glRotatef(car_rotation, 0.0, 0.0, 1.0)  # Rotate around z-axis (upward direction)
    draw_car()

    # Virtual camera on the car
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.5)  # Offset the camera from the car
    glColor3f(1.0, 1.0, 1.0)  # White color for the camera
    glBegin(GL_QUADS)
    glColor4f(0,1,1,0.3)
    glVertex3f(0.0, 0.0, 0.0)  # Camera position
    glVertex3f(0.0, 1.0, 0.0)  # Camera look direction
    glVertex3f(0.0, 1.0, 0.5)  # Camera look direction
    glVertex3f(0.0, 0.0, 0.5)  # Camera look direction
    glEnd()
    glPopMatrix()
    glPopMatrix()
    
    glFlush()
    pygame.display.flip()

def handle_keys():
    """
    Handles keyboard input to control the car's movement and rotation.
    """
    global car_x, car_y, car_rotation

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        car_x += 0.1 * math.cos(math.radians(car_rotation))
        car_y += 0.1 * math.sin(math.radians(car_rotation))
    if keys[pygame.K_s]:
        car_x -= 0.1 * math.cos(math.radians(car_rotation))
        car_y -= 0.1 * math.sin(math.radians(car_rotation))
    if keys[pygame.K_a]:
        car_rotation += 1.0
    if keys[pygame.K_d]:
        car_rotation -= 1.0
    if keys[pygame.K_q]:
        pygame.quit()
        return

def handle_mouse(event):
    """
    Handles mouse input to control the camera's rotation and zoom.
    """
    global camera_rotation, camera_zoom

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            # Scroll up, zoom in
            camera_zoom *= 1.1
        elif event.button == 5:
            # Scroll down, zoom out
            camera_zoom *= 0.9
    elif event.type == pygame.MOUSEMOTION:
        if event.buttons[0] == 1:
            # Left button pressed, rotate
            camera_rotation += event.rel[0] * 0.01

def main():
    """
    The main function that sets up the window, handles events, and runs the simulation loop.
    """
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.toggle_fullscreen()
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)

    clock = pygame.time.Clock()
    track()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                handle_mouse(event)

        handle_keys()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        render()

        clock.tick(60)

if __name__ == '__main__':
    main()
