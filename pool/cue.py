import pygame
import math
from pool.ball import Ball
from pymunk.vec2d import Vec2d
from typing import Tuple

class Cue:
    color = (238, 161, 128)  # light brown
    width = 6
    length = 180

    def __init__(self, ball: Ball, offset=25):
        """
        ball: the Ball object to aim at
        offset: distance from ball center to cue tip when at rest
        """
        self.ball = ball
        self.dragging = False
        self.angle = 0  # radians
        self.offset = offset

    def set_angle(self, mouse_pos: Tuple[int, int]):
        """Set the angle of the cue based on mouse position."""
        dx = self.ball.position[0] - mouse_pos[0]
        dy = self.ball.position[1] - mouse_pos[1]
        angle = math.atan2(dy, dx)
        self.angle = angle

    def start_drag(self, mouse_pos: Tuple[int, int]):
        """Begin dragging to adjust the angle of the cue."""
        self.dragging = True
        self.set_angle(mouse_pos)

    def drag(self, mouse_pos: Tuple[int, int]):
        """Update the cue's angle while dragging."""
        if self.dragging:
            self.set_angle(mouse_pos)

    def stop_drag(self):
        """End dragging the cue."""
        self.dragging = False

    def draw(self, screen):
        # Draw the cue using correct trigonometry
        ball_pos = self.ball.body.position
        # Direction vector (unit)
        dx = math.cos(self.angle)
        dy = math.sin(self.angle)
        # Tip of the cue (just offset from ball)
        tip_x = ball_pos.x - self.offset * dx
        tip_y = ball_pos.y - self.offset * dy
        # Butt of the cue (length away from tip, opposite direction)
        butt_x = tip_x - self.length * dx
        butt_y = tip_y - self.length * dy
        pygame.draw.line(screen, self.color, (int(tip_x), int(tip_y)), (int(butt_x), int(butt_y)), self.width)