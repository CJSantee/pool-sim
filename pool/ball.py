import pygame
import pymunk
from pymunk.vec2d import Vec2d

class Ball:
    ball_color = (255, 255, 255)  # white
    radius = 15
    mass = 1

    def __init__(self, space: pymunk.Space, pos: tuple[float, float]):
        self.dragging = False
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, moment)
        self.body.position = Vec2d(*pos)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.01
        space.add(self.body, self.shape)

    def is_mouse_over(self, mouse_pos):
        """Return True if the mouse is over the ball."""
        dx = mouse_pos[0] - self.body.position.x
        dy = mouse_pos[1] - self.body.position.y
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

    def start_drag(self, mouse_pos):
        """Begin dragging the ball."""
        self.dragging = True
        self._drag_offset = (self.body.position.x - mouse_pos[0], self.body.position.y - mouse_pos[1])
        self.body.body_type = pymunk.Body.KINEMATIC
        self.body.velocity = (0, 0)

    def drag(self, mouse_pos, bounds=None):
        """Update the ball's position while dragging. Optionally clamp to bounds ((min_x, min_y), (max_x, max_y))."""
        if self.dragging:
            new_x = mouse_pos[0] + self._drag_offset[0]
            new_y = mouse_pos[1] + self._drag_offset[1]
            if bounds:
                (min_x, min_y), (max_x, max_y) = bounds
                new_x = min(max(new_x, min_x), max_x)
                new_y = min(max(new_y, min_y), max_y)
            self.body.position = (new_x, new_y)
            self.body.velocity = (0, 0)

    def stop_drag(self):
        """End dragging the ball and restore physics."""
        self.dragging = False
        # self.body.body_type = pymunk.Body.DYNAMIC
        # self.body.velocity = (0, 0)
        # self.body.angular_velocity = 0
        # self.body.force = (0, 0)
        print(f'self.body.position: {self.body.position}')

    def draw(self, screen: pygame.Surface):
        """Draw the ball on the given Pygame surface."""
        pos = self.body.position
        radius = self.shape.radius
        pygame.draw.circle(screen, self.ball_color, pos, int(radius))

    @property
    def position(self):
        return self.body.position