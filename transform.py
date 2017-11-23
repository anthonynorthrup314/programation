from copy import deepcopy
import math
import numpy as np

from helpers import *

class Transform(object):
	"""
	Affine transform
	
	| x1 |   | a b c |   | x0 |
	| y1 | = | d e f | * | y0 |
	| 1  |   | 0 0 1 |   | 1  |
	
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
		return deepcopy(self)
	
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
		point = np.matmul(self.matrix, np.matrix([x, y, 1]).getT())
		return point[0], point[1]
	
	def combine(self, other):
		"""
		Combine two transformations
		"""
		# Use matrix multiplication
		self.matrix = np.matmul(self.matrix, other.matrix)
		return self
	
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
		return Transform(1, 0, dx, 0, 1, dy)
	
	def set_shift(self, dx, dy):
		"""
		Set the offsets
		"""
		self.matrix[0:2, 2] = np.matrix([dx, dy]).getT()
		return self
	
	def shift(self, ddx, ddy):
		"""
		Change the offsets
		"""
		self.matrix[0:2, 2] += np.matrix([ddx, ddy]).getT()
		return self
	
	@staticmethod
	def SKEW_ABOUT(xcenter, ycenter, a, b, c, d):
		"""
		Creates a Skew transformation
		"""
		offset = np.matrix([0, 0]).getT()
		if xcenter != 0. or ycenter != 0.:
			# Compute the offset for unshift->transform->shift
			center = np.matrix([xcenter, ycenter]).getT()
			offset = (np.identity(2, dtype=float) - np.matrix([[a, b], [c, d]])) * center
		return Transform(a, b, offset[0, 0], c, d, offset[1, 0])
	
	def skew_about(self, xcenter, ycenter, a, b, c, d):
		"""
		Changes the transform
		"""
		self.matrix = Transform.SKEW_ABOUT(xcenter, ycenter, a, b, c, d).combine(self).matrix
		return self
	
	@staticmethod
	def SKEW(a, b, c, d):
		"""
		Creates a basic Skew transformation
		"""
		return Transform.SKEW_ABOUT(0, 0, a, b, c, d)
	
	def set_skew(self, a, b, c, d):
		"""
		Sets the skew
		"""
		self.matrix[0:2, 0:2] = np.matrix([[a, b], [c, d]])
		return self
	
	def skew(self, a, b, c, d):
		"""
		Changes the transform
		"""
		self.matrix = Transform.SKEW(a, b, c, d).combine(self).matrix
		return self
	
	@staticmethod
	def RESIZE_ABOUT(xcenter, ycenter, scalar):
		"""
		Creates a Resize transformation
		"""
		return Transform.SKEW_ABOUT(xcenter, ycenter, scalar, 0, 0, scalar)
	
	def resize_about(self, xcenter, ycenter, scalar):
		"""
		Changes the transform
		"""
		self.matrix = Transform.RESIZE_ABOUT(xcenter, ycenter, scalar).combine(self).matrix
		return self
	
	@staticmethod
	def RESIZE(scalar):
		"""
		Creates a basic Resize transformation
		"""
		return Transform.RESIZE_ABOUT(0, 0, scalar)
	
	def set_resize(self, scalar):
		"""
		Sets the skew
		"""
		return self.set_skew(scalar, 0, 0, scalar)
	
	def resize(self, scalar):
		"""
		Changes the transform
		"""
		return self.skew(scalar, 0, 0, scalar)
	
	@staticmethod
	def ROTATE_ABOUT(xcenter, ycenter, angle):
		"""
		Creates a Rotation transform
		"""
		return Transform.SKEW_ABOUT(xcenter, ycenter, *rotation_matrix(angle).getA1())
	
	def rotate_about(self, xcenter, ycenter, angle):
		"""
		Changes the transform
		"""
		self.matrix = Transform.ROTATE_ABOUT(xcenter, ycenter, angle).combine(self).matrix
		return self
	
	@staticmethod
	def ROTATE(angle):
		"""
		Creates a basic Rotation transformation
		"""
		return Transform.ROTATE_ABOUT(0, 0, angle)
	
	def set_rotate(angle):
		"""
		Sets the skew
		"""
		return self.set_skew(*rotation_matrix(angle).getA1())
	
	def rotate(angle):
		"""
		Changes the transform
		"""
		self.matrix = Transform.ROTATE(angle).combine(self).matrix
		return self
