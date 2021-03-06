from uttt_data import *
from pygame_game import PygameGame
import pygame, pygame.locals
import uttt_data

class UTTTGame(PygameGame):

    def __init__(self, width_px, height_px, frames_per_second, data, send_queue):
        # PygameGame sets self.width and self.height        
        PygameGame.__init__(self, "Ultimate Tic Tac Toe", width_px, height_px, frames_per_second)
        pygame.font.init()
        self.data = data
        self.send_queue = send_queue
        self.image = pygame.image.load("Space.jpg")
        self.player1 = pygame.image.load("alieng.png")
        self.player2 = pygame.image.load("alienp.png")
        self.image1 = pygame.image.load("blackhole2.png")
        self.font = pygame.font.Font("Starjedi.ttf", 14)

        pygame.mixer.init()
        self.game_music = pygame.mixer.music.load("starwars.mp3")

        pygame.mixer.music.play(-1, 0.0)
        
        return
   
    def handle_state(self):
        if self.data:
            state = self.data.GetState()
            if state in [ uttt_data.STATE_SHOW_SIGNUP, uttt_data.STATE_WAIT_SIGNUP, 
                          uttt_data.STATE_SIGNUP_FAIL_USERNAME,
                          uttt_data.STATE_SHOW_LOGIN, uttt_data.STATE_WAIT_LOGIN, uttt_data.STATE_LOGIN_FAIL,
                          uttt_data.STATE_SIGNUP_FAIL_EMAIL, uttt_data.STATE_SIGNUP_FAIL_PASSWORD,
                          uttt_data.STATE_SIGNUP_FAIL_PASSWORD_UNMATCHED, uttt_data.STATE_SIGNUP_OK ]:
                # minimize window
                #pygame.display.iconify()
                if self.screen.get_size() != ( 1, 1 ):
                    print "shrink"
                    self.screen = pygame.display.set_mode(
                        # set the size
                        (1, 1),
                        # use double-buffering for smooth animation
                        pygame.DOUBLEBUF |
                        # apply alpha blending
                        pygame.SRCALPHA |
                        # allow resizing
                        pygame.RESIZABLE)
                
            elif state in [ uttt_data.STATE_WAIT_GAME, uttt_data.STATE_SHOW_GAME,
                            uttt_data.STATE_GAME_OVER, uttt_data.STATE_TURN_FAILED,
                            uttt_data.STATE_WAIT_TURN ]:
                # unminimize window
                if self.screen.get_size() != ( self.width, self.height ):
                    print "WHAT?  pygame doesn't support unminimize?"
                    self.screen = pygame.display.set_mode(
                        # set the size
                        (self.width, self.height),
                        # use double-buffering for smooth animation
                        pygame.DOUBLEBUF |
                        # apply alpha blending
                        pygame.SRCALPHA |
                        # allow resizing
                        pygame.RESIZABLE)
            elif state in [ uttt_data.STATE_SOCKET_CLOSED, uttt_data.STATE_SOCKET_ERROR,
                            uttt_data.STATE_ERROR ]:
                # close
                print "Socket closed, or other error, pygame will quit."
                #pygame.quit()
            elif state in [ uttt_data.STATE_SOCKET_OPEN ]:
                # what should I do?
                pass
            else:
                print "Unknown state in pygame: ", state

        return

    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position):
        self.handle_state()
        
        if 1 in newbuttons:
            if self.data.GetNextPlayer() != self.data.GetPlayer():
                # not our turn
                return

            mX,mY = mouse_position[0], mouse_position[1]
            col = mX / (self.width/9)
            row = mY / (self.height/9)
            board = 3 * (row / 3) + (col / 3)
            position = 3 * (row % 3) + (col % 3)
            
            if self.data and self.send_queue:
                text = self.data.SendTurn(board, position)
                print "pygame: queuing: %s" % (text, )
                self.send_queue.put(text)
        return

    def paint(self, surface):
        # Background
        rect = pygame.Rect(0,0,self.width,self.height)
        surface.blit(self.image,(0,0))

        opponent = "you are playing: " + self.data.GetOpponentName()
        self.drawTextLeft(surface, opponent, (255, 255, 255), 25, 35, self.font)

        currentTurn = "it  is  " + self.data.GetNextPlayer() + "' s  turn"
        self.drawTextLeft(surface, currentTurn, (255, 255, 255), 25, 55, self.font)
        print currentTurn
        you = "you are " + self.data.GetPlayer() + "s"
        self.drawTextLeft(surface, you, (255, 255, 255), 25, 75, self.font)      
        print you

        for board in range(9):
            if self.data.GetNextBoard() == board:
                color = (0,0,0)
                x = (board % 3)*self.width/3
                y = (board / 3)*self.height/3
                w = self.width/3
                h = self.height/3
                rect= pygame.Rect(x,y,w,h)
                pygame.draw.rect(surface,color,rect)
    
                if board == 0:
                    surface.blit(self.image1,(0,0))
                elif board == 1:
                    surface.blit(self.image1,(200,0))
                elif board == 2:
                    surface.blit(self.image1,(400,0))
                elif board == 3:
                    surface.blit(self.image1,(0,200))
                elif board == 4:
                    surface.blit(self.image1,(200,200))
                elif board == 5:
                    surface.blit(self.image1,(400,200))
                elif board == 6:
                    surface.blit(self.image1,(0,400))
                elif board == 7:
                    surface.blit(self.image1,(200,400))
                elif board == 8:
                    surface.blit(self.image1,(400,400))
                        
                    

        
        
        
        
        
        # Regular Lines
        for i in range(1,9):
            pygame.draw.line(surface, (255,255,255), (0, i*self.height/9), (self.width, i*self.height/9))
        for j in range(1,9):
            pygame.draw.line(surface, (255,255,255), (j*self.width/9, 0), (j*self.height/9, self.height))

        # Board Lines
        for k in range(1,3):
            pygame.draw.line(surface, (255,255,0), (0, k*self.height/3), (self.width, k*self.height/3), 3)
        for l in range(1,3):
            pygame.draw.line(surface, (255,255,0), (l*self.width/3, 0), (l*self.height/3, self.height), 3)

        # Markers
        for board in range(9):
            for position in range(9):
                col = 3 * (board % 3) + position % 3
                row = 3 * (board / 3) + position / 3
                x = int((col + .5) * self.width / 9)
                y = int((row + .5) * self.height / 9)
                marker = self.data.GetMarker(board, position)
                if marker == uttt_data.PLAYER_X:
                    #pygame.draw.circle(surface, (0,0,255), (x, y), 5)
                    surface.blit(self.player1, (x-18, y-23))
                elif marker == uttt_data.PLAYER_O:
                    #pygame.draw.circle(surface, (0,0,255), (x, y), 5)
                    surface.blit(self.player2, (x-18, y-23))

        opponent = "You are playing: " + self.data.GetOpponentName()
        self.drawTextLeft(surface, opponent, (255, 255, 255), 25, 35, self.font)

        currentTurn = "I t  is  " + self.data.GetNextPlayer() + "' s  turn"
        self.drawTextLeft(surface, currentTurn, (255, 255, 255), 25, 55, self.font)

        you = "You are " + self.data.GetPlayer() + "s"
        self.drawTextLeft(surface, you, (255, 255, 255), 25, 75, self.font) 
        return

    def drawTextLeft(self, surface, text, color, x, y, font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomleft = (x, y)
        surface.blit(textobj, textrect)
        return
   

def uttt_pygame_main(data, send_queue):
    game = UTTTGame(600, 600, 30, data, send_queue)
    game.main_loop()
    return

if __name__ == "__main__":
    data = UTTTData()
    data.SetState(uttt_data.STATE_SHOW_GAME)
    uttt_pygame_main(data, None)

