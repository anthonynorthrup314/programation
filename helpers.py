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

def handle_config(self, kwargs, extras = {}):
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
	all_configs = [kwargs, extras, self.__dict__]
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

def rotation_matrix(angle):
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
