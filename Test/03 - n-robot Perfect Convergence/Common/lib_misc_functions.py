from math import sqrt, atan2
from Common.lib_SEC import make_circle

def rob_centroid(robots):
	x_coords = 0
	y_coords = 0
	for r in robots:
		x_coords = x_coords + r.x
		y_coords = y_coords + r.y
	return (x_coords/len(robots), y_coords/len(robots))

def rob_dist(R1,R2): # Using Robots
	return dist((R1.x,R1.y),(R2.x,R2.y))

def dist(T1,T2): # Using Tuples
	return sqrt((T1[0] - T2[0])**2+(T1[1] - T2[1])**2)

def rob_SEC(net):
	seq = []
	for R1 in net:
		seq.append((R1.x,R1.y))
	return make_circle(seq)
