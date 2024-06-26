import pygame
from pygame.locals import *
import queue

class Utils:
    def get_mouse_event(self):
        # dohvati koordinate misa
        position = pygame.mouse.get_pos()
        
        # povratak lijevog klika i koordinata misa
        return position

    def left_click_event(self):
        # spremi gumbove misa
        mouse_btn = pygame.mouse.get_pressed()
        # napravi zastavicu za lijevi klik misa
        left_click = False

        if mouse_btn[0]: #and e.button == 1:
            # promijena satanja zastavice lijevog klika
            left_click = True

        return left_click