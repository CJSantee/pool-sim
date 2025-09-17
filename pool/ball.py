import pygame
import pymunk
import math
from pymunk.vec2d import Vec2d

class Ball:
    radius = 12
    mass = 1

    def __init__(self, space: pymunk.Space, pos: tuple[float, float], ball_color=None):
        if ball_color:
            self.ball_color = ball_color
        else:
            self.ball_color = (255, 255, 255)  # white
        self.dragging = False
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, moment)
        self.body.position = Vec2d(*pos)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.01
        space.add(self.body, self.shape)

    def draw(self, screen: pygame.Surface):
        """Draw the ball on the given Pygame surface."""
        pos = self.body.position
        radius = self.shape.radius
        pygame.draw.circle(screen, self.ball_color, pos, int(radius))
        pygame.draw.circle(screen, (255, 255, 255), pos, int(radius / 2.25))  # white outline

    @staticmethod
    def rack_positions(apex_pos: tuple[int, int], ball_radius: int):
        """Generate positions for racking 15 balls in a triangle formation."""
        positions: list[tuple[int, int]] = []
        rows = 5
        dx = 2 * ball_radius
        dy = math.sqrt(3) * ball_radius
        for row in range(rows):
            y = int(apex_pos[1] - row * dy)
            # Center the row horizontally
            x_start = apex_pos[0] - row * ball_radius
            for col in range(row + 1):
                x = int(x_start + col * dx)
                positions.append((x, y))
        return positions

    @property
    def position(self):
        return self.body.position