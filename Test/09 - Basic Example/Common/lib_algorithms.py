
def vig2(R1):
	R2 = R1.snapshot[0]
	if R1.color == 0:
		if R2.color == 0:
			R1.target = ((R1.x+R2.x)/2, (R1.y+R2.y)/2) 
			R1.color = 1
			R1.phase = 'MOVING'
		else:
			R1.target = (R2.x, R2.y) 
			R1.phase = 'MOVING'
	else:
		R1.phase = 'WAITING'
		if R2.color == 1:
			R1.color = 0
