import aggdraw
import numpy as np
from PIL import Image

from helpers import *

class Camera(object):
	"""
	Controls the drawing of frames
	"""
	CONFIG = {
		"width": 320,
		"height": 240
	}
	def __init__(self, *args, **kwargs):
		handle_config(self, kwargs)
		self.data = np.zeros((self.width, self.height, 3))
	
	def draw_frame(self, actors, background = None):
		"""
		Draw 
		"""
		# Handle background image
		if background != None:
			self.data = np.array(background)
		else:
			self.data = np.zeros((self.width, self.height, 3))
		# Draw the actors
		self.draw_actors(actors)
		# Return the frame
		return self.data
	
	def draw_actors(self, actors):
		"""
		Draw the actors
		"""
		# Create the image to draw on
		img = image_from_array(self.data)
		c = aggdraw.Draw(img)
		# Draw the actors
		for actor in actors:
			# Can only draw actors
			if not isinstance(actor, Actor):
				continue
			# Draw the actor
			self.draw_actor(actor, c)
		# Get the image data
		self.data = np.array(img)
	
	def draw_actor(self, actor, c):
		"""
		Draw an actor to the aggdraw object
		"""
		# Get the points of the actor
		points = actor.points
		# Can't draw if there is no data
		if len(points) == 0:
			return
		# Create a path from the points
		# Draw the path
		sym = aggdraw.Symbol(path)
		pen = self.actor_pen(actor)
		brush = self.actor_brush(actor)
		c.symbol((0, 0), sym, pen = pen, brush = brush)
	
	def actor_pen(self, actor):
		"""
		Get a pen for the actor
		"""
		# No stroke?
		if actor.stroke_color == None or actor.stroke_width == 0. or actor.stroke_alpha == 0.:
			return None
		# Create pen
		pen_color = actor.stroke_color.hex_l
		pen_width = actor.stroke_width
		pen_opacity = actor.stroke_alpha
		return aggdraw.Pen(pen_color, width = pen_width, opacity = pen_opacity)
	
	def actor_brush(self, actor):
		"""
		Get a brush for the actor
		"""
		# No fill?
		if actor.fill_color == None or actor.fill_alpha == 0.:
			return None
		# Create brush
		brush_color = actor.fill_color.hex_l
		brush_opacity = actor.fill_alpha
		return aggdraw.Brush(brush_color, opacity = brush_opacity)
