import pygame
import pymunk
import random
import math
from pool.table import Table
from pool.ball import Ball
from pool.cue_ball import CueBall
from pool.cue import Cue

class PoolGame:
    background_color = (199, 199, 199)  # gray table

    yellow = (234, 195, 66)
    blue = (62, 101, 162)
    red = (194, 67, 65)
    black = (11, 8, 5)
    purple = (77, 63, 166)
    orange = (223, 112, 58)
    maroon = (96, 34, 36)
    green = (73, 127, 74)

    def __init__(self, width=400, height=800):
        # Setup window
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pool Simulation")
        self.clock = pygame.time.Clock()

        # Setup physics space
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)  # No gravity in top-down pool

        # Table boundaries
        self.table = Table(self.space)

        self.reset()

        self.running = True

    def reset(self):
        self.cue_ball = CueBall(self.space, (200, 600))
        self.cue = Cue(self.cue_ball)

        positions = Ball.rack_positions((200, 200), self.cue_ball.radius)
        self.balls: list[Ball] = []

        colors = [
            self.yellow,
            self.blue,
            self.blue,
            self.red,
            self.red,
            self.orange,
            self.orange,
            self.maroon,
            self.maroon,
            self.green,
            self.green,
            self.purple,
            self.purple,
        ]

        for index, pos in enumerate(positions):
            if index == 0:
                color = self.yellow
            elif index == 4: 
                color = self.black
            else:
                color = random.choice(colors)
                colors.remove(color)
            self.balls.append(Ball(self.space, pos, ball_color=color))

    def run(self):
        """Main game loop with custom drawing and click-and-drag ball."""
        bounds = ((50 + self.cue_ball.radius, 50 + self.cue_ball.radius), (350 - self.cue_ball.radius, 650 - self.cue_ball.radius))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.cue_ball.is_mouse_over(mouse_pos):
                        self.cue_ball.start_drag(mouse_pos)
                    else:
                        self.cue.start_drag(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.cue_ball.dragging:
                        self.cue_ball.stop_drag()
                    if self.cue.dragging:
                        self.cue.stop_drag()
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.cue_ball.dragging:
                        self.cue_ball.drag(mouse_pos, bounds)
                    if self.cue.dragging:
                        self.cue.drag(mouse_pos)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Shoot cue ball in direction of cue
                    angle = self.cue.angle
                    self.cue.hide()
                    power = 800  # adjust as needed
                    impulse = (math.cos(angle) * power, math.sin(angle) * power)
                    self.cue_ball.body.body_type = pymunk.Body.DYNAMIC
                    self.cue_ball.body.apply_impulse_at_local_point(impulse)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.reset()

            # Clear screen
            self.screen.fill(self.background_color)

            # Only step physics if not dragging
            if not self.cue_ball.dragging:
                self.space.step(1 / 60.0)

            self.table.draw(self.screen)

            for ball in self.balls:
                ball.draw(self.screen)

            self.cue_ball.draw(self.screen)
            self.cue.draw(self.screen)


            # Flip display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()