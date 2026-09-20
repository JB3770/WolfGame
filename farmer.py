import pygame
import random

stride = 0


class Farmer:
    farmerSprite = pygame.transform.scale2x(pygame.image.load('farmer.png'))
    def __init__(self, pos, surface, state, direction, vision):
        self._pos = pos
        self.surface = surface
        self._state = state
        self._direction = direction
        self._vision = pygame.Rect((self._pos[0], self._pos[1], 100, 80))
        self._hitbox = pygame.Rect((self._pos[0], self._pos[1], 35, 70))

    def move(self, playerPos):
        if (self._state == 'calm'): 
            global stride
            if (stride <= 0):
                r = random.randint(1, 4)
                if (r == 1):
                    self._direction = 'up'
                elif (r == 2):
                    self._direction = 'right'
                elif (r == 3):
                    self._direction = 'down'
                else:
                    self._direction = 'left'
                stride = random.randint(30, 100)

            if (self._direction == 'right'):
                self._pos[0] += 1
            elif (self._direction == 'left'):
                self._pos[0] -= 1
            elif (self._direction == 'down'):
                self._pos[1] += 1
            else:
                self._pos[1] -= 1

            stride -= 1
            self._hitbox.topleft = self._pos
        elif (self._state == 'chase'):
            try:
                dx = (playerPos[0] - self._pos[0]) / abs(playerPos[0] - self._pos[0])
            except(ZeroDivisionError):
                dx = 0
            try:
                dy = (playerPos[1] - self._pos[1]) / abs(playerPos[1] - self._pos[1])
            except(ZeroDivisionError):
                dy = 0
            self._pos[0] += 3 * dx
            self._pos[1] += 3 * dy
            self._hitbox.topleft = self._pos

    @property
    def position(self):
        return self._pos

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, s):
        self._state = s

    @property
    def vision(self):
        return self._vision

    def manageVision(self):
        if self._direction == 'up':
            self._vision = pygame.Rect(
                self._hitbox.centerx - 40,
                self._hitbox.top - 300,
                80,
                300
            )

        elif self._direction == 'left':
            self._vision = pygame.Rect(
                self._hitbox.left - 300,
                self._hitbox.centery - 40,
                300,
                80
            )

        elif self._direction == 'down':
            self._vision = pygame.Rect(
                self._hitbox.centerx - 40,
                self._hitbox.bottom,
                80,
                300
            )

        else:  # right
            self._vision = pygame.Rect(
                self._hitbox.right,
                self._hitbox.centery - 40,
                300,
                80
            )

        pygame.draw.rect(self.surface, (0, 100, 255), self._vision, 3)

    def draw(self):
        self.manageVision()
        self.surface.blit(self.farmerSprite, self._hitbox.topleft)
        