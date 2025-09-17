import pygame
import pymunk
import pymunk.pygame_util
from pool.table import Table
from pool.ball import Ball
from pool.cue import Cue

class PoolGame:
    background_color = (199, 199, 199)  # gray table

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

        # Add a ball
        self.ball = Ball(self.space, (200, 600))

        # Add cue
        self.cue = Cue(self.ball)

        self.running = True

    def run(self):
        """Main game loop with custom drawing and click-and-drag ball."""
        bounds = ((50 + self.ball.radius, 50 + self.ball.radius), (350 - self.ball.radius, 650 - self.ball.radius))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.ball.is_mouse_over(mouse_pos):
                        self.ball.start_drag(mouse_pos)
                    else:
                        self.cue.start_drag(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.ball.dragging:
                        self.ball.stop_drag()
                    if self.cue.dragging:
                        self.cue.stop_drag()
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.ball.dragging:
                        self.ball.drag(mouse_pos, bounds)
                    if self.cue.dragging:
                        self.cue.drag(mouse_pos)

            # Clear screen
            self.screen.fill(self.background_color)

            # Only step physics if not dragging
            if not self.ball.dragging:
                self.space.step(1 / 60.0)

            self.table.draw(self.screen)
            self.ball.draw(self.screen)
            self.cue.draw(self.screen)

            # Flip display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()