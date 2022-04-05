from math import sqrt, pi, atan2
from Common.lib_SEC import make_circle


def rob_argument(R1,R2):
	return atan2((R2.y-R1.y),(R2.x-R1.x))

def rob_SEC(net):
	seq = []
	for R1 in net:
		seq.append((R1.x,R1.y))
		
	return make_circle(seq)

def rob_angle(r1,r2,r3):
	A = rob_argument(r2,r3) - rob_argument(r2,r1)
	if A < 0:
		A = -A
	if A > pi:
		A = 2*pi - A
	return A

def dist(T1,T2): # Using Tuples
	return sqrt((T1[0] - T2[0])**2+(T1[1] - T2[1])**2)
