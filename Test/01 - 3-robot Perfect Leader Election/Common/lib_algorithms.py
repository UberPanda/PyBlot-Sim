from Common.lib_misc_functions import dist, rob_angle, rob_SEC

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
