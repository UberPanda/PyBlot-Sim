from random import SystemRandom, uniform, randint, sample
from time import time
from Common.lib_misc_functions import rob_centroid, dist, rob_SEC
from signal import signal, SIGINT
from sys import exit
from Common.lib_robot import Robot
from Common.lib_schedulers import scheduler


_sysrand = SystemRandom()

######################################################

## Simulation Parameters



## Robot parameters

RANGE_X = (-1,1) # Initial position range
RANGE_Y = (-1,1)

# Vision parameters

ASYNC_WORST = True

# Motion parameters

RIGID_MOTION = True
MINIMUM_DISTANCE = 0

######################################################

for NB_ROB in [2,3,4,5,10]:

	tries = 0
	start = time()
	elapsed = 0
	simus = []

	min_sim = 1
	max_sim = 1
	avg_sim = []

	while elapsed<10:
		tries += 1

		if tries == 1: # Just to more gracefully handle ctrl+c
			def signal_handler(sig, frame):
				avg_tot = (1000*sum(avg_sim) + sum(simus))/(1000*len(avg_sim) + len(simus)) 
				print()
				print('SSYNC CoG N')
				print('Number of Bots : ' + str(NB_ROB))
				print('Number of tries : ' + str(tries))
				print('Min : ' + str(min_sim))
				print('Max : ' + str(max_sim))
				print('Avg : ' + str(avg_tot))
				exit(0)
			signal(SIGINT, signal_handler)

		# Network initialization

		network = []
		for i in range(NB_ROB):
			network.append(Robot('r'+ str(i+1),uniform(RANGE_X[0],RANGE_X[1]),uniform(RANGE_Y[0],RANGE_Y[1]),0))

		
		for R1 in network:
			
			R1.ASYNC_worst = ASYNC_WORST
			R1.rigid_motion = RIGID_MOTION
			R1.minimum_distance = MINIMUM_DISTANCE
			
		## Beginning of the simulation
		
		pos_b = []
		walked_distances = []
		
		center = rob_centroid(network)
				
		Min_Dist = 0
		for R1 in network:
			Min_Dist = Min_Dist + dist((R1.x,R1.y), center) # Distance travelled in FSYNC
			pos_b.append((R1.x,R1.y))
			walked_distances.append(0)

		while True:
			
			lst = [i for i in range(len(network))]
			TBA = randint(1,len(network))
			activated = sample(lst,TBA)
			
			scheduler('SSYNC',network,'gathering_CoG',activated)
			
			## Live state monitoring
			
			for i in range(len(network)):
				walked_distances[i] = walked_distances[i] + dist(pos_b[i], (network[i].x,network[i].y)) # For each robot, the distance between the previous position and the current position
				pos_b[i] = (network[i].x,network[i].y)			

			## Victory condition
			
			win = True
			if rob_SEC(network)[2] > 10**(-10):
				win = False
			else:
				for R1 in network:
					if R1.phase != 'WAITING':
						win = False
						break
			
			if win == True:
				break

			## Defeat condition

				
		S_walk = sum(walked_distances)
		simus.append(S_walk/Min_Dist)
					
		elapsed = time() - start
		
		if tries %(1000) == 0: # Needed to no kill the RAM
			min_sim = min(min(simus),min_sim)
			max_sim = max(max(simus),max_sim)
			avg_sim.append(sum(simus) / len(simus))
			simus = []

	if tries >= 1000:
		avg_tot = (1000*sum(avg_sim) + sum(simus))/(1000*len(avg_sim) + len(simus)) 
	else:
		min_sim = min(min(simus),min_sim)
		max_sim = max(max(simus),max_sim)
		avg_tot = sum(simus) / len(simus)	
			
	print('SSYNC CoG N')
	print('Number of Bots : ' + str(NB_ROB))
	print('Number of tries : ' + str(tries))
	print('Min : ' + str(min_sim))
	print('Max : ' + str(max_sim))
	print('Avg : ' + str(avg_tot))
