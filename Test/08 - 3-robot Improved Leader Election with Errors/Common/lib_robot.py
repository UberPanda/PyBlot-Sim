import Common.lib_algorithms as lib_algos
from Common.lib_sim_functions import make_error_L

class Robot:
	def __init__(self, name, x, y):
		self.name = name
		self.x = x ## Real position in the network
		self.y = y 
				
		self.phase = 'WAITING'
		
		self.LOOK_error_type = 'none' # Can be 'relative', 'absolute' or 'rel_angle_abs_dist'
		self.LOOK_distance_error = 0
		self.LOOK_angle_error = 0
		
		# Available info for COMPUTE :
		
		self.snapshot = [] ## snapshot
		self.target = ()
		
		self.sim_tries = 0
		


	def LOOK(self,network,scheduler):
		self.snapshot = []
		for R2 in network: 
			if R2 != self:
				self.snapshot.append(Robot(R2.name, R2.x, R2.y))
		
		for R2 in self.snapshot: 
			if self.LOOK_error_type != 'none':
				make_error_L(self,R2)
		self.phase = 'COMPUTING'



	def COMPUTE(self,algo):
		try:
			result = getattr(lib_algos, algo)(self)
		except:
			raise AttributeError('This algorithm does not exist in the current version (or you made a typo ?)')
		
		if self.target == (self.x,self.y) or self.target == ():  ## Safety
			self.phase = 'WAITING'
		return result
