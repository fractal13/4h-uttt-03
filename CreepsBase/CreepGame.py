import pygame
import game_mouse
from CreepData import CreepData

class CreepGame(game_mouse.Game):
    def __init__(self, title, width, height, cell_size, frame_rate):
        self.newGame(title, width, height, cell_size, frame_rate)
        return

    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position):
        self.data.evolve(keys, newkeys, buttons, newbuttons, mouse_position)
        return
        
    def paint(self, surface):
        self.data.draw(surface)
        return

    def newGame(self, title, width, height, cell_size, frame_rate):
        game_mouse.Game.__init__(self, title, width*cell_size, height*cell_size, frame_rate)
        self.data = CreepData(width, height, cell_size, frame_rate)
        return
