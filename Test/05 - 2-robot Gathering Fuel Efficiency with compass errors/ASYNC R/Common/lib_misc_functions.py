from math import sqrt, cos, sin, pi, atan2


def rob_argument(R1,R2):
	return atan2((R2.y-R1.y),(R2.x-R1.x))

def fix_argument(A): # Converts to [-pi,pi]
	A = A%(2*pi)
	if A > pi:
		return A - 2*pi
	else:
		return A

def rob_rotate(R1,R2,A): # Using Robots
	x_r1 = R2.x - R1.x
	y_r1 = R2.y - R1.y
	xn_r1 = cos(A)*x_r1-sin(A)*y_r1
	yn_r1 = sin(A)*x_r1+cos(A)*y_r1
	return (xn_r1+R1.x,yn_r1+R1.y)

def rotate(R1,R2,A): # Using tuples
	x_r1 = R2[0] - R1[0]
	y_r1 = R2[1] - R1[1]
	xn_r1 = cos(A)*x_r1-sin(A)*y_r1
	yn_r1 = sin(A)*x_r1+cos(A)*y_r1
	return (xn_r1+R1[0],yn_r1+R1[1])

def rob_centroid(robots):
	x_coords = 0
	y_coords = 0
	total = 0
	for r in robots:
		x_coords = x_coords + r.x
		y_coords = y_coords + r.y
		total = total + 1
	return (x_coords/total, y_coords/total)

def rob_angle(r1,r2,r3):
	A = rob_argument(r2,r3) - rob_argument(r2,r1)
	if A < 0:
		A = -A
	if A > pi:
		A = 2*pi - A
	return A

def rob_dist(R1,R2): # Using Robots
	return dist((R1.x,R1.y),(R2.x,R2.y))

def dist(T1,T2): # USing Tuples
	return sqrt((T1[0] - T2[0])**2+(T1[1] - T2[1])**2)
