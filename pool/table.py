import pygame
import pymunk

class Table:
    width = 300
    height = width * 2
    position = (50, 50) # Top-left corner
    thickness = 5
    
    # Colors
    wall_color = (91, 47, 45)  # brown
    cloth_color = (58, 129, 124)  # green

    def __init__(self, space: pymunk.Space):
        """Create the pool table walls."""
        self.walls = [
            pymunk.Segment(space.static_body, (self.position[0], self.position[1]), (self.position[0] + self.width, self.position[1]), self.thickness),   # Top
            pymunk.Segment(space.static_body, (self.position[0], self.position[1] + self.height), (self.position[0] + self.width, self.position[1] + self.height), self.thickness), # Bottom
            pymunk.Segment(space.static_body, (self.position[0], self.position[1]), (self.position[0], self.position[1] + self.height), self.thickness),   # Left
            pymunk.Segment(space.static_body, (self.position[0] + self.width, self.position[1]), (self.position[0] + self.width, self.position[1] + self.height), self.thickness)  # Right
        ]
        for wall in self.walls:
            wall.elasticity = 0.95
            wall.friction = 0.01
        space.add(*self.walls)
    
    def draw(self, screen: pygame.Surface):
        """Draw the table walls on the given Pygame surface."""
        # Draw walls
        for wall in self.walls:
            start = [int(coord) for coord in wall.a]
            end = [int(coord) for coord in wall.b]
            pygame.draw.line(screen, self.wall_color, start, end, int(wall.radius * 2))
        
        # Draw table surface
        pygame.draw.rect(screen, self.cloth_color, (self.position[0], self.position[1], self.width, self.height))