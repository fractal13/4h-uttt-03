import pygame
from CreepGame import CreepGame

def main():
    pygame.font.init()
    # parameters:
    # title				 : the name of your game
    # width, height      : in cells
    # cell size          : in pixels
    # desired frame rate : in frames per second
    c = CreepGame("Creeps", 60, 40, 10, 30)
    c.main_loop()
    return
    
if __name__ == "__main__":
    main()