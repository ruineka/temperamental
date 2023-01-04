#!/bin/python3

import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Temperamental TDP Control')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800,600))

# gamepad init

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name() + " connected!")


# Gui Elements

manager = pygame_gui.UIManager((800,600))

button1 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,50,100,100),
                            text='5w TDP',
                            manager=manager
                        )

button2 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,150,100,100),
                            text='10w TDP',
                            manager=manager
                        )

button3 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,250,100,100),
                            text='15w TDP',
                            manager=manager
                        )

button4 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,350,100,100),
                            text='25w TDP',
                            manager=manager
                        )

button5 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,450,175,30),
                            text='Restore Defaults',
                            manager=manager
                        )

label1 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(0,-25,200,100),
                            text="Set TDP Value",
                            manager=manager
)


isRunning = True
clock = pygame.time.Clock()

while isRunning:

    time_delta = clock.tick(60)/1000.0
    window_surface.blit(background,(0,0))
    window_surface.fill((25,20,100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
        if event.type == pygame.JOYBUTTONUP:
            print(event)
    
        manager.process_events(event)
    
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    pygame.display.update()     

