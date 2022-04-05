from math import sqrt, cos, sin, pi, atan2


def rob_centroid(robots):
	x_coords = 0
	y_coords = 0
	total = 0
	for r in robots:
		x_coords = x_coords + r.x
		y_coords = y_coords + r.y
		total = total + 1
	return (x_coords/total, y_coords/total)


def rob_argument(R1,R2):
	return atan2((R2.y-R1.y),(R2.x-R1.x))

def rob_dist(R1,R2): # Using Robots
	return dist((R1.x,R1.y),(R2.x,R2.y))

def dist(T1,T2): # USing Tuples
	return sqrt((T1[0] - T2[0])**2+(T1[1] - T2[1])**2)



