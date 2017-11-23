from colour import Color
import math
import numpy as np
from PIL import Image
import Tkinter as tk

# Some helpers copied from 3B1B's Manim project
# https://github.com/3b1b/manim

# Window dimensions
DEF_WIDTH = 640
DEF_HEIGHT = 480

def filter_locals(local_args):
	"""
	Remove the usual local variables
	"""
	excluded = ["self", "kwargs"]
	result = local_args.copy()
	for key in excluded:
		result.pop(key, local_args)
	return result

def combine_configs(configs):
	"""
	Combine configurations, first appearence takes priority
	"""
	all_items = list()
	for config in configs:
		all_items += config.items()
	config = dict()
	for item in all_items:
		key, value = item
		if key not in config:
			config[key] = value
		else:
			# Combine two child configs
			if isinstance(value, dict) and isinstance(config[key], dict):
				config[key] = combine_configs(config[key], value)
	return config

def handle_config(self, kwargs, local_args = {}):
	"""
	Sets up object variables based on configs
	"""
	# Get all superclass configurations
	superclasses = [self.__class__]
	configs = list()
	while len(superclasses) > 0:
		superclass = superclasses.pop()
		superclasses += superclass.__bases__
		if hasattr(superclass, "CONFIG"):
			configs.append(superclass.CONFIG)
	# Create priority order of configs
	all_configs = [kwargs, filter_locals(local_args), self.__dict__]
	all_configs += configs
	self.__dict__ = combine_configs(all_configs)

def is_number(val):
	"""
	Check if a value is a number
	"""
	try:
		return not math.isnan(float(val))
	except:
		return False
	return True

def degtorad(angle):
	"""
	Convert degrees to radians
	"""
	return angle * math.pi / 180.

def rotation_matrix(angle):
	"""
	Compute the usual rotation matrix
	"""
	angle = degtorad(angle)
	return np.matrix([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])

def image_from_array(data):
	"""
	Convert a numpy array to a PIL image
	"""
	return Image.fromarray(np.uint8(data))

def to_color(col):
	"""
	Convert different color representations to a Color object
	"""
	try:
		if isinstance(col, Color):
			return col
		if isinstance(col, str):
			return Color(col)
		if isinstance(col, tuple) or isinstance(col, list):
			if len(col) == 3:
				return Color(rgb=col)
			if len(col) == 4:
				t = col[0]
				col = (col[1], col[2], col[3])
				if t == "hsl":
					return Color(hsv=col)
				if t == "rgb":
					return Color(rgb=col)
				raise ValueError("Invalid color type: {}".format(t))
			raise ValueError()
		if isinstance(col, dict):
			return Color(**col)
		raise ValueError()
	except ValueError as e:
		if len(e.args) > 0:
			raise e
		raise ValueError("Invalid color format: {}".format(col))

def verify_bounds(bounds):
	"""
	Ensure the bounds are in a usable form
	"""
	assert isinstance(bounds, tuple), "Bounds must be in the form of a tuple"
	assert len(bounds) == 4, "Must provide four coordinates"
	for v in bounds:
		assert is_number(v), "Bounds must be a tuple of numbers"
