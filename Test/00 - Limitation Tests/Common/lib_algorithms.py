from Common.lib_misc_functions import rob_centroid

def gathering_CoG(R1):
	R1.target = rob_centroid([*(R1.snapshot),R1])
	R1.phase = 'MOVING'
