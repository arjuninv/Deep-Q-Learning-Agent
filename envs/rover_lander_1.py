try:
    from envs.core import Env
except:
    from core import Env

import pygame
import math
import random
import numpy as np

dt = np.dtype(int)
dt = dt.newbyteorder('>')
pygame.init()

class rover:
    def __init__(self, screen):
        self.screen = screen
        self.x = 190
        self.y = 0
    
    def draw_self(self):
        self.rover = pygame.Rect(int(self.x),int(self.y), 10, 50)
        pygame.draw.rect(self.screen, (255,255,255), self.rover, 1)

class platform:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randrange(0,370, step=10)
        self.y = 290
    
    def draw_self(self):
        self.platform = pygame.Rect(int(self.x), int(self.y),30, 10) 
        pygame.draw.rect(self.screen, (255,255,255), self.platform, 1)


class rover_lander_1(Env):
    def __init__(self):
        self.height = 300
        self.width = 400
        self.done = False
        self.objects = []
        # Action Space
        #   0 - Do nothing
        #   1 - thruters left 
        #   2 - thruters down 
        #   3 - thruters right 
        self.action_space = [0, 1, 2, 3]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.rover = rover(self.screen)
        self.platform = platform(self.screen)
        self.score = 0
        self.reward = False
        self.surface = pygame.display.get_surface()


    def action_env(self):
        return "int ; 0:do nothing, 1:thrust down, 2: thrust left, 3:thrust right"
    

    def quit(self):
        self.done = True

    def thrust(self, dir):
        if dir == 1:
            self.rover.y -= 1
        elif dir == 2:
            self.rover.x -= 10
        elif dir == 3:
            self.rover.x += 10
        elif dir == 0:
            pass

    def check_collision(self):
        self.dis = math.hypot(self.rover.x - self.platform.x, self.rover.y - self.platform.y)
        if self.dis < 50 and self.rover.x in range(self.platform.x,self.platform.x + 30) and int(self.platform.y - self.rover.y) > 45:
            self.reset()
            self.score += 1
            self.reward = True
        elif self.rover.y + 50 > self.height:
            self.reset()

    def random(self):
        self.reward = False
        self.action = random.randrange(0,4, 1)

        # print(action)
        self.platform.draw_self()
        self.rover.draw_self()
        self.thrust(self.action)
        pygame.time.wait(100)
        self.rover.y += 10
        self.check_collision()
        self.frame = np.frombuffer(self.surface.get_buffer(), dtype=dt)
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        return (self.frame, self.reward, self.done)


    
    def user_mod(self):
        while not self.done:
            self.reward = False
            self.platform.draw_self()
            self.rover.draw_self()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.thrust(3)
                    elif event.key == pygame.K_a:
                        self.thrust(2)
                    elif event.key == pygame.K_w:
                        self.rover.y -= 10
                    elif event.key == pygame.K_s:
                        self.thrust(0)
                    elif event.key == pygame.K_q:
                        self.quit()

            pygame.time.wait(10)
            self.rover.y += 1
            self.check_collision()
            self.frame = np.frombuffer(self.surface.get_buffer(), dtype=dt)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            print (self.frame, self.reward, self.done)


    
    def save_frame(self):
        pass
    
    def reset(self):
        del self.rover
        del self.platform
        self.rover = rover(self.screen)
        self.platform = platform(self.screen)

    def observation(self):
        return (self.action, self.dis)

    def step(self, action):
        self.reward = False
        # while not self.done:
        self.action = action
        # print(action)
        self.platform.draw_self()
        self.rover.draw_self()
        self.thrust(self.action)
        pygame.time.wait(100)
        self.rover.y += 10
        self.check_collision()
        self.frame = np.frombuffer(self.surface.get_buffer(), dtype=dt)
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        return (self.frame, self.reward, self.done)

test = rover_lander_1()

# for _ in range(3):
#     print(test.random())



test.user_mod()