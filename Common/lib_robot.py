from random import uniform, SystemRandom, choice
from Common.lib_sim_functions import make_error_L
from Common.lib_misc_functions import dist
from math import cos, sin, atan2
import Common.lib_algorithms as lib_algos

_sysrand = SystemRandom()

class Robot:
	def __init__(self, name, x, y, color=0):
		self.name = name
		self.x = x ## Real position in the network
		self.y = y 
				
		self.phase = 'WAITING'
		
		self.LOOK_error_type = 'none' # Can be 'relative', 'absolute' or 'rel_angle_abs_dist'
		self.LOOK_distance_error = 0
		self.LOOK_angle_error = 0
		
		self.compass = 'none'
		self.compass_error = 0
		self.compass_offset = 0
		
		self.rigid_motion = True # False for non-rigid
		self.minimum_distance = 0
		
		self.ASYNC_worst = True
		
		# Available info for COMPUTE :
		
		self.snapshot = [] ## snapshot
		self.color = color ## color
		self.target = ()
		
		# Misc
		
		self.obs_solved = False
		self.sim_tries = 0



	def LOOK(self,network,scheduler):
		if self.compass == 'dynamic':
			self.compass_offset = uniform(-self.compass_error,self.compass_error)
		self.snapshot = []
		for R2 in network: 
			if self != R2:
				R2x = R2.x
				R2y = R2.y
				if not self.ASYNC_worst: # ASYNC behaviour that does not automatically pick the worst case
					if scheduler == 'ASYNC' and R2.phase == 'MOVING':
						tgt = choice([0,1,2]) # 33% chance of picking the origin, 33% chance of picking the target, 33% of uniform between target and origin
						if tgt == 1:
							R2x = R2.target[0]
							R2y = R2.target[1]
						elif tgt == 2: 
							R2x = uniform(R2x, R2.target[0])
							R2y = uniform(R2y, R2.target[1])
						
				self.snapshot.append(Robot(R2.name, R2x, R2y, R2.color))
		
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
		else:
			if not self.rigid_motion: # change target for non rigid motion
				if dist((self.x,self.y),self.target) > self.minimum_distance: # Check if closer than delta
					tgt = choice([0,1,2]) # 33% chance of picking delta, 33% chance of picking the target, 33% of uniform between target and origin
					if tgt == 0:
						angle = atan2((self.target[1]-self.y),(self.target[0]-self.x))
						target_x = self.x+cos(angle)*self.minimum_distance # choose delta
						target_y = self.y+sin(angle)*self.minimum_distance
						self.target = (target_x,target_y)
					elif tgt == 1: 
						angle = atan2((self.target[1]-self.y),(self.target[0]-self.x))
						target_x = uniform(self.x+cos(angle)*self.minimum_distance,self.target[0]) # uniform between self+delta and target
						target_y = uniform(self.y+sin(angle)*self.minimum_distance,self.target[1])
						self.target = (target_x,target_y)
		return result


	def MOVE(self):

		self.x = self.target[0] # Rigid, move to target
		self.y = self.target[1]
			
		self.target = ()
		self.phase = 'WAITING'
