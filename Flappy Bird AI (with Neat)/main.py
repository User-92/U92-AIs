# /usr/bin/python3.7
# Setup Pygame and imports --------------------------------------------------------------------------------------------- #
import pygame, sys, random, os, pickle,neat
import data.font as f
clock = pygame.time.Clock()
from pygame.locals import *
# Init Display ---------------------------------------------------------------------------------------------------------- #
pygame.init()
pygame.display.set_caption("Flappy Bird AI")
screen = pygame.display.set_mode((576,800),0,32)
display = pygame.Surface((288,400))

# Load Images ---------------------------------------------------------------------------------------------------------- #
background = pygame.image.load("data/img/bg.png")
ground_img = pygame.image.load("data/img/base.png")
birb_img = pygame.image.load("data/img/bird/bird_0.png")
pipe_img = pygame.image.load("data/img/pipe.png")

font = f.Font("data/img/large_font.png")

# Classes and Funcs ---------------------------------------------------------------------------------------------------- #

# Birb class
class Bird():
    def __init__(self,x,y,size_x,size_y):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.images = {"0":pygame.image.load("data/img/bird/bird_0.png"),"1":pygame.image.load("data/img/bird/bird_1.png"),"2":pygame.image.load("data/img/bird/bird_2.png")}
        self.frame = 0
        self.currentimg = self.images[str(self.frame)]
        self.imgtimer = 0
        self.rect = pygame.Rect(x,y,size_x,size_y)
        self.vx = 0
        self.verticalmomentum = 0
        self.alive = True
        self.score = 0
        self.passedpipes = []
    def jump(self):
        self.verticalmomentum = -6
    def update_rect(self):
        self.rect = pygame.Rect(self.x,self.y,self.size_x,self.size_y)
    def update_img(self):
        self.imgtimer += 1
        if self.imgtimer >= 7:
            self.imgtimer = 0
            self.frame += 1
            if self.frame >= 3:
                self.frame = 0
            self.currentimg = self.images[str(self.frame)]

    def move(self):
        if self.alive:
            movement = [0, 0]
            self.verticalmomentum += 0.4
            if self.verticalmomentum > 7:
                self.verticalmomentum = 7
            movement[1] += self.verticalmomentum
            self.y += movement[1]
        self.update_rect()
    def render(self, surf):
        surf.blit(self.currentimg, (self.x,self.y))

# Pipe class
class Pipe():
    def __init__(self,x,y,size_x,size_y,flipped=False):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.flipped = flipped
        if self.flipped:
            self.img = pygame.transform.flip(pipe_img,False, True)
        else:
            self.img = pipe_img
        self.rect = pygame.Rect(x,y,size_x,size_y)
    def move(self, movement):
        self.x -= movement
        self.rect = pygame.Rect(self.x,self.y,self.size_x,self.size_y)
    def render(self,surf):
        surf.blit(self.img, (self.x,self.y))

# Game Function -------------------------------------------------------------------------------------------------------- #
def main(genomes,config):
    ge = []
    nets = []

    birbs = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birbs.append(Bird(125,300,32,24))
        g.fitness = 0
        ge.append(g)

    groundrect = pygame.Rect(0,369,288,30)

    pipes = []
    passedpipes = []
    pipetimer = 171

    groundscroll = 2
    scrollspeed = 2

    score = 0
    run = True
    passedpipe = False
    while run:
        screen.fill((0,0,0))
        display.blit(background, (0,0))
        font.render(display, f"Score: {int(score)}", (218, 10),50)

        groundscroll += scrollspeed
        if groundscroll >= 48:
            groundscroll = 0

        pipein = 0
        if len(birbs) > 0:
            if len(pipes) > 2 and birbs[0].x > pipes[0].x + pipes[0].size_x:
                pipein = 2
        else:
            run = False
            break

        pipetimer += 1
        if pipetimer >= 100:
            pipetimer = 0
            randy = random.randint(140, 300)
            pipes.append(Pipe(288, randy, 52, 300))
            pipes.append(Pipe(288, randy - 410, 52, 320, True))

        for x,birb in enumerate(birbs):
            birb.move()
            ge[x].fitness += 0.05

            try:
                output = nets[x].activate((birb.y, abs(birb.y - pipes[pipein].y), abs(birb.y - (pipes[pipein].y - 90)))) #90 9s the distance between the top pipe and the bottom pipe
            except:
                pass
            if output[0] > 0.5:
                birb.jump()

            if birb.rect.colliderect(groundrect) or birb.y < 0:
                birbs.pop(x)
                nets.pop(x)
                ge.pop(x)

            birb.update_img()
            birb.render(display)
        if score > 50:
            break

        pipepops = []
        for pipe in pipes:
            pipe.move(scrollspeed)
            pipe.render(display)
            if pipe.x < 0 - pipe.size_x:
                pipepops.append(pipe)
            for x,birb in enumerate(birbs):
                if birb.x > pipe.x + (pipe.size_x/2) and not pipe in birb.passedpipes:
                    birb.score += 0.5
                    passedpipe = True
                    ge[x].fitness += 3
                    birb.passedpipes.append(pipe)

                if birb.rect.colliderect(pipe.rect):
                    ge[x].fitness -= 1
                    birbs.pop(x)
                    nets.pop(x)
                    ge.pop(x)
        for pipe in pipepops:
            pipes.remove(pipe)
            #passedpipes.remove(pipe)
        if passedpipe:
            score += 1
            passedpipe = False

        display.blit(ground_img, (0 - groundscroll,369))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(pygame.transform.scale(display, (576,800)),(0,0))
        pygame.display.update()
        clock.tick(60)

# Neat Python Stuff ---------------------------------------------------------------------------------------------------- #
def run(configpath):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configpath)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main,50)
    with open("flapai.txt", "wb") as f:
        pickle.dump(winner, f, pickle.HIGHEST_PROTOCOL)
    f.close()

localdir = os.path.dirname(__file__)
configpath = os.path.join(localdir, "data/config.txt")
run(configpath)
