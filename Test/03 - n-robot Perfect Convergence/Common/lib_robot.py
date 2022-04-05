from random import uniform, SystemRandom, choice
import Common.lib_algorithms as lib_algos
from Common.lib_misc_functions import dist
from math import cos, sin, atan2

_sysrand = SystemRandom()

class Robot:
	def __init__(self, name, x, y, color=0):
		self.name = name
		self.x = x ## Real position in the network
		self.y = y 
				
		self.phase = 'WAITING'
		
		# Parameters
		
		self.rigid_motion = True # False for non-rigid
		self.minimum_distance = 0
		
		self.ASYNC_worst = True # True : picks the origin of movement when looking at a moving robot ; False : picks either origin, target, or in between.
		
		# Available info for COMPUTE :
		
		self.snapshot = [] ## snapshot
		self.target = ()




	def LOOK(self,network,scheduler):
		self.snapshot = []
		for R2 in network: 
			if self != R2:
				R2x = R2.x
				R2y = R2.y
				if not self.ASYNC_worst: # ASYNC behaviour that does not automatically pick the origin
					if scheduler == 'ASYNC' and R2.phase == 'MOVING':
						tgt = choice([0,1,2]) # 33% chance of picking the origin, 33% chance of picking the target, 33% of uniform between target and origin
						if tgt == 1:
							R2x = R2.target[0]
							R2y = R2.target[1]
						elif tgt == 2: 
							R2x = uniform(R2x, R2.target[0])
							R2y = uniform(R2y, R2.target[1])
						
						
				self.snapshot.append(Robot(R2.name, R2x, R2y))
		
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
	
		self.x = self.target[0]
		self.y = self.target[1]
			
		self.target = ()
		self.phase = 'WAITING'
