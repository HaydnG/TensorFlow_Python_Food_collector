import random

import pygame
import numpy as np

pygame.init()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_s,
    KEYDOWN,
    QUIT,
    K_KP_1,
    K_KP_4,
)

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode([600, 600])

        self.player_size = 60
        self.player_y = 300


        self.food_y = 0
        self.food_size = 80
        self.food_count = 0
        self.miss_count = 0

        self.user_input = True
        self.draw_game = True


        self.observations = 2
        self.actions = 2

        self.running = True

        self._move_food()

    def step(self, action):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.draw_game = not self.draw_game
                    print(self.draw_game)

        if action == 0:
            self.player_y -= 200
        if action == 1:
            self.player_y += 200

        if self.draw_game:
            self._draw_frame()


        reward = 0
        if self.player_y == self.food_y:
            self.food_count += 1
            reward += 1
        else:
            self.miss_count +=1
            reward -= 1

        self.player_y = 300

        if self.food_count == 15:
            return self.get_state(), 1, True, self.food_count, self.miss_count
        elif self.miss_count == 10:
            return self.get_state(), -1, True, self.food_count, self.miss_count

        return self.get_state(), reward, False, self.food_count, self.miss_count


    def get_state(self):

        state = [True if self.food_y > self.player_y else False,
                True if self.food_y < self.player_y else False]

        return np.array(state, dtype=int)


    def _draw_frame(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 255), ((self.screen.get_width() / 2) - self.food_size/2, self.food_y, self.food_size, self.food_size))

        pygame.draw.rect(self.screen, (255, 0, 255), ((self.screen.get_width() / 2) - self.food_size/2, self.player_y, self.player_size, self.player_size))

        pygame.display.update()

    def reset(self):
        self.player_y = 300
        self.food_count = 0
        self.miss_count = 0
        self.running = True
        self._move_food()

    def _move_food(self):

        location = random.randint(0,1)

        if location == 0:
            self.food_y = 100
        elif location == 1:
            self.food_y = 500

