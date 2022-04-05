from Common.lib_misc_functions import dist, rob_angle, rob_SEC
import Common.lib_robot
from Common.lib_sim_functions import make_error_L

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
	fict_self = Common.lib_robot.Robot(R1.name, R1.x,R1.y)
	leader = R1.COMPUTE('geo_election')
	fict_net = [*R1.snapshot,fict_self]
	for i in range(0,tries):
		for R2 in fict_net:
			R3 = Common.lib_robot.Robot(R2.name,R2.x,R2.y)
			make_error_L(R1,R3)
			R3.snapshot = [x for x in fict_net if x.name != R3.name]
			if leader != R3.COMPUTE('geo_election'):
				return 'detected'
	return leader
