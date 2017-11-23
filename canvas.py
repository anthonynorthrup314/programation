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
		for v in [width, height]:
			assert isinstance(v, int), "Dimensions must be integers"
			assert v > 0, "Dimensions must be larger than 0"
		handle_config(self, kwargs, locals());
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
		self.img = image_from_array(self.data)
		self.drawing = aggdraw.Draw(self.img)
		self.hasTransform = False
		# Draw each shape
		for shape in shapes:
			shape.draw(self)
		# Cleanup
		self.drawing.flush()
		del self.hasTransform
		del self.drawing
		self.data = np.array(self.img)
		del self.img
	
	def set_transform(self, transform=None):
		"""
		Setup the aggdraw transformation
		"""
		# Handle previous transform
		if self.hasTransform:
			if not transform:
				self.drawing.settransform()
				self.hasTransform = False
		# Use transform
		if transform:
			self.drawing.settransform(transform.to_array())
			self.hasTransform = True
	
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
