from random import uniform, SystemRandom, randint, choice
from time import time
from math import pi
from Common.lib_robot import Robot
from Common.lib_schedulers import scheduler
from Common.lib_misc_functions import rob_dist, dist


_sysrand = SystemRandom()

######################################################

## Simulation Parameters

SSTAB = True

## Robot parameters

COLOR_RANGE = range(2) # Total number of colors.

# Vision parameters

ERR_TYPE_L = 'relative' # Can be 'none', 'relative', 'absolute' or 'rel_angle_abs_dist'
ERR_DIST_L = 0 # Maximum distance error. Proportional if ERR_TYPE_L is relative, absolute otherwise
ERR_ANG_L = 0 # Angular error (radians)


# Motion parameters

RIGID_MOTION = True
MINIMUM_DISTANCE = 0

######################################################

f1 = open('results_ASYNC_FEC_err','a')

start = time()
elapsed = 0

while elapsed < 10:
	
	ERR_DIST_L = uniform(0,1)
	ERR_ANG_L = uniform(0,pi/2)

	# Network initialization

	network = []
	network.append(Robot('r1',0,0,0))
	network.append(Robot('r2',1,0,0))

	for R1 in network:
		if SSTAB == True:
			R1.color = choice(COLOR_RANGE)
	
		R1.LOOK_error_type = ERR_TYPE_L
		R1.LOOK_distance_error = ERR_DIST_L
		R1.LOOK_angle_error = ERR_ANG_L
		
		R1.rigid_motion = RIGID_MOTION
		R1.minimum_distance = MINIMUM_DISTANCE
	
	## Beginning of the simulation

	win = False
	pos_b = []
	walked_distances = []
	for r in network:
		pos_b.append((r.x,r.y))
		walked_distances.append(0)

	while True:
		
		activated = [randint(0,len(network)-1)]
		
		scheduler('ASYNC',network,'fuel_efficient_convergence',activated)
		
		## Live state monitoring
		
		for i in range(len(network)):
			walked_distances[i] = walked_distances[i] + dist((pos_b[i]),(network[i].x,network[i].y))
			pos_b[i] = (network[i].x,network[i].y)

		## Victory condition

		if rob_dist(network[0],network[1]) < max(10**(-10)*dist((0,0),(network[0].x,network[0].y)), 10**(-10)) and network[0].phase == 'WAITING' and network[1].phase == 'WAITING':
			win = True
			break
		
		
		## Defeat condition
		
		if rob_dist(network[0],network[1]) > 10:
			break
		
			
	if win:
		win = False
		f1.write(str(ERR_DIST_L) + ',' + str(ERR_ANG_L) + ',' + str(sum(walked_distances)) + '\n')
	else:
		f1.write(str(ERR_DIST_L) + ',' + str(ERR_ANG_L) + ',' + '-1' + '\n')
	

	elapsed = time() - start
