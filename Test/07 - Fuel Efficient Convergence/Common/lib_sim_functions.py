from math import cos, sin, pi
from random import SystemRandom, uniform, choice
from Common.lib_misc_functions import rob_dist, rob_argument

_sysrand = SystemRandom()

def make_error_L(R1,R2): # To create errors in vision during MOVE phase, used in lib_robot
	
	if R1.LOOK_error_type == 'absolute':
		r = uniform(0,R1.LOOK_distance_error)
		t = uniform(0,2*pi)
		R2.x = R2.x + r*cos(t)
		R2.y = R2.y + r*sin(t)
			
	elif R1.LOOK_error_type == 'relative' or R1.LOOK_error_type == 'rel_angle_abs_dist': 
		r = uniform(-R1.LOOK_distance_error,R1.LOOK_distance_error)
		if R1.LOOK_angle_error < pi:
			t = uniform(-R1.LOOK_angle_error,R1.LOOK_angle_error) # Radians
		else:
			t = uniform(-pi,pi)
			
		r_12 = rob_dist(R1,R2) # Polar coordinates of R2 according to R1
		t_12 = rob_argument(R1,R2)
		
		t_12_a = t_12 + t # Polar coordinates of R2 according to R1 after error
		
		if R1.LOOK_error_type == 'relative':
			r_12_a = r_12 + r*(r_12)
			
			R2.x = R1.x + r_12_a * cos(t_12_a)
			R2.y = R1.y + r_12_a * sin(t_12_a)
		elif R1.LOOK_error_type == 'rel_angle_abs_dist':
			r_12_a = r_12 + r
			
			R2.x = R1.x + r_12_a * cos(t_12_a)
			R2.y = R1.y + r_12_a * sin(t_12_a)
