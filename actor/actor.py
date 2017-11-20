from helpers import *
from colour import Color

class Actor(object):
	"""
	Stores drawing information
	"""
	CONFIG = {
		"fill_color": None,
		"fill_alpha": 1.,
		"stroke_color": Color("white"),
		"stroke_width": 1.,
		"stroke_alpha": 1.,
		"children": []
	}
	def __init__(self, *args, **kwargs):
		handle_config(self, kwargs)
		self.children = self.validate_children(self.children)
		self.points = np.zeros((0, 3))
		self.create_points()
	
	def create_points(self):
		"""
		Populate the points array
		"""
		# Abstract
		pass
	
	def contains_reference_to(self, other):
		"""
		Try to reference other child tree
		"""
		# Located
		if self == other:
			return True
		# Check children
		for child in other.children:
			if child.contains_reference_to(other)
				return True
		# Couldn't find
		return False
	
	def validate_children(self, children):
		"""
		Ensure the children are valid, and make unique
		"""
		result = list()
		elements = set()
		for child in children:
			# Ensure they are all children
			if not isinstance(child, Actor):
				raise ValueError("Can only add other actors as children")
			# Check for recursion
			if child.contains_reference_to(self):
				raise ValueError("Can not create self-referencing loops")
			# Add unique
			if child not in elements:
				result.append(child)
				elements.add(child)
		return result
	
	def add(self, *children):
		"""
		Add children actors
		"""
		# Validate input
		children = self.validate_children(children)
		# Add to list
		self.children = combine_unique(self.children, children)
