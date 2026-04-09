import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from logger import log_state, log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	# Keeps the time in game constant and not dependent 
	# on PC preformance
	clock = pygame.time.Clock()
	dt = 0

	# Two groups empty so far of updatable and drawable
	# 
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable,)
	Shot.containers = (shots, updatable, drawable)

	# Instantiate the player and the asteroids in the center of the screen
	#
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	asteroid_field = AsteroidField()

	print("Starting Asteroids with pygame version: 2.6.1")
	print(f"Screen width: {SCREEN_WIDTH} Screen height: {SCREEN_HEIGHT}")
	
	while True:
		log_state()
		# This happens the events when they happen
		#
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		# Updates the player state
		# using a new Group()
		updatable.update(dt)
		# Check collisions on asteroids
		#
		for asteroid in asteroids:
			if asteroid.collides_with(player):
				log_event("player_hit")
				print("Game over!")
				sys.exit()

			for shot in shots:
				if asteroid.collides_with(shot):
					log_event("asteroid_shot")
					asteroid.split()
					shot.kill()

		# This method fills the screen black
		#
		screen.fill("black")
		# Draws the player
		#
		for thing in drawable:
			thing.draw(screen)
		# This method will refresh the screen
		#
		pygame.display.flip()
		# Limits framerate to 60 FPS
		# .tick(60) returns  the milliseconds
		# since last frame divided by 1000 to get delta time in seconds
		dt = clock.tick(60) / 1000


if __name__ == "__main__":
	main()
