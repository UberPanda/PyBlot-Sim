# Run with python, not pypy

from random import uniform, SystemRandom
from time import time
import matplotlib.pyplot as plt
from Common.lib_robot import Robot

_sysrand = SystemRandom()

######################################################

## Simulation Parameters



## Robot parameters

RANGE_X = (-1.5,1.5) # Initial position range
RANGE_Y = (-1.5,1.5)

# Vision parameters

ERR_TYPE_L = 'absolute' # Can be 'none', 'relative', 'absolute' or 'rel_angle_abs_dist'

ERR_DIST_L = 0.001 # Maximum distance error. Proportional if ERR_TYPE_L is relative, absolute otherwise
ERR_ANG_L = 0  # Angular error (radians)



# Motion parameters



######################################################

for nb_tries in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25,30,40,50]:

	start = time()
	elapsed = 0

	good = 0
	errors = 0
	detected = 0

	win_r1_x = []
	win_r1_y = []
	win_r2_x = []
	win_r2_y = []
	win_r3_x = []
	win_r3_y = []

	error_x = []
	error_y = []
	
	detected_x = []
	detected_y = []
	
	simus = 0

	# Network initialization

	network = [0,0,0]
	network[0] = Robot('r1',-0.5,0) # Not random for figures
	network[1] = Robot('r2',0.5,0)

	while elapsed<10:
		
		network[2] = Robot('r3',uniform(RANGE_X[0],RANGE_X[1]),uniform(RANGE_Y[0],RANGE_Y[1]))

		for R1 in network:

			R1.LOOK_error_type = ERR_TYPE_L
			R1.LOOK_distance_error = ERR_DIST_L
			R1.LOOK_angle_error = ERR_ANG_L
			R1.sim_tries = nb_tries
			
		## Beginning of the simulation

		for R1 in network:
			R1.LOOK(network,'FSYNC')
		
		L1 = network[0].COMPUTE('improved_geo_election')
		L2 = network[1].COMPUTE('improved_geo_election')
		L3 = network[2].COMPUTE('improved_geo_election')
		
		## Live state monitoring



		## Victory condition
		if L1 == 'detected' or L2 == 'detected' or L3 == 'detected':
			detected+=1
			detected_x.append(network[2].x)
			detected_y.append(network[2].y)
		else:
			if L1 == L2 and L2 == L3:
				good+=1
				if L1 == 'r1':
					win_r1_x.append(network[2].x)
					win_r1_y.append(network[2].y)
				elif L1 == 'r2':
					win_r2_x.append(network[2].x)
					win_r2_y.append(network[2].y)
				elif L1 == 'r3':
					win_r3_x.append(network[2].x)
					win_r3_y.append(network[2].y)
					
			## Defeat condition
			
			else:	
				errors+=1
				error_x.append(network[2].x)
				error_y.append(network[2].y)

		simus+=1
		
		end = time()
		elapsed = end-start

	print(str(nb_tries) + ' detection tries')
	print(str(elapsed) + ' seconds' )
	print(str(good) + ' good out of ' + str(simus) + ' tries' )
	print(str(detected) + ' detections out of ' + str(simus) + ' tries -> ' + str(100*detected/simus) + '% of detections')
	print(str(errors) + ' errors out of ' + str(simus) + ' tries -> ' + str(100*errors/simus) + '% of errors')


	plt.figure(figsize=(5,5))
	plt.plot(win_r1_x, win_r1_y, 'r.',zorder=1)
	plt.plot(win_r2_x, win_r2_y, 'g.',zorder=2)
	plt.plot(win_r3_x, win_r3_y, 'b.',zorder=3)
	plt.plot(error_x,error_y, 'y.',zorder=4)
	plt.plot(detected_x,detected_y, 'c.',zorder=5)

	plt.plot(network[0].x,network[0].y, 'ko',zorder=6)
	plt.plot(network[1].x,network[1].y, 'ko',zorder=7)

	plt.axis([RANGE_X[0],RANGE_X[1],RANGE_Y[0],RANGE_Y[1]])
	plt.show() 
