import aggdraw
from copy import deepcopy
from PIL import Image, ImageTk
import Tkinter as tk

from helpers import *
from shape import *

class Canvas(object):
	"""
	Handles the drawing of Shapes
	"""
	CONFIG = {
		"width": 640,
		"height": 480
	}
	def __init__(self, width, height, **kwargs):
		extras = dict(width = width, height = height)
		handle_config(self, kwargs, extras = extras);
		self.data = np.zeros((self.height, self.width, 3))
	
	def copy(self):
		return deepcopy(self)
	
	def draw(self, *shapes, **kwargs):
		"""
		Draw the shapes to memory
		"""
		# Handle kwargs
		background = kwargs.pop("background", None)
		# Verify input
		for shape in shapes:
			assert isinstance(shape, Shape), "Can only draw shapes to a canvas"
		if background:
			assert isinstance(background, np.ndarray), "Can only use a background stored as a numpy array"
			assert self.data.shape == background.shape, "Can only use a background of the same dimensions"
		assert len(kwargs) == 0, "Only supported keyword is 'background'"
		# Handle background
		if background:
			self.data = background.copy()
		else:
			self.data = np.zeros((self.height, self.width, 3))
		# Setup the image
		img = image_from_array(self.data)
		self.drawing = aggdraw.Draw(img)
		hasTransform = False
		# Draw each shape
		for shape in shapes:
			# Handle previous transform
			if hasTransform:
				if not shape.transform:
					self.drawing.settransform()
					hasTransform = False
			# Use shape transform
			if shape.transform:
				self.drawing.settransform(shape.transform.to_array())
				hasTransform = True
			# Setup the pen and brush
			pen = self.get_shape_pen(shape)
			brush = self.get_shape_brush(shape)
			# Draw the shape
			shape.draw(self, pen, brush)
		# Cleanup
		self.drawing.flush()
		del self.drawing
		self.data = np.array(img)
	
	def get_shape_pen(self, shape):
		"""
		Create a pen as defined by the shape
		"""
		# No stroke?
		if not shape.stroke_color or shape.stroke_width <= 0. or shape.stroke_alpha <= 0.:
			return None
		return aggdraw.Pen(shape.stroke_color.hex_l, width = shape.stroke_width, opacity = int(255 * shape.stroke_alpha))
	
	def get_shape_brush(self, shape):
		"""
		Create a brush as defined by the shape
		"""
		# No fill?
		if not shape.fill_color or shape.fill_alpha <= 0.:
			return None
		return aggdraw.Brush(shape.fill_color.hex_l, opacity = int(255 * shape.fill_alpha))
	
	def show(self):
		"""
		Show the canvas in a Tk window
		"""
		#TODO Move to separate class that handles multiple frames
		# Setup Tk
		padding = 1
		root = tk.Tk()
		root.geometry('{}x{}'.format(self.width + 2 * padding, self.height + 2 * padding))
		root.resizable(0, 0)
		# Create canvas object
		canvas = tk.Canvas(root, width = self.width, height = self.height)
		canvas.pack()
		# Convert to displayable image
		img = image_from_array(self.data)
		imgP = ImageTk.PhotoImage(img)
		# Add image to canvas
		imgC = canvas.create_image(padding, padding, image = imgP, anchor = "nw")
		# Display the window
		root.mainloop()
