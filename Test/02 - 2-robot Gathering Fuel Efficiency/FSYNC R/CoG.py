from random import uniform, SystemRandom, randint, sample, choice
from time import time
from math import pi, sqrt
from Common.lib_robot import Robot
from Common.lib_schedulers import scheduler
from Common.lib_misc_functions import rob_dist,dist

from signal import signal, SIGINT
from sys import exit

_sysrand = SystemRandom()

######################################################

## Simulation Parameters

SSTAB = True

## Robot parameters

COLOR_RANGE = range(1) # Total number of colors.

# Vision parameters

COMPASS = 'none' # Can also be 'perfect', 'static' or 'dynamic'
COMPASS_ERROR = 0 # Angular error (radians)

# Motion parameters

RIGID_MOTION = True
MINIMUM_DISTANCE = 0

######################################################

tries = 0
start = time()
elapsed = 0
simus = []

min_sim = 1
max_sim = 1
avg_sim = []

while elapsed<10:
	tries += 1

	if tries == 1:
		def signal_handler(sig, frame):
			avg_tot = (1000*sum(avg_sim) + sum(simus))/(1000*len(avg_sim) + len(simus)) 
			print()
			print('FSYNC R CoG')
			print('Number of tries : ' + str(tries))
			print('Min : ' + str(min_sim))
			print('Max : ' + str(max_sim))
			print('Avg : ' + str(avg_tot))
			exit(0)
		signal(SIGINT, signal_handler)

	# Network initialization

	network = []
	network.append(Robot('r1',0,0,0))
	network.append(Robot('r2',1,0,0))

	for R1 in network:
		if SSTAB == True:
			R1.color = choice(COLOR_RANGE)

		R1.rigid_motion = RIGID_MOTION
		R1.minimum_distance = MINIMUM_DISTANCE

	## Beginning of the simulation

	pos_b = []
	walked_distances = []
	for r in network: # Travelled distance monitoring
		pos_b.append((r.x,r.y))
		walked_distances.append(0)

	while True:
		
		scheduler('FSYNC',network,'gathering_CoG')
		
		## Live state monitoring

		for i in range(len(network)):
			walked_distances[i] = walked_distances[i] + sqrt((pos_b[i][0]-network[i].x)**2 + (pos_b[i][1]-network[i].y)**2)
			pos_b[i] = (network[i].x,network[i].y)

		## Victory condition

		if rob_dist(network[0],network[1]) < max(10**(-10)*dist((0,0),(network[0].x,network[0].y)), 10**(-10)) and network[0].phase == 'WAITING' and network[1].phase == 'WAITING':
			break
		
		## Defeat condition
	

			
	S_walk = sum(walked_distances)
	simus.append(S_walk)
	elapsed = time() - start
	
	if tries %(1000) == 0:
		min_sim = min(min(simus),min_sim)
		max_sim = max(max(simus),max_sim)
		avg_sim = [sum(simus) / len(simus)]
		simus = []

if tries >= 1000:
	avg_tot = (1000*sum(avg_sim) + sum(simus))/(1000*len(avg_sim) + len(simus)) 
else:
	min_sim = min(min(simus),min_sim)
	max_sim = max(max(simus),max_sim)
	avg_tot = sum(simus) / len(simus)

print('FSYNC R CoG')
print('Number of tries : ' + str(tries))
print('Min : ' + str(min_sim))
print('Max : ' + str(max_sim))
print('Avg : ' + str(avg_tot))
