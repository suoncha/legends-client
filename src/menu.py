import sys
from pygame import *
from game import *
from sound import *
from player import *
from config import *

class MenuManager:
    # Initialize startup
    def __init__(self):
        # Create game screen
        self.screen = pygame.display.set_mode()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Legends")
        self.x, self.y = self.screen.get_size()
        # Create sound
        self.sound = SoundManager()
        # Define buttons
        self.buttonTitle = pygame.image.load(IMAGES + "menu/title.png")
        self.buttonTitle = pygame.transform.scale(self.buttonTitle, (int(self.x*0.5), int(self.y*0.5)))
        self.buttonCredit = pygame.image.load(IMAGES + "menu/credit.png")
        self.buttonCredit = pygame.transform.scale(self.buttonCredit, (int(self.x*0.1), int(self.y*0.1)))
        self.buttonName = pygame.image.load(IMAGES + "menu/name.png")
        self.buttonName = pygame.transform.scale(self.buttonName, (int(self.x*0.2), int(self.y*0.2)))
        self.buttonPlay = pygame.image.load(IMAGES + "menu/start.png")
        self.buttonPlay = pygame.transform.scale(self.buttonPlay, (int(self.x*0.1), int(self.y*0.1)))
        self.buttonSound = pygame.image.load(IMAGES + "menu/sound.png")
        self.buttonSound = pygame.transform.scale(self.buttonSound, (int(self.y*0.1), int(self.y*0.1)))

    # Mouse click check 
    def click(self, mouse, pos, w, h):
        xMouse = mouse[0]
        yMouse = mouse[1]
        xPos = pos[0]
        yPos = pos[1]
        if (xMouse > xPos) and (xMouse < xPos + w) and (yMouse > yPos) and (yMouse < yPos + h):
            return True
        else:
            return False
    
    # Print menu
    def default(self):
        self.screen.blit(self.buttonPlay, (self.x*0.45,self.y*0.5))
        self.screen.blit(self.buttonCredit, (self.x*0.45,self.y*0.65))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.click(mouse.get_pos(), [self.x*0.45,self.y*0.53], self.x*0.1, self.y*0.05):
                    self.view = 2
                if self.click(mouse.get_pos(), [self.x*0.45,self.y*0.68], self.x*0.1, self.y*0.04):
                    self.view = 1
                if self.click(mouse.get_pos(), [self.x*0.9,self.y*0.83], self.y*0.1, self.y*0.1):
                    self.sound.playTheme()
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                self.view = -1
        pygame.display.update()
    
    # Print credit
    def credit(self):
        self.screen.blit(self.buttonName, (self.x*0.4,self.y*0.5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                self.view = 0
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.click(mouse.get_pos(), [self.x*0.85,self.y*0.83], self.x*0.1, self.y*0.1):
                    self.sound.playTheme()
        pygame.display.update()

    # Menu loop
    def run(self):
        # Initialize variables
        self.run = True
        self.view = 0
        self.game = GameManager()

        while self.run:
            self.screen.fill('white')
            self.screen.blit(self.buttonTitle, (self.x*0.25,0))    
            self.screen.blit(self.buttonSound, (self.x*0.9,self.y*0.85))  
            if self.view == -1: 
                pygame.quit() 
                sys.exit()
            if self.view == 0: self.default()
            if self.view == 1: self.credit()
            if self.view == 2: 
                self.run = False
                self.start()
            pygame.display.update()

    # Main loop
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('white')
            self.game.run()
            self.clock.tick(FPS)
            pygame.display.update()