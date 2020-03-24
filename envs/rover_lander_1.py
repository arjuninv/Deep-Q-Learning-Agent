try:
    from envs.core import Env
except:
    from core import Env

import pygame
import math
import random


class rover:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randrange(0,370, step=10)
        self.y = 0
    
    def draw_self(self):
        self.rover = pygame.Rect(int(self.x),int(self.y), 10, 50)
        pygame.draw.rect(self.screen, (255,255,255), self.rover, 1)

class platform:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        self.x = random.randrange(0,370, step=10)
        self.y = 290
    
    def draw_self(self):
        self.platform = pygame.Rect(int(self.x), int(self.y),30, 10) 
        pygame.draw.rect(self.screen, (255,255,255), self.platform, 1)


class rover_lander_1(Env):
    height = 300
    width = 400
    observation_space = (width, height)
    action_space = 4 # [0, 1, 2, 3]
    def __init__(self):
        self.done = False
        self.objects = []
        # Action Space
        #   0 - Do nothing
        #   1 - thruters left 
        #   2 - thruters down 
        #   3 - thruters right 
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.rover = rover(self.screen)
        self.platform = platform(self.screen)

    # def action_env(self):
    #     return "int ; 0:do nothing, 1:thrust down, 2: thrust left, 3:thrust right"
    
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
        if self.dis < 50 and self.rover.x in range(self.platform.x,self.platform.x + 30) and int(self.platform.y - self.rover.y) > 45:
            self.reward = 20
            self.quit()
        elif self.rover.y + 50 > self.height:
            print("oops")
            self.quit()

    
    def user_mod(self):
        while not self.done:
            self.reward = 0
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

            self.dis = math.hypot(self.rover.x - self.platform.x, self.rover.y - self.platform.y)
            pygame.time.wait(1)
            self.rover.y += 1
            self.reward = self.compute_reward()
            self.check_collision()
            self.frame = pygame.surfarray.array3d(self.screen)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            # print (self.frame, self.reward, self.done)
            print(self.reward)

    def save_frame(self):
        pass
    
    def reset(self):
        del self.rover
        del self.platform
        self.frame = pygame.surfarray.array3d(self.screen)
        self.done = False
        self.objects = []
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.rover = rover(self.screen)
        self.platform = platform(self.screen)
        return self.frame

    def observation(self):
        return (self.action, self.dis)
    
    def render(self):
        pass
    
    def compute_reward(self):
        try:
            lst = self.cur
        except:
            lst = abs(self.platform.x-self.rover.x)
        self.cur = abs(self.platform.x-self.rover.x)
        if lst > self.cur:
            return 1
        elif self.cur in range(0,20):
            return 1
        else:
            return 0
        # return (lst, self.cur)

    def step(self, action):
        self.dis = math.hypot(self.rover.x - self.platform.x, self.rover.y - self.platform.y)
        self.platform.draw_self()
        self.rover.draw_self()
        self.thrust(action)
        pygame.time.wait(1)
        self.rover.y += 10
        self.reward = self.compute_reward()
        self.check_collision()
        self.frame = pygame.surfarray.array3d(self.screen)
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        return (self.frame, self.reward, self.done)
    
    def random_action_sample(self):
        return (random.randint(0, 4) - 1) 
