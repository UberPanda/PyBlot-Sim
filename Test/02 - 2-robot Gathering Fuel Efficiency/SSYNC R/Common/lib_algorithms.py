from Common.lib_misc_functions import rob_dist, rob_rotate, fix_argument, rob_centroid, rob_argument
from math import pi, cos, sin


epsilon = 10**-6 ## Used to prevent angle approximation errors with compasses


def gathering_CoG(R1):
	R1.target = rob_centroid([*(R1.snapshot),R1])
	R1.phase = 'MOVING'

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
