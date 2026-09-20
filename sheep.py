import pygame
import random

class Sheep:
    white = pygame.transform.scale2x(pygame.image.load('white.png')) 
    black = pygame.transform.scale2x(pygame.image.load('black.png'))
    scrawny = pygame.transform.scale2x(pygame.image.load('scrawny.png'))
    pink = pygame.transform.scale2x(pygame.image.load('pink.png'))
    me = pygame.transform.scale2x(pygame.image.load('me.png'))
    tung = pygame.transform.scale2x(pygame.image.load('tung.png'))

    def __init__(self, pos, surface, color):
        self._pos = pos
        self.surface = surface
        self._color = color
        self._hitbox = pygame.Rect((self._pos[0], self._pos[1], 25, 25))
        pygame.draw.rect(self.surface, [255,0,0], self._hitbox)

    def assignColor(self):
        r = random.randint(1, 3770)
        if (r < 1886):
            self._color = 'white'
        elif (r < 2619):
            self._color = 'black'
        elif (r < 3200):
            self._color = 'scrawny' # THESE ODDS SUCK. MAKE THEM NOT SUCK
        elif (r < 3768):    
            self._color = 'pink'
        elif (r == 3769):
            self._color = 'me'
        else:
            self._color = 'tung'

    def move(self):
        rand = random.randint(1,4)
        stride = random.randint(15, 60)
        if (rand == 1):
            for i in range(stride):
                self._pos[0] += 1
        elif (rand == 2):
            for i in range(stride):
                self._pos[0] -= 1
        elif (rand == 3):
            for i in range(stride):
                self._pos[1] += 1
        elif (rand == 4):
            for i in range(stride):
                self._pos[1] -= 1
        self._hitbox.topleft = self._pos

    @property
    def position(self):
        return self._pos

    @property
    def hitbox(self):
        return self._hitbox
    @property 
    def color(self):
        return self._color

    def draw(self):
        #pygame.draw.rect(self.surface, [255, 0, 0], (self._pos[0], self._pos[1], 25, 25))
        self.surface.blit(getattr(self, self._color), (self._pos[0] - 10, self._pos[1] - 10))

    

        



class suicidalSheep(Sheep):
    def __init__(self, pos, surface, color):
        super().__init__(pos, surface, color)

    def move(self, playerPos):
        try:
            dx = (playerPos[0] - self._pos[0]) / abs(playerPos[0] - self._pos[0])
        except(ZeroDivisionError):
            dx = 0
        try:
            dy = (playerPos[1] - self._pos[1]) / abs(playerPos[1] - self._pos[1])
        except(ZeroDivisionError):
            dy = 0
        self._pos[0] += 2 * dx
        self._pos[1] += 2 * dy
        self._hitbox.topleft = self._pos

class resistantSheep(Sheep):
    def __init__(self, pos, surface):
        super().__init__(pos, surface)

class fleeingSheep(Sheep):
    def __init__(self, pos, surface):
        super().__init__(pos, surface)
