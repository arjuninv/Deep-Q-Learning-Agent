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
        self.x = random.randrange(0,45, step=10)
        self.y = 0
    
    def draw_self(self):
        self.rover = pygame.Rect(int(self.x),int(self.y), 5, 5)
        pygame.draw.rect(self.screen, (255,255,255), self.rover, 0)

class platform:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        self.x = random.randrange(0,35, step=1)
        self.y = 45
    
    def draw_self(self):
        self.platform = pygame.Rect(int(self.x), int(self.y),15, 5) 
        pygame.draw.rect(self.screen, (0, 217, 255), self.platform, 0)


class rover_lander_1(Env):
    height = 50
    width = 50
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
            self.rover.y -= 0.1
        elif dir == 2:
            if self.rover.x>0:
                self.rover.x -= 1
        elif dir == 3:
            if self.rover.x<45:
                self.rover.x += 1
        elif dir == 0:
            pass

    def check_collision(self):
        if self.dis < 11 and self.rover.x in range(self.platform.x,self.platform.x + 11) and int(self.platform.y - self.rover.y) < 5:
            self.reward = 20
            self.quit()
        elif self.rover.y + 5 > self.height:
            # print("oops")
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
                        self.rover.y -= 1
                    elif event.key == pygame.K_s:
                        self.thrust(0)
                    elif event.key == pygame.K_q:
                        self.quit()

            self.dis = math.hypot(self.rover.x - self.platform.x, self.rover.y - self.platform.y)
            pygame.time.wait(100)
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
        elif self.cur in range(0,11) and self.platform.x-self.rover.x <= 0:
            return 1
        else:
            return -1
        # return (lst, self.cur)

    def step(self, action):
        self.dis = math.hypot(self.rover.x - self.platform.x, self.rover.y - self.platform.y)
        self.platform.draw_self()
        self.rover.draw_self()
        self.thrust(action)
        # pygame.time.wait(100)
        self.rover.y += 1
        self.reward = self.compute_reward()
        self.check_collision()
        self.frame = pygame.surfarray.array3d(self.screen)
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        return (self.frame, self.reward, self.done)
    
    def random_action_sample(self):
        return (random.randint(0, 4) - 1) 
