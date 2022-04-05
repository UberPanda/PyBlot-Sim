from math import sqrt

def rob_dist(R1,R2): # Using Robots
	return dist((R1.x,R1.y),(R2.x,R2.y))

def dist(T1,T2): # USing Tuples
	return sqrt((T1[0] - T2[0])**2+(T1[1] - T2[1])**2)
