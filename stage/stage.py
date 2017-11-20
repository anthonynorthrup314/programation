from helpers import *
from camera import Camera

from tk_stage import TkStage

class Stage(object):
	"""
	Holds the actors
	"""
	CONFIG = {
		"width": 320,
		"height": 240,
		"camera_config": {}
	}
	def __init__(self, *args, **kwargs):
		handle_config(self, kwargs)
		self.camera = Camera(**self.camera_config)
	
	def render_frame(self):
		self.camera.draw_frame([])
	
	def show(self):
		TkStage(self)
