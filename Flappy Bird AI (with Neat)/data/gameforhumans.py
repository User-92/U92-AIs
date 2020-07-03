# Setup Pygame and imports --------------------------------------------------------------------------------------------- #
import pygame, sys, random, os
import font as f

clock = pygame.time.Clock()
from pygame.locals import *

# Init Display ---------------------------------------------------------------------------------------------------------- #
pygame.init()
pygame.display.set_caption("Flappy Bird AI (Human Version)")
screen = pygame.display.set_mode((576, 800), 0, 32)
display = pygame.Surface((288, 400))

# Load Images ---------------------------------------------------------------------------------------------------------- #
background = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/base.png")
birb_img = pygame.image.load("img/bird/bird_0.png")
pipe_img = pygame.image.load("img/pipe.png")

font = f.Font("img/large_font.png")


# Classes and Funcs ---------------------------------------------------------------------------------------------------- #

# Birb class
class Bird():
    def __init__(self, x, y, size_x, size_y):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.images = {"0": pygame.image.load("img/bird/bird_0.png"),
                       "1": pygame.image.load("img/bird/bird_1.png"),
                       "2": pygame.image.load("img/bird/bird_2.png")}
        self.frame = 0
        self.currentimg = self.images[str(self.frame)]
        self.imgtimer = 0
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.vx = 0
        self.verticalmomentum = 0
        self.alive = True

    def jump(self):
        self.verticalmomentum = -6

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update_img(self):
        self.imgtimer += 1
        if self.imgtimer >= 7:
            self.imgtimer = 0
            self.frame += 1
            if self.frame >= 3:
                self.frame = 0
            self.currentimg = self.images[str(self.frame)]

    def move(self, groundrect):
        if self.rect.colliderect(groundrect):
            self.alive = False
            self.y = 349
        elif not self.alive and not self.rect.colliderect(groundrect):
            movement = [0, 0]
            self.verticalmomentum += 0.4
            if self.verticalmomentum > 7:
                self.verticalmomentum = 7
            movement[1] += self.verticalmomentum
            self.y += movement[1]
        if self.alive:
            movement = [0, 0]
            self.verticalmomentum += 0.4
            if self.verticalmomentum > 7:
                self.verticalmomentum = 7
            movement[1] += self.verticalmomentum
            self.y += movement[1]
        self.update_rect()

    def render(self, surf):
        surf.blit(self.currentimg, (self.x, self.y))


# Pipe class
class Pipe():
    def __init__(self, x, y, size_x, size_y, flipped=False):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.flipped = flipped
        if self.flipped:
            self.img = pygame.transform.flip(pipe_img, False, True)
        else:
            self.img = pipe_img
        self.rect = pygame.Rect(x, y, size_x, size_y)

    def move(self, movement):
        self.x -= movement
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def render(self, surf):
        surf.blit(self.img, (self.x, self.y))


# Game Function -------------------------------------------------------------------------------------------------------- #
def main():
    birb = Bird(125,300,32,24)
    groundrect = pygame.Rect(0, 369, 288, 30)

    pipes = []
    passedpipes = []
    pipetimer = 171

    spacepress = False
    groundscroll = 0

    score = 0
    groundadvance = 2
    while True:
        screen.fill((0, 0, 0))
        display.blit(background, (0, 0))
        font.render(display, f"Score: {int(score)}", (218, 10), 50)

        pipetimer += 1
        if birb.alive:
            if pipetimer >= 171:
                pipetimer = 0
                randy = random.randint(140, 300)
                pipes.append(Pipe(288, randy, 52, 300))
                pipes.append(Pipe(288, randy - 410, 52, 320, True))

        if birb.alive:
            groundscroll += groundadvance
            if groundscroll >= 48:
                groundscroll = 0
            birb.update_img()
        birb.move(groundrect)
        birb.render(display)

        pipepops = []
        for pipe in pipes:
            if birb.alive:
                pipe.move(2)
            # pygame.draw.rect(display, (255, 255, 255), pipe.rect)
            pipe.render(display)
            if pipe.x < 0 - pipe.size_x:
                pipepops.append(pipe)
            if birb.rect.colliderect(pipe.rect):
                birb.alive = False
            if birb.x > pipe.x + pipe.size_x and not pipe in passedpipes:
                score += 0.5
                passedpipes.append(pipe)
        for pipe in pipepops:
            pipes.remove(pipe)
            passedpipes.remove(pipe)

        display.blit(ground_img, (0 - groundscroll, 369))

        spacepress = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if birb.alive:
                        birb.jump()
        screen.blit(pygame.transform.scale(display, (576, 800)), (0, 0))
        pygame.display.update()
        clock.tick(60)
main()