import Common.lib_algorithms as lib_algos


class Robot:
	def __init__(self, name, x, y):
		self.name = name
		self.x = x ## Real position in the network
		self.y = y 
				
		self.phase = 'WAITING'
		
		# Available info for COMPUTE :
		
		self.snapshot = [] ## snapshot
		self.target = ()
		


	def LOOK(self,network,scheduler):
		self.snapshot = []
		for R2 in network: 
			if R2 != self:
				self.snapshot.append(Robot(R2.name, R2.x, R2.y))
				
		self.phase = 'COMPUTING'


	def COMPUTE(self,algo):
		try:
			result = getattr(lib_algos, algo)(self)
		except:
			raise AttributeError('This algorithm does not exist in the current version (or you made a typo ?)')
		
		if self.target == (self.x,self.y) or self.target == ():  ## Small safety against weird scheduling
			self.phase = 'WAITING'
		
		return result
## Movement not needed for this test
