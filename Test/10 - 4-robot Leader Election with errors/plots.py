# Run with python, not pypy

from random import uniform, SystemRandom
from time import time
import matplotlib.pyplot as plt
from Common.lib_robot import Robot
from Common.lib_SEC import make_circle

_sysrand = SystemRandom() # Uses OS CPRNG instead of python PRNG

######################################################

## Simulation Parameters

STEPS_R3 = 10

## Robot parameters

RANGE_X = (-1.5,1.5) # Initial position range
RANGE_Y = (-1.5,1.5)

# Vision parameters

ERR_TYPE_L = 'absolute' # Can be 'none', 'relative', 'absolute' or 'rel_angle_abs_dist'

ERR_DIST_L = 0.001 # Maximum distance error. Proportional if ERR_TYPE_L is relative, absolute otherwise
ERR_ANG_L = 0  # Angular error (radians)

# Motion parameters



######################################################



# Network initialization

network = [0,0,0,0]
network[0] = Robot('r1',-0.5,0) # Not random for consistency
network[1] = Robot('r2',0.5,0)
network[2] = Robot('r3',RANGE_X[0],RANGE_Y[0])

yi = 0
while network[2].y <= (RANGE_X[0] + RANGE_X[1])/2 + 0.001: # to actually get simulations on the border
	xi = 0
	network[2].x = RANGE_X[0]
	while network[2].x <= (RANGE_X[0] + RANGE_X[1])/2 + 0.001:
		
		Circle = make_circle([(network[0].x,network[0].y),(network[1].x,network[1].y),(network[2].x,network[2].y)])
		
		elapsed = 0
		
		simus = 0

		good = 0
		errors = 0
		
		win_r1_x = []
		win_r1_y = []
		win_r2_x = []
		win_r2_y = []
		win_r3_x = []
		win_r3_y = []
		win_r4_x = []
		win_r4_y = []
		error_x = []
		error_y = []
		
		start = time()

		while elapsed<10:
	
			network[3]= Robot('r4',uniform(RANGE_X[0],RANGE_X[1]),uniform(RANGE_Y[0],RANGE_Y[1]))
			
			for R1 in network:
				R1.LOOK_error_type = ERR_TYPE_L
				R1.LOOK_distance_error = ERR_DIST_L
				R1.LOOK_angle_error = ERR_ANG_L
	
			
			## Beginning of the simulation

			for R1 in network:
				R1.LOOK(network,'FSYNC')
			
			L1 = network[0].COMPUTE('geo_election')
			L2 = network[1].COMPUTE('geo_election')
			L3 = network[2].COMPUTE('geo_election')
			L4 = network[2].COMPUTE('geo_election')

			## Live state monitoring



			## Victory condition
			
			if L1 == L2 and L2 == L3 and L3 == L4:
				good+=1
				if L1 == 'r1':
					win_r1_x.append(network[3].x)
					win_r1_y.append(network[3].y)
				elif L1 == 'r2':
					win_r2_x.append(network[3].x)
					win_r2_y.append(network[3].y)
				elif L1 == 'r3':
					win_r3_x.append(network[3].x)
					win_r3_y.append(network[3].y)
				elif L1 == 'r4':
					win_r4_x.append(network[3].x)
					win_r4_y.append(network[3].y)
					
			## Defeat condition
			else:
				errors+=1
				error_x.append(network[3].x)
				error_y.append(network[3].y)

			simus+=1
			
			end = time()
			elapsed = end-start

		print(str(elapsed) + ' seconds' )
		print(str(good) + ' good out of ' + str(simus) + ' tries' )
		print(str(errors) + ' errors out of ' + str(simus) + ' tries -> ' + str(100*errors/simus) + '% of errors' )



		plt.figure(figsize=(15,15))
		plt.plot(win_r1_x, win_r1_y, 'r.',zorder=1)
		plt.plot(win_r2_x, win_r2_y, 'g.',zorder=2)
		plt.plot(win_r3_x, win_r3_y, 'b.',zorder=3)
		plt.plot(win_r4_x, win_r4_y, 'c.',zorder=4)
		plt.plot(error_x,error_y, 'y.',zorder=5)

		plt.plot(network[0].x,network[0].y, 'ko',zorder=6)
		plt.plot(network[1].x,network[1].y, 'ko',zorder=7)
		plt.plot(network[2].x,network[2].y, 'ko',zorder=8)


		C1 = plt.Circle((Circle[0],Circle[1]),Circle[2],color='k', fill=False, lw=2,zorder=9)
		plt.gcf().gca().add_artist(C1)
		plt.plot(Circle[0],Circle[1],'kx',zorder=10)
		
		plt.axis([RANGE_X[0],RANGE_X[1],RANGE_Y[0],RANGE_Y[1]])
		plt.savefig('Figs/Fig'+str(yi)+'_'+str(xi)+'.png',bbox_inches='tight') 
		plt.clf()
		plt.close('all')

		network[2].x = network[2].x + (RANGE_X[1] - RANGE_X[0])/STEPS_R3
		xi = xi + 1
		
	network[2].y = network[2].y + (RANGE_Y[1] - RANGE_Y[0])/STEPS_R3
	yi = yi + 1
	

print(str(elapsed) + ' seconds' )
