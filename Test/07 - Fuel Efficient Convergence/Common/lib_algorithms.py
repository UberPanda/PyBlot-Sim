from Common.lib_misc_functions import rob_centroid

def gathering_CoG(R1):
	R1.target = rob_centroid([*(R1.snapshot),R1])
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
