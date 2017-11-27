import math
import numpy as np
from PIL import Image, ImageTk
import Tkinter as tk

from canvas import *
from helpers import *
from shape import *

class Camera(object):
	"""
	Controls multi-frame capture/display
	"""
	CONFIG = {
		"width": DEF_WIDTH,
		"height": DEF_HEIGHT,
		"frames": [],
		"loop_behavior": "loop", # once, loop, reverse
		"canvas_config": {}
	}
	def __init__(self, **kwargs):
		handle_config(self, kwargs)
		self.canvas = Canvas(**change_kwargs(self.canvas_config, width = self.width, height = self.height))
	
	def capture_frame(self, *objects):
		"""
		Create a new frame
		"""
		self.canvas.draw(*objects)
		self.frames.append(self.canvas.data)
	
	def show(self, **kwargs):
		"""
		Show the frames in a tk window
		"""
		TkCamera(self, **kwargs)

class TkCamera(object):
	"""
	Tk window for displaying camera data
	"""
	CONFIG = {
		"frame": 0,
		"frame_speed": 1,
		"frame_time": DEF_FRAMETIME,
		"padding": 1
	}
	def __init__(self, camera, **kwargs):
		handle_config(self, kwargs, locals())
		# Setup Tk
		w, h, p = self.camera.width, self.camera.height, self.padding
		self.root = tk.Tk()
		self.root.geometry('{}x{}'.format(w + 2 * p, h + 2 * p))
		self.root.resizable(0, 0)
		# Create canvas object
		self.canvas = tk.Canvas(self.root, width = w, height = h)
		self.canvas.pack()
		# Display the first frame
		if len(self.camera.frames) > 0:
			self.update_frame()
		# Don't animate without multiple frames
		if len(self.camera.frames) < 2:
			self.frame_speed = 0
		# Run loop
		self.step()
		self.root.mainloop()
	
	def update_frame(self):
		"""
		Display the current frame
		"""
		# Clear previous frame
		self.canvas.delete("all")
		# Store on self to avoid GC
		self.temp = dict(img=None, imgP=None, imgC=None)
		# Convert to displayable image
		data = self.camera.frames[self.frame]
		self.temp["img"] = image_from_array(data)
		self.temp["imgP"] = ImageTk.PhotoImage(master = self.canvas, width = self.camera.width, height = self.camera.height, image = self.temp["img"])
		# Add image to canvas
		self.temp["imgC"] = self.canvas.create_image(self.padding, self.padding, image = self.temp["imgP"], anchor = "nw")
	
	def step(self):
		"""
		Update the screen
		"""
		# Handle animation end
		if self.frame_speed == 0:
			# Won't update again
			return
		# Next frame, handle loop behavior
		if self.frame_speed > 0 and self.frame + self.frame_speed >= len(self.camera.frames):
			if self.camera.loop_behavior == "loop":
				self.frame = self.frame + self.frame_speed - len(self.camera.frames)
			elif self.camera.loop_behavior == "reverse":
				self.frame = 2 * len(self.camera.frames) - (self.frame + self.frame_speed)
			else: # once
				self.frame = len(self.camera.frames) - 1
		elif self.frame_speed < 0 and self.frame + self.frame_speed < 0:
			if self.camera.loop_behavior == "loop":
				self.frame = self.frame + self.frame_speed + len(self.camera.frames)
			elif self.camera.loop_behavior == "reverse":
				self.frame = -(self.frame + self.frame_speed)
			else: # once
				self.frame = 0
		else:
			self.frame += self.frame_speed
		# Display current frame
		self.update_frame()
		# Call step again later
		self.root.after(int(math.ceil(self.frame_time * 1000.)), self.step)
