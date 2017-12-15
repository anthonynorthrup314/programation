import math
import os
import subprocess

import numpy
import PIL.ImageTk
import Tkinter

import canvas
import helpers
import shape

class Camera(object):
    """Controls multi-frame capture/display"""
    
    CONFIG = {
        "width": helpers.DEF_WIDTH,
        "height": helpers.DEF_HEIGHT,
        "frames": [],
        "loop_behavior": "loop", # Possible values: once, loop, reverse
        "canvas_config": {}
    }
    
    def __init__(self, **kwargs):
        helpers.handle_config(self, kwargs)
        self.canvas = canvas.Canvas(**helpers.change_kwargs(
            self.canvas_config, width=self.width, height=self.height))
    
    def capture_frame(self, *objects, **kwargs):
        """Create a new frame
        
        objects -- List of Shape objects to draw
        """
        self.canvas.draw(*objects, **kwargs)
        self.frames.append(self.canvas.data)
    
    def show(self, **kwargs):
        """Show the frames in a tk window"""
        TkCamera(self, **kwargs)
    
    def write_to_file(self, filename, fps=helpers.DEF_FPS, show_loop=False):
        """Save frames to a file
        
        Source:
        http://zulko.github.io/blog/2013/09/27/
            read-and-write-video-frames-in-python-using-ffmpeg/
        """
        assert isinstance(filename, str), "You must supply a valid filename"
        assert filename[-4:] == ".mp4", "Can only save to an mp4"
        assert isinstance(fps, int), "FPS can only be an integer"
        assert fps > 0, "FPS must be positive"
        absfile = os.path.abspath(filename)
        filedir = os.path.dirname(absfile)
        if not os.path.isdir(filedir):
            os.makedirs(filedir)
        command = [
            helpers.FFMPEG_BIN,
            "-y", # Overwrite
            "-f", "rawvideo",
            "-vcodec","rawvideo",
            "-s", "{}x{}".format(self.width, self.height),
            "-pix_fmt", "rgba",
            "-r", str(fps),
            "-i", "-", # From pipe
            "-an", # No audio
            "-vcodec", "libx264",
            "-pix_fmt", "yuv420p",
            "-loglevel", "error",
            absfile
        ]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if pipe is None:
            raise IOError("Could not start FFMPEG with given parameters: " +
                          command.join(" "))
        try:
            for frame in self.frames:
                pipe.stdin.write(frame.tostring())
            if show_loop == True and self.loop_behavior == "reverse":
                for frame in reversed(self.frames):
                    pipe.stdin.write(frame.tostring())
        except IOError as e:
            print pipe.communicate()[1]
            raise IOError()
        pipe.stdin.close()
        if pipe.stderr is not None:
            pipe.stderr.close()
        pipe.wait()
        print "Saved to '{}' successfully".format(filename)

class TkCamera(Tkinter.Tk):
    """Tk window for displaying camera data"""
    
    CONFIG = {
        "fps": helpers.DEF_FPS,
        "paused": False,
        "do_step": False,
        "frame": 0,
        "frame_speed": 1,
        "padding": 1,
        "temp": {}
    }
    
    def __init__(self, camera, **kwargs):
        width, height = camera.width, camera.height
        helpers.handle_config(self, kwargs, locals())
        Tkinter.Tk.__init__(self)
        # Setup Tk
        w, h, p = self.width, self.height, self.padding
        self.geometry("{}x{}".format(w + 2 * p, h + 2 * p))
        self.resizable(0, 0)
        self.bind("<Key>", self.cb_key)
        # Create canvas object
        self.canvas = Tkinter.Canvas(self, width=w, height=h, bg="black")
        self.canvas.pack()
        # Display the first frame
        if len(self.camera.frames) > 0:
            self.update_frame()
        # Don't animate without multiple frames
        if len(self.camera.frames) < 2:
            self.frame_speed = 0
        # Run loop
        self.step()
        self.mainloop()
    
    def update_frame(self):
        """Display the current frame"""
        # Clear previous frame
        self.canvas.delete("all")
        # Convert to displayable image
        data = self.camera.frames[self.frame]
        self.temp["img"] = helpers.image_from_array(data)
        if (self.width, self.height) != (self.camera.width,
                self.camera.height):
            self.temp["img"] = self.temp["img"].resize((self.width,
                                                        self.height))
        self.temp["imgP"] = PIL.ImageTk.PhotoImage(image=self.temp["img"])
        # Add image to canvas
        self.temp["imgC"] = self.canvas.create_image(
            self.padding, self.padding, image = self.temp["imgP"],
            anchor = "nw")
        # Add paused notice
        if self.paused:
            self.temp["paused"] = self.canvas.create_text(
                self.padding, self.padding, text = "PAUSED {}/{}".format(
                    self.frame + 1, len(self.camera.frames)), fill = "#FFFFFF",
                    anchor = "nw")
    
    def step(self):
        """Handle changing frames"""
        # Handle animation end
        if self.frame_speed == 0:
            # Won't update again
            return
        # Update screen if not paused
        if not self.paused or self.do_step:
            self.do_step = False
            # Next frame, handle loop behavior
            if (self.frame_speed > 0 and self.frame + self.frame_speed
                    >= len(self.camera.frames)):
                if self.camera.loop_behavior == "loop":
                    self.frame = (self.frame + self.frame_speed
                                  - len(self.camera.frames))
                elif self.camera.loop_behavior == "reverse":
                    self.frame = (2 * len(self.camera.frames)
                                  - (self.frame + self.frame_speed) - 1)
                    self.frame_speed *= -1
                else: # once
                    self.frame = len(self.camera.frames) - 1
                    self.frame_speed = 0
            elif self.frame_speed < 0 and self.frame + self.frame_speed < 0:
                if self.camera.loop_behavior == "loop":
                    self.frame = (self.frame + self.frame_speed
                                  + len(self.camera.frames))
                elif self.camera.loop_behavior == "reverse":
                    self.frame = -(self.frame + self.frame_speed)
                    self.frame_speed *= -1
                else: # once
                    self.frame = 0
                    self.frame_speed = 0
            else:
                self.frame += self.frame_speed
            # Display current frame
            self.update_frame()
        # Call step again later
        delay = int(math.ceil(1000. / self.fps)) if self.fps != 0 else 1
        self.after(delay, self.step)
    
    def cb_key(self, event):
        """Callback for key events"""
        key = event.keysym.lower()
        is_lower = key == event.keysym
        if key == "escape":
            self.destroy()
        elif key == "p":
            self.paused = not self.paused
            self.update_frame()
        elif key in ("enter", "space"):
            if self.paused:
                self.do_step = True
