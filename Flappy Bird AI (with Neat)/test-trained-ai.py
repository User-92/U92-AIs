# /usr/bin/python3.7
# AI NAME: BIRB
# Setup Pygame and imports --------------------------------------------------------------------------------------------- #
import pygame, sys, random, os, pickle,neat
import data.font as f

clock = pygame.time.Clock()
from pygame.locals import *

# Init Display ---------------------------------------------------------------------------------------------------------- #
pygame.init()
pygame.display.set_caption("Flappy Bird AI (After Training)")
screen = pygame.display.set_mode((576, 800), 0, 32)
display = pygame.Surface((288, 400))

# Load Images ---------------------------------------------------------------------------------------------------------- #
background = pygame.image.load("data/img/bg.png")
ground_img = pygame.image.load("data/img/base.png")
birb_img = pygame.image.load("data/img/bird/bird_0.png")
pipe_img = pygame.image.load("data/img/pipe.png")

font = f.Font("data/img/large_font.png")


# Classes and Funcs ---------------------------------------------------------------------------------------------------- #
# Birb class
class Bird():
    def __init__(self, x, y, size_x, size_y):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.images = {"0": pygame.image.load("data/img/bird/bird_0.png"),"1": pygame.image.load("data/img/bird/bird_1.png"),"2": pygame.image.load("data/img/bird/bird_2.png")}
        self.frame = 0
        self.currentimg = self.images[str(self.frame)]
        self.imgtimer = 0
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.verticalmomentum = 0
        self.alive = True

    def jump(self):
        # Jump Height
        self.verticalmomentum = -6

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update_img(self):

        #changing frames based of the frame timer
        self.imgtimer += 1
        if self.imgtimer >= 7:
            self.imgtimer = 0
            self.frame += 1
            if self.frame >= 3:
                self.frame = 0
            self.currentimg = self.images[str(self.frame)]

    def move(self, groundrect):
        #makes the birb fall to the ground
        if not self.alive and not self.rect.colliderect(groundrect):
            movement = [0, 0]
            self.verticalmomentum += 0.4
            if self.verticalmomentum > 7:
                self.verticalmomentum = 7
            movement[1] += self.verticalmomentum
            self.y += movement[1]
        #allows the birb to move it is alive
        if self.alive:
            movement = [0, 0]
            self.verticalmomentum += 0.4
            if self.verticalmomentum > 7:
                self.verticalmomentum = 7
            movement[1] += self.verticalmomentum
            self.y += movement[1]
        #updates the birb's rect
        self.update_rect()

    def render(self, surf):
        #blits the birbs current image on the surface provided
        surf.blit(self.currentimg, (self.x, self.y))


# Pipe class
class Pipe():
    def __init__(self, x, y, size_x, size_y, flipped=False):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        # stuff used for creating the top pipes
        self.flipped = flipped
        if self.flipped:
            self.img = pygame.transform.flip(pipe_img, False, True)
        else:
            self.img = pipe_img
        self.rect = pygame.Rect(x, y, size_x, size_y)

    def move(self, movement):
        #moves based on the movement provided (groundspeed)
        self.x -= movement
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def render(self, surf):
        #blits pipe's image on the surface provided
        surf.blit(self.img, (self.x, self.y))


# Game Function -------------------------------------------------------------------------------------------------------- #
def main(config):

    # NEAT Stuff ------------------------------------------------------------------------------------------------------- #
    # opening and loading the ai data
    with open("flapai.txt", "rb") as f:
        genome = pickle.load(f)
    # creating the neural network based on the data from the file
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Init ------------------------------------------------------------------------------------------------------------- #
    birb = Bird(125,300,32,24)
    groundrect = pygame.Rect(0, 369, 288, 30)
    pipes = []
    passedpipes = []
    pipetimer = 171
    groundscroll = 0
    score = 0
    groundadvance = 2
    output = [0,0]

    # Game Loop -------------------------------------------------------------------------------------------------------- #
    while True:
        # Background --------------------------------------------------------------------------------------------------- #
        screen.fill((0, 0, 0))
        display.blit(background, (0, 0))
        font.render(display, f"Score: {int(score)}", (218, 10), 50)

        if birb.alive:
            # variable used for moving the ground
            groundscroll += groundadvance
            if groundscroll >= 48:
                groundscroll = 0
            # update the birbs image
            birb.update_img()
            try:
                # getting the value from the network's output node based on the data given
                output = net.activate((birb.y, abs(birb.y - pipes[pipein].y), abs(birb.y - (pipes[pipein].y - 90)))) #90 9s the distance between the top pipe and the bottom pipe
            except:
                pass
            # if the output is over 0.5, meaning that birb thinks the bird should jump, birb jumps
            if output[0] > 0.5:
                birb.jump()
        #moving and rendering the player
        birb.move(groundrect)
        birb.render(display)

        # adding pipes based on the timer
        pipetimer += 1
        if birb.alive:
            if pipetimer >= 100:
                pipetimer = 0
                #finding the height the pipe should be at
                randy = random.randint(140, 300)
                #bottom pipe
                pipes.append(Pipe(288, randy, 52, 300))
                #top pipe
                pipes.append(Pipe(288, randy - 410, 52, 320, True))

        #getting the pipe infront of birb
        pipein = 0
        if len(pipes) >= 2 and birb.x > pipes[0].x + pipes[0].size_x:
            pipein = 2

        pipepops = []
        for pipe in pipes:
            # moving the pipes if birb is alivw
            if birb.alive:
                pipe.move(groundadvance)
            #rendering all pipes
            pipe.render(display)
            # if the pipe is off screen, the pipe is added to pipepops to be removed later (after the for loop)
            if pipe.x < 0 - pipe.size_x:
                pipepops.append(pipe)
            # if the birb collides with the pipe, it is no longer alive
            if birb.rect.colliderect(pipe.rect):
                birb.alive = False
            # if the birb has passed a pipe, it is given one point and is added to passedpipes so the player can't get points from pipes they have already passed
            if birb.x > pipe.x + pipe.size_x and not pipe in passedpipes:
                score += 0.5
                passedpipes.append(pipe)

        # removing all of the pipes that are off screen
        for pipe in pipepops:
            pipes.remove(pipe)
            passedpipes.remove(pipe)

        # resetting if the birb hits the ground
        if birb.rect.colliderect(groundrect):
            birb.alive = True
            birb.x = 125
            birb.y = 300
            birb.update_rect()
            groundadvance = 2
            pipes = []
            pipetimer = 100

        # displaying the ground image
        display.blit(ground_img, (0 - groundscroll, 369))

        # Buttons ------------------------------------------------------------------------------------------------------ #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Update Display ----------------------------------------------------------------------------------------------- #
        screen.blit(pygame.transform.scale(display, (576, 800)), (0, 0))
        pygame.display.update()
        clock.tick(60)

# Neat Python Stuff ---------------------------------------------------------------------------------------------------- #
localdir = os.path.dirname(__file__)
configpath = os.path.join(localdir, "data/config.txt")
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configpath)

# Run AI
main(config)