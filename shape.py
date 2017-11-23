import aggdraw
from colour import Color
from copy import deepcopy

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
		"parent_transform": None,
		"global_transform": None
	}
	def __init__(self, **kwargs):
		handle_config(self, kwargs)
		self.update_transform()
		self.handle_colors()
	
	def copy(self):
		return deepcopy(self)
	
	def handle_colors(self):
		"""
		Convert various color inputs to Color objects
		"""
		self.stroke_color = to_color(self.stroke_color)
		self.fill_color = to_color(self.fill_color)
	
	def get_pen(self):
		"""
		Create a pen as defined by the shape
		"""
		# No stroke?
		if not self.stroke_color or self.stroke_width <= 0. or self.stroke_alpha <= 0.:
			return None
		return aggdraw.Pen(self.stroke_color.hex_l, width = self.stroke_width, opacity = int(255 * self.stroke_alpha))
	
	def get_brush(self):
		"""
		Create a brush as defined by the shape
		"""
		# No fill?
		if not self.fill_color or self.fill_alpha <= 0.:
			return None
		return aggdraw.Brush(self.fill_color.hex_l, opacity = int(255 * self.fill_alpha))
	
	def update_transform(self, parent_transform=False):
		"""
		Handle parent transform
		"""
		if parent_transform == False:
			parent_transform = self.parent_transform
		self.parent_transform = parent_transform
		self.global_transform = self.transform.copy()
		if self.parent_transform:
			self.global_transform.merge(self.parent_transform)
		#TODO Can update sub-objects here
	
	def pre_draw(self, canvas):
		"""
		Set up the transform and aggdraw objects
		"""
		canvas.set_transform(self.global_transform)
		self.pen = self.get_pen()
		self.brush = self.get_brush()
	
	def post_draw(self, canvas):
		"""
		Clean up the aggdraw objects
		"""
		del self.brush
		del self.pen
	
	def draw_self(self, canvas, pen, brush):
		"""
		Draw the shape to the canvas
		"""
		# Implemented in child classes
		pass
	
	def draw(self, canvas):
		"""
		Perform drawing events
		"""
		self.pre_draw(canvas)
		self.draw_self(canvas, self.pen, self.brush)
		self.post_draw(canvas)

class TestShape(Shape):
	"""
	Just has an example drawing
	"""
	def __init__(self, **kwargs):
		super(TestShape, self).__init__(**kwargs)
	def draw_self(self, canvas, pen, brush):
		"""
		Draw the shape to the canvas
		"""
		w = DEF_WIDTH
		h = DEF_HEIGHT
		d = canvas.drawing
		d.line((0, 0, w, h), pen)
		d.line((0, h, w, 0), pen)
		d.arc((0, 0, w, h), 45, 135, pen)
		d.chord((0, 0, w, h), 135, 225, pen, brush)
		d.pieslice((0, 0, w, h), 225, 315, pen, brush)
		s = aggdraw.Symbol("M {} {} C {} {}, {} {}, {} {} Z".format(w/2,h/2,2*w/3,h/3,5*w/6,2*h/3,w,h/2))
		d.symbol((0, 0, w, h), s, pen, brush)
