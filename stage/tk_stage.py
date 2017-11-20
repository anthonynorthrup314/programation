from PIL import Image, ImageTk
import Tkinter as tk

from helpers import *

class TkStage(tk.Tk):
	"""
	Display a stage in a tk window
	"""
	CONFIG = {
		"width": 320,
		"height": 240
	}
	def __init__(self, stage, **kwargs):
		tk.Tk.__init__(self, **kwargs)
		extras = {
			"width": stage.width,
			"height": stage.height,
			"stage": stage
		}
		handle_config(self, kwargs, extras = extras)
		# Configure window
		self.geometry('{}x{}'.format(self.width, self.height))
		#self.resizable(0, 0)
		# Create canvas
		self.canvas = tk.Canvas(self, width = self.width, height = self.height)
		self.canvas.pack()
		# Add frame to canvas
		self.stage.render_frame()
		img = image_from_array(self.stage.camera.data)
		imgP = ImageTk.PhotoImage(img)
		self.canvas.create_image(0, 0, image = imgP, anchor = "nw")
		# Display
		self.mainloop()
