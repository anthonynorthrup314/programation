import math
import numpy as np

from helpers import *

class Transform(object):
	"""
	Affine transform
	
	| a b c |   | x0 |   | x1 |
	| d e f | * | y0 | = | y1 |
	| 0 0 1 |   | 1  |   | 1  |
	
	x1 = a * x0 + b * y0 + c
	y1 = d * x0 + e * y0 + f
	"""
	def __init__(self, a, b, c, d, e, f):
		# Ensure proper arguments
		for v in [a,b,c,d,e,f]:
			assert is_number(v), "Parameters must be numbers"
		# Setup matrix
		self.matrix = np.matrix([[a, b, c], [d, e, f], [0., 0., 1.]])
	
	# Standard methods
	def __str__(self):
		return "{{Transform: [{}, {}, {}, {}, {}, {}]}}".format(*self.to_array())
	def __repr__(self):
		return self.__str__()
	def __eq__(self, other):
		if not isinstance(other, Transform):
			return False
		return self.matrix == other.matrix
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def copy(self):
		"""
		Create a deep copy
		"""
		return Transform(*self.to_array())
	
	def to_array(self):
		"""
		Get in a form usable by aggdraw
		
		Returns: (a, b, c, d, e, f)
		"""
		return self.matrix.getA1()[0:6]
	
	def apply(self, x, y):
		"""
		Apply the matrix to a point
		"""
		point = np.matmul(self.matrix, np.matrix([x, y, 1]))
		return point[0], point[1]
	
	def set_shift(self, dx = 0, dy = 0):
		"""
		Set the offset
		"""
		self.matrix[0:2, 2] = np.matrix([[dx], [dy]])
		return self
	
	def shift(self, ddx, ddy):
		"""
		Shift the offset
		"""
		self.matrix[0:2, 2] += np.matrix([[ddx], [ddy]])
		return self
	
	def scale(self, scalar):
		"""
		Adjust the scaling
		"""
		self.matrix[0:2, 0:2] *= scalar
		return self
	
	def set_skew(self, a, b, c, d):
		"""
		Set the skew
		"""
		self.matrix[0:2, 0:2] = np.matrix([[a, b], [c, d]])
		return self
	
	def skew(self, a, b, c, d):
		"""
		Adjust the skew
		"""
		self.matrix[0:2, 0:2] = np.matmul(self.matrix[0:2, 0:2], np.matrix([[a, b], [c, d]]))
		return self
	
	def rotate(self, angle):
		"""
		Adjust the skew, counter clock-wise
		"""
		return self.skew(*rotation_matrix(angle).getA1())
	
	def rotate_about(self, xcenter, ycenter, angle):
		"""
		Rotate the transformation about a point
		"""
		reshift = np.matrix([[xcenter, ycenter]]) - np.matmul(rotation_matrix(angle), np.array([xcenter, ycenter]))
		return self.rotate(-angle).shift(*reshift.getA1())
	
	@staticmethod
	def IDENTITY():
		"""
		Create an Identity transformation
		"""
		return Transform(1, 0, 0, 0, 1, 0)
	
	@staticmethod
	def SHIFT(dx, dy):
		"""
		Creates a basic Shift transformation
		"""
		return Transform.IDENTITY().set_shift(dx, dy)
	
	@staticmethod
	def RESIZE(scalar):
		"""
		Creates a basic Resize transformation
		"""
		return Transform.IDENTITY().scale(scalar)
	
	@staticmethod
	def SKEW(a, b, c, d):
		"""
		Creates a basic Skew transformation
		"""
		return Transform.IDENTITY().set_skew(a, b, c, d)
	
	@staticmethod
	def ROTATE(angle):
		"""
		Creates a basic Rotation transformation
		"""
		return Transform.IDENTITY().rotate(angle)
	
	@staticmethod
	def ROTATE_ABOUT(xcenter, ycenter, angle):
		"""
		Creates a Rotation transform
		"""
		return Transform.IDENTITY().rotate_about(xcenter, ycenter, angle)
