import pygame
import numpy as np
import time
import random

pygame.init()
win = [1200,800]
RED = [255,0,0]
BLACK = [0,0,0]

screen = pygame.display.set_mode(win)

class Fighter:
	def __init__(o,size,pos = [0,0],health = 10,color=RED):
		o.size = size
		o.max_health = health
		o.health = health
		o.attack = 1
		o.range = 1
		o.image = pygame.Surface([2*size,2*size])
		o.image.set_colorkey(BLACK)
		pygame.draw.circle(o.image,color,[size,size],size)
		o.pos = np.array(pos)
		o.speed = 5

	def move_to(o,pos):
		dir = - np.array(o.pos) + np.array(pos)
		dir = dir/np.linalg.norm(dir)
		o.pos = o.pos + o.speed*dir

	def move(o,d):
		o.pos = o.pos + np.array(d)

	def get_draw_pos(o):
		return o.pos - np.array(o.image.get_size())/2

	def resolve_collide(o,fighter):
		me_to_him = fighter.pos - o.pos
		dist = np.linalg.norm(me_to_him)
		overlap = o.size + fighter.size - dist
		if overlap > 0:
			push_away_dir = -me_to_him/dist
			push_ratio = o.size**2/(o.size**2+fighter.size**2)
			fighter.move(push_ratio*overlap*-push_away_dir)
			o.move((1-push_ratio)*overlap*push_away_dir)




fighters = []
for i in range(60):
	pos = [random.randint(0,500),random.randint(0,500)]
	size = random.randint(10,20)
	speed = random.randint((50-size)//5,(50-size)*2)
	color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
	fighters.append(Fighter(size,pos,color=color))
	
	fighters[i].speed = speed


tot_collision = 0
tot_draw = 0
running = True
t = time.time()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	if time.time() - t > 0.016:
		t = time.time()
		screen.fill(BLACK)
		mouse_pos = pygame.mouse.get_pos()

		#gestion mouvement et colision
		for fighter in fighters:
			fighter.move_to(mouse_pos)
			for other in fighters:
				if other != fighter:
					fighter.resolve_collide(other)

		#affichage
		for fighter in fighters:
			screen.blit(fighter.image,np.array(fighter.get_draw_pos(),dtype = int))


		pygame.display.update()

