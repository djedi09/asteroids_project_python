import pygame
import random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        # Killed when hit by shot
        self.kill()

        # Figures out size of asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        
        # Figures out size of new asteroid(s)
        # when split
        angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # Creates new velocities for 1-2 more asteroids
        #
        velocity1 = self.velocity.rotate(angle)
        velocity2 = self.velocity.rotate(-angle)
        # Creates the new asteroids
        #
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        # Scales velocites up a bit
        #
        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2


