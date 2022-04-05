

def scheduler(sched,network,algo):
	
	if sched == 'FSYNC':
		for R1 in network:
			R1.LOOK(network,'FSYNC')
		for R1 in network:
			R1.COMPUTE(algo)
		for R1 in network:
			if R1.phase == 'MOVING':
				R1.MOVE()

	else:
		raise Exception('Unknown Scheduler')

