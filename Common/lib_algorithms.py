from Common.lib_SEC import make_circle
from Common.lib_misc_functions import dist, rob_dist, rob_angle, rob_rotate, fix_argument, rob_centroid, rob_argument
from math import pi, cos, sin
import Common.lib_robot as lib_robot
from Common.lib_sim_functions import make_error_L
from random import randint, SystemRandom, choice

_sysrand = SystemRandom()

epsilon = 10**-6 ## Used to prevent angle approximation errors with compasses

def geo_election(R1):
	if len(R1.snapshot) < 2:
		raise Exception('You are trying to perform geoleader election for two robots or less, which is fundamentaly impossible.')
		#return 'Impossible'
	elif len(R1.snapshot) == 2:
		return lead_tri(R1)
	elif len(R1.snapshot) > 2:
		return lead_SEC(R1)

def lead_tri(R1): # Leader Election for three robots, variant using greatest angles instead of smallest
	A0 = rob_angle(R1.snapshot[1],R1,R1.snapshot[0]) # Computes the angles of self
	A1 = rob_angle(R1,R1.snapshot[0],R1.snapshot[1]) # Computes the angles of the first other
	A2 = rob_angle(R1.snapshot[0],R1.snapshot[1],R1) # Computes the angles of the second other
	
	if A0 < A1 and A0 < A2:
		return R1.name
	elif A1 < A2 and A1 < A0:
		return R1.snapshot[0].name
	elif A2 < A0 and A2 < A1:
		return R1.snapshot[1].name
	
	elif A0 == A1 and A0 == A2: # Cannot actually happen
		print('Equilateral')
	elif A1 == A2:
		print('Isosceles')
		return R1.name
	elif A0 == A2:
		print('Isosceles')
		return R1.snapshot[0].name
	elif A0 == A1:
		print('Isosceles') # statistically insignificant
		return R1.snapshot[1].name

def lead_SEC(R1):
	C_SEC = rob_SEC([R1, *R1.snapshot])[0:2] # Looks for the robot closest to the center of the SEC, identical distances are statistically insignificant so not implemented
	closest = R1
	smallest_distance = dist(C_SEC,(R1.x,R1.y))
	for R2 in R1.snapshot:
		new_distance = dist(C_SEC, (R2.x,R2.y))
		if new_distance < smallest_distance:
			smallest_distance = new_distance
			closest = R2
	return closest.name

def improved_geo_election(R1):
	tries = R1.sim_tries
	fict_self = lib_robot.Robot(R1.name, R1.x,R1.y)
	leader = R1.COMPUTE('geo_election')
	fict_net = [*R1.snapshot,fict_self]
	for i in range(0,tries):
		for R2 in fict_net:
			R3 = lib_robot.Robot(R2.name,R2.x,R2.y)
			make_error_L(R1,R3)
			R3.snapshot = [x for x in fict_net if x.name != R3.name]
			if leader != R3.COMPUTE('geo_election'):
				return 'detected'
	return leader

def gathering_CoG(R1):
	R1.target = rob_centroid([*(R1.snapshot),R1])
	R1.phase = 'WAITING'

def das4(R1):
	R2 = R1.snapshot[0]
	if R1.color == 0:
		if R2.color == 0:
			R1.target = ((R1.x+R2.x)/2, (R1.y+R2.y)/2) 
			R1.color = 1
			R1.phase = 'MOVING'
		elif(R2.color == 2):
			R1.target = (R2.x, R2.y) 
			R1.color = 1
			R1.phase = 'MOVING'
		else:
			R1.phase = 'WAITING'
	elif R1.color == 1:
		R1.color = 2 
		R1.phase = 'WAITING'
	elif R1.color == 2:
		if R2.color == 2 or R2.color == 3:
			R1.color = 3
		R1.phase = 'WAITING'
	elif R1.color == 3:
		if R2.color == 3 or R2.color == 0:
			R1.color = 0
		R1.phase = 'WAITING'

def vig2(R1):
	R2 = R1.snapshot[0]
	if R1.color == 0:
		if R2.color == 0:
			R1.target = ((R1.x+R2.x)/2, (R1.y+R2.y)/2) 
			R1.color = 1
			R1.phase = 'MOVING'
		else:
			R1.target = (R2.x, R2.y) 
			R1.phase = 'MOVING'
	else:
		R1.phase = 'WAITING'
		if R2.color == 1:
			R1.color = 0


def vig3(R1):
	R2 = R1.snapshot[0]
	if R1.color == 0:
		if R2.color == 0:
			R1.target = ((R1.x+R2.x)/2, (R1.y+R2.y)/2) 
			R1.color = 1
			R1.phase = 'MOVING'
		elif(R2.color == 1):
			R1.target = (R2.x, R2.y) 
			R1.phase = 'MOVING'
		elif(R2.color == 2):
			R1.phase = 'WAITING'
	elif R1.color == 1:
		if R2.color == 0:
			R1.phase = 'WAITING'
		elif(R2.color == 1):
			R1.color = 2 
			R1.phase = 'WAITING'
		elif(R2.color == 2):
			R1.target = (R2.x, R2.y) 
			R1.phase = 'MOVING'
	elif R1.color == 2:
		if R2.color == 0:
			R1.target = (R2.x, R2.y) 
			R1.phase = 'MOVING'
		elif(R2.color == 1):
			R1.phase = 'WAITING'
		elif(R2.color == 2):
			R1.color = 0
			R1.phase = 'WAITING'


def her2(R1):
	R2 = R1.snapshot[0]
	if R1.color == 0:
		if R2.color == 0 and R1.x != R2.x or R1.y != R2.y:
			R1.target = ((R1.x+R2.x)/2, (R1.y+R2.y)/2) 
			R1.color = 1
			R1.phase = 'MOVING'
		elif R2.color == 1 and R1.x != R2.x or R1.y != R2.y:
			R1.target = (R2.x, R2.y) 
			R1.phase = 'MOVING'
		else:
			R1.phase = 'WAITING'
	else:
		R1.phase = 'WAITING'
		if R2.color == 1:
			R1.color = 0


def RDV_compass_ASYNC_dynamic(R1):
	argP = fix_argument(rob_argument(R1,R1.snapshot[0])-R1.compass_offset) ## Between [-pi,pi]
	if argP >= -pi/2 - epsilon and argP <= pi/3-R1.compass_error + epsilon:
		R1.phase = 'WAITING'
	elif argP > pi/3 - R1.compass_error + epsilon and argP < 2*pi/3 + R1.compass_error - epsilon:
		move_dist = rob_dist(R1,R1.snapshot[0])
		R1.target = rob_rotate(R1,R1.snapshot[0],2*pi/3+2*R1.compass_error)
		R1.phase = 'MOVING'
	else:
		R1.target = (R1.snapshot[0].x,R1.snapshot[0].y)
		R1.phase = 'MOVING'



def RDV_compass_SSYNC_static(R1):
	argP = fix_argument(rob_argument(R1,R1.snapshot[0])-R1.compass_offset)
	if argP > (-pi/2)+R1.compass_error + epsilon and argP <= 0 + epsilon:
		R1.phase = 'WAITING'
	
	elif  argP <= (-pi/2)+R1.compass_error + epsilon and argP > -pi + epsilon:
		move_dist = rob_dist(R1,R1.snapshot[0])
		R1.target = (R1.x - move_dist*cos(R1.compass_offset),R1.y - move_dist*sin(R1.compass_offset))
		R1.phase = 'MOVING'
	
	else:
		R1.target = (R1.snapshot[0].x,R1.snapshot[0].y)
		R1.phase = 'MOVING'

def RDV_compass_SSYNC_dynamic(R1):
	argP = fix_argument(rob_argument(R1,R1.snapshot[0])-R1.compass_offset)
	if argP > -pi/2 + R1.compass_error + epsilon and argP <= pi/2 - R1.compass_error + epsilon:
		R1.phase = 'WAITING'
	
	elif argP <= -pi/2 - R1.compass_error + epsilon or argP > pi/2 + R1.compass_error + epsilon:
		R1.target = (R1.snapshot[0].x,R1.snapshot[0].y)
		R1.phase = 'MOVING'

	#elif (argP > pi/2 - R1.compass_error + epsilon and argP <= pi/2 + R1.compass_error + epsilon) or (argP > -pi/2 - R1.compass_error + epsilon and argP <= -pi/2 + R1.compass_error - epsilon):
	else:
		move_dist = rob_dist(R1,R1.snapshot[0])
		R1.target = rob_rotate(R1,R1.snapshot[0],pi/2+R1.compass_error)
		R1.phase = 'MOVING'
		

def fuel_efficient_convergence(R1):
	
	R2 = R1.snapshot[0]
	if R1.color == 0:
		if R2.color == 0:
			R1.target = ((R1.x+R2.x)/2, (R1.y+R2.y)/2) 
			R1.phase = 'MOVING'
		R1.color = 1
	else:
		R1.phase = 'WAITING'
		if R2.color == 1:
			R1.color = 0
