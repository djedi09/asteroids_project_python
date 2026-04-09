import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.shot_cooldown = 0
        self.rotation = 0
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        # Starting point
        unit_vector = pygame.Vector2(0, 1)
        # Figures out direction pointed by player rotation
        # then goes in the direction pointed 
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt

        self.position += rotated_with_speed_vector

    def update(self, dt):
        # time cooldown on shot
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()
        # rotate left
        if keys[pygame.K_a]:
            self.rotate(-dt) 
        # rotate right
        if keys[pygame.K_d]:
            self.rotate(dt)
        # forward
        if keys[pygame.K_w]:
            self.move(dt) 
        # backward
        if keys[pygame.K_s]:
            self.move(-dt)
        # fire a shot
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.shot_cooldown > 0:
            return
        # resets cooldown
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        
        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = velocity * PLAYER_SHOOT_SPEED