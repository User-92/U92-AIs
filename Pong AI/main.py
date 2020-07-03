import pygame, sys, os, random
import font as f
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Pong AI")
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH,HEIGHT),0,32)

class Ball():
    def __init__(self,x,y,sx,sy):
        self.x = x
        self.y = y
        self.size_x = sx
        self.size_y = sy
        self.vx = 5
        self.vy = 0
        self.rect = pygame.Rect(x,y,sx,sy)
    def get_rect(self):
        self.rect = pygame.Rect(self.x,self.y,self.size_x,self.size_y)
    def collion_check(self,rect):
        return self.rect.colliderect(rect)
    def update(self, paddles, playerscore, aiscore):
        collidewithpaddle = False
        if self.x >= WIDTH - self.size_x:
            self.vx = random.choice([-5,5])
            self.vy = 0
            self.x = WIDTH // 2 - self.size_x
            self.y = HEIGHT // 2 - self.size_y
            playerscore += 1
        elif self.x <= 0:
            self.vx = random.choice([-5,5])
            self.vy = 0
            self.x = WIDTH//2 - self.size_x
            self.y = HEIGHT // 2 - self.size_y
            aiscore += 1
        if self.y >= HEIGHT - self.size_y or self.y <= 0:
            self.vy *= -1

        movement = [0,0]
        movement[0] += self.vx
        movement[1] += self.vy
        self.x += movement[0]
        self.y += movement[1]

        for p1rect in paddles:
            if self.rect.colliderect(p1rect.rect):
                collidewithpaddle = True
                cppos = [self.x,self.y]
                self.vy = (((p1rect.y + 30) - self.y) //10 + random.randint(-5,5)//10) *-1

                self.x -= movement[0]
                self.vx *= -1
                self.x += self.vx
        self.get_rect()
        return playerscore, aiscore
    def render(self,surf):
        pygame.draw.rect(surf, (255,255,255), self.rect)

class Paddle():
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.size_x = x_size
        self.size_y = y_size
        self.rect = pygame.Rect(x, y, x_size, y_size)
    def get_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
    def move(self,movement):
        self.x += movement[0]
        self.y += movement[1]
        if self.y < 0 or self.y + self.size_y > HEIGHT:
            self.y -= movement[1]
        self.get_rect()
    def render(self, surf):
        pygame.draw.rect(surf, (255,255,255), self.rect)

down = False
up = False
w = False
s = False

font = f.Font("img/large_fontwhite.png")

paddles = []
paddles.append(Paddle(20,0,20,60))
paddles.append(Paddle(WIDTH - 40,0,20,60))

balls = []
balls.append(Ball(250,250,20,20))

aiscore = 0
playerscore = 0

while True:
    screen.fill((0,0,0))

    font.render(screen,f"{playerscore}",(200,10),100)
    font.render(screen, f"{aiscore}", (300, 10), 100)

    playerpmovement = [0,0]
    if up:
        playerpmovement[1] -= 5
    if down:
        playerpmovement[1] += 5
    aipmovement = [0, 0]
    if paddles[1].y > (balls[0].y//5)*5:
        aipmovement[1] -= 5
    elif paddles[1].y < (balls[0].y//5)*5:
        aipmovement[1] += 5

    paddles[0].move(playerpmovement)
    paddles[1].move(aipmovement)

    for paddle in paddles:
        paddle.render(screen)

    for ball in balls:
        playerscore,aiscore = ball.update(paddles,playerscore,aiscore)
        ball.render(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                down = True
            if event.key == K_UP:
                up = True
            if event.key == K_w:
                w = True
            if event.key == K_s:
                s = True
        if event.type == KEYUP:
            if event.key == K_DOWN:
                down = False
            if event.key == K_UP:
                up = False
            if event.key == K_w:
                w = False
            if event.key == K_s:
                s = False
    pygame.display.update()
    clock.tick(60)