

def scheduler(sched,network,algo,activated=[]):
	
	if sched == 'FSYNC':
		for R1 in network:
			R1.LOOK(network,'FSYNC')
		for R1 in network:
			R1.COMPUTE(algo)
		for R1 in network:
			if R1.phase == 'MOVING':
				R1.MOVE()
			
	elif sched == 'SSYNC':
		if not activated:
			raise Exception('You need to input the activated parameter in SSYNC and ASYNC')
		partial_network = [network[i] for i in activated]
		for R1 in partial_network:
			R1.LOOK(network,'FSYNC')
		for R1 in partial_network:
			R1.COMPUTE(algo)
		for R1 in partial_network:
			if R1.phase == 'MOVING':
				R1.MOVE()
			
	elif sched == 'ASYNC':
		if not activated:
			raise Exception('You need to input the activated parameter in SSYNC and ASYNC')
		R1 = network[activated[0]]
		if R1.phase == 'WAITING':
			R1.LOOK(network,'ASYNC')
		elif R1.phase == 'COMPUTING':
			R1.COMPUTE(algo)
		elif R1.phase == 'MOVING':
			R1.MOVE()
			
	else:
		raise Exception('Unknown Scheduler')

