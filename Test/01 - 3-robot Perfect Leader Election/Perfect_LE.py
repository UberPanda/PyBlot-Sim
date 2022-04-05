# Run with python, not pypy

from random import uniform, SystemRandom
from time import time
import matplotlib.pyplot as plt
from Common.lib_robot import Robot

_sysrand = SystemRandom() # Uses OS CPRNG instead of python PRNG

######################################################

## Simulation Parameters



## Robot parameters

RANGE_X = (-1.5,1.5) # Initial position range
RANGE_Y = (-1.5,1.5)

# Vision parameters



# Motion parameters



######################################################

print('FSYNC Test for Perfect Leader Election')
print('Robots are r1 and r2')
print('In progress...')

start = time()
elapsed = 0

good = 0
errors = 0

win_r1_x = []
win_r1_y = []
win_r2_x = []
win_r2_y = []
win_r3_x = []
win_r3_y = []

error_x = []
error_y = []

simus = 0

# Network initialization

network = [0,0,0]
network[0] = Robot('r1',-0.5,0) # Not random for the figure, can be made random for unbiased data points
network[1] = Robot('r2',0.5,0)

while elapsed<10: # can be done with time, or number of simulations
	
	network[2] = Robot('r3',uniform(RANGE_X[0],RANGE_X[1]),uniform(RANGE_Y[0],RANGE_Y[1]))
	
	## Beginning of the simulation

	for R1 in network:
		R1.LOOK(network,'FSYNC')
	
	L1 = network[0].COMPUTE('geo_election')
	L2 = network[1].COMPUTE('geo_election')
	L3 = network[2].COMPUTE('geo_election') # No scheduler needed, we only need a single cycle
	

	## Live state monitoring



	## Victory condition
	
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

print(str(elapsed) + ' seconds' )
print(str(good) + ' good out of ' + str(simus) + ' tries' )
print(str(errors) + ' errors out of ' + str(simus) + ' tries -> ' + str(100*errors/simus) + '% of errors' )



plt.figure(figsize=(5,5))
plt.plot(win_r1_x, win_r1_y, 'r.',zorder=1)
plt.plot(win_r2_x, win_r2_y, 'g.',zorder=2)
plt.plot(win_r3_x, win_r3_y, 'b.',zorder=3)
plt.plot(error_x,error_y, 'y.',zorder=4)

plt.plot(network[0].x,network[0].y, 'ko',zorder=6)
plt.plot(network[1].x,network[1].y, 'ko',zorder=7)

plt.axis([RANGE_X[0],RANGE_X[1],RANGE_Y[0],RANGE_Y[1]])
plt.show() 
