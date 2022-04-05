from random import SystemRandom, uniform
from time import time
from Common.lib_robot import Robot

_sysrand = SystemRandom() # Uses OS CPRNG instead of python PRNG

######################################################

## Simulation Parameters



## Robot parameters



# Motion parameters




######################################################

print('FSYNC Test for Discrete Limitations')
print('Robots are r1 and r2')
print('In progress...')

simus = 0
start = time()
elapsed = 0

tries_each = [0,0]
failed = [0,0]

tested = 0 # the robot that is activated 

while simus < 2000000: # can be done with time or number of simulations
	simus += 1

	# Network initialization

	network = []
	network.append(Robot('r1',uniform(0,1),0))
	network.append(Robot('r2',uniform(2,3),0))
		

	## Beginning of the loop	
	
	while True:
		
		prev_net = [Robot('r1_prev',network[0].x,network[0].y) , Robot('r2_prev',network[1].x,network[1].y)] # save previous config to monitor fixed points
		
		R1 = network[tested]
		## Manual scheduling for this particular test
		R1.LOOK(network,'FSYNC')
		R1.COMPUTE('gathering_CoG')
		R1.MOVE()
		
		
		## Live state monitoring


		## Victory condition

		if (network[0].x,network[0].y) == (network[1].x,network[1].y): # Gathering (not really)
			break
		
		## Defeat condition
		
		elif (network[0].x,network[0].y, network[1].x,network[1].y) == (prev_net[0].x,prev_net[0].y, prev_net[1].x,prev_net[1].y): # Stuck
			failed[tested] += 1
			break
	
		
	
	elapsed = time() - start

	tries_each[tested] += 1
		
	if simus == 1000000:
		tested = 1

print('It took ' + str(elapsed) +' seconds')

print('Number of tries: ' + str(simus))
print('Failed r1: ' + str(failed[0]) + ' out of ' + str(tries_each[0]) + ' tries (' + str(100 * failed[0] / tries_each[0]) + '%)')
print('Failed r2: ' + str(failed[1]) + ' out of ' + str(tries_each[1]) + ' tries (' + str(100 * failed[1] / tries_each[1]) + '%)')
