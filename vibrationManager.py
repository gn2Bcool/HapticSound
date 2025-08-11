import pygame

pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

if hasattr(joystick, 'rumble'):
    joystick.rumble(0.0,0.0, 25)

joystick.quit()
pygame.joystick.quit()
