import aggdraw
from colour import Color

from helpers import *
from transform import *

class Shape(object):
	"""
	Defines default values for other shapes
	"""
	CONFIG = {
		# Stroke
		"stroke_color": Color("white"),
		"stroke_width": 1.,
		"stroke_alpha": 1.,
		# Fill
		"fill_color": None,
		"fill_alpha": 1.,
		# Transform
		"transform": Transform.IDENTITY(),
	}
	def __init__(self, **kwargs):
		handle_config(self, kwargs)
		#TODO Handle other color inputs (eg. name and hex)
	
	def draw(self, canvas, pen=None, brush=None):
		"""
		Draw the shape to the canvas
		"""
		# Implemented in child classes
		#TODO Remove sample drawing code
		w = DEF_WIDTH
		h = DEF_HEIGHT
		d = canvas.drawing
		d.line((0, 0, w, h), pen)
		d.line((0, h, w, 0), pen)
		d.arc((0, 0, w, h), 45, 135, pen)
		d.chord((0, 0, w, h), 135, 225, pen, brush)
		d.pieslice((0, 0, w, h), 225, 315, pen, brush)
		s = aggdraw.Symbol("M {} {} C {} {}, {} {}, {} {} Z".format(w/2,h/2,2*w/3,h/3,5*w/6,h/3,w,h/2))
		d.symbol((0, 0, w, h), s, pen, brush)
