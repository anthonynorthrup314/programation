import aggdraw

from helpers import *
from shape import *

class TestShape(Shape):
	"""
	Just has an example drawing
	"""
	def draw_self(self, canvas, pen, brush):
		w, h = DEF_WIDTH, DEF_HEIGHT
		d = canvas.drawing
		d.line((0, 0, w, h), pen)
		d.line((0, h, w, 0), pen)
		d.arc((0, 0, w, h), 45, 135, pen)
		d.chord((0, 0, w, h), 135, 225, pen, brush)
		d.pieslice((0, 0, w, h), 225, 315, pen, brush)
		s = aggdraw.Symbol("M {} {} C {} {}, {} {}, {} {} Z".format(w/2,h/2,2*w/3,h/3,5*w/6,2*h/3,w,h/2))
		d.symbol((0, 0, w, h), s, pen, brush)

class TestShapeChildren(Shape):
	"""
	Testing child shapes
	"""
	def __init__(self, **kwargs):
		Shape.__init__(self, **kwargs)
		# Remove transform information from kwargs
		ckwargs = kwargs.copy()
		for key in ["transform", "parent_transform", "global_transform"]:
			ckwargs.pop(key, kwargs)
		# Create children
		w,h = DEF_WIDTH, DEF_HEIGHT
		bounds = (0, 0, w, h)
		self.add(
			Line((0, 0, w, h), **ckwargs),
			Line((0, h, w, 0), **ckwargs),
			Arc(bounds, 45, 135, **ckwargs),
			Chord(bounds, 135, 225, **ckwargs),
			PieSlice(bounds, 225, 315, **ckwargs),
			Symbol(bounds, "M {} {} C {} {}, {} {}, {} {} Z".format(w/2,h/2,2*w/3,h/3,5*w/6,2*h/3,w,h/2), **ckwargs)
		)
		# Apply transform to children
		self.update_transform()

class BoundedShape(Shape):
	"""
	A shape with bounds
	"""
	def __init__(self, bounds, **kwargs):
		verify_bounds(bounds)
		handle_config(self, kwargs, locals())
		Shape.__init__(self, **kwargs)

class Line(BoundedShape):
	"""
	Simple line
	"""
	def draw_self(self, canvas, pen, brush):
		canvas.drawing.line(self.bounds, pen)

class Symbol(BoundedShape):
	"""
	SVG path object
	"""
	def __init__(self, bounds, path, **kwargs):
		assert isinstance(path, str), "Path must be a string"
		symbol = aggdraw.Symbol(path)
		handle_config(self, kwargs, locals())
		BoundedShape.__init__(self, bounds, **kwargs)
	
	def draw_self(self, canvas, pen, brush):
		canvas.drawing.symbol(self.bounds, self.symbol, pen, brush)
	
	def update(self):
		"""
		Update the internal aggdraw symbol object
		"""
		self.symbol = aggdraw.Symbol(self.path)

class SliceShape(BoundedShape):
	"""
	Part of a circle
	"""
	def __init__(self, bounds, start_angle, end_angle, **kwargs):
		for v in [start_angle, end_angle]:
			assert isinstance(v, int), "Angles must be integers"
		handle_config(self, kwargs, locals())
		BoundedShape.__init__(self, bounds, **kwargs)

class Arc(SliceShape):
	"""
	Simple arc
	"""
	def draw_self(self, canvas, pen, brush):
		canvas.drawing.arc(self.bounds, self.start_angle, self.end_angle, pen)

class Chord(SliceShape):
	"""
	Simple chord
	"""
	def draw_self(self, canvas, pen, brush):
		canvas.drawing.chord(self.bounds, self.start_angle, self.end_angle, pen, brush)

class PieSlice(SliceShape):
	"""
	Simple pie slice
	"""
	def draw_self(self, canvas, pen, brush):
		canvas.drawing.pieslice(self.bounds, self.start_angle, self.end_angle, pen, brush)
