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
