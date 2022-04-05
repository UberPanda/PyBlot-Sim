from random import SystemRandom, choice, uniform
from math import sqrt, pi, cos, sin
from Common.lib_robot import Robot
from Common.lib_schedulers import scheduler
from Common.lib_misc_functions import rob_dist

_sysrand = SystemRandom()

######################################################

SSTAB = True
COLOR_RANGE = range(2) # Total number of colors.

######################################################

simus = 0
act_list = []

while simus < 1000000:
	simus += 1

	# Network initialization

	network = []
	network.append(Robot('r1',0,0,0))
	
	ang = uniform(-pi,pi)
	network.append(Robot('r2',cos(ang),sin(ang),0))
	
	for R1 in network:
		if SSTAB == True:
			R1.color = choice(COLOR_RANGE)

	## Beginning of the simulation
	
	steps = 0
	while True:
		
		scheduler('FSYNC',network,'vig2')
		
		## Live state monitoring
		
		steps += 1
		
		## Victory condition

		if rob_dist(network[0],network[1]) < 10**(-10):
			break
		
		## Defeat condition

	act_list.append(steps)
	
	
print('FSYNC R Vig2')
print('Min : ' + str(min(act_list)))
print('Max : ' + str(max(act_list)))
print('Avg : ' + str(sum(act_list) / len(act_list)))
