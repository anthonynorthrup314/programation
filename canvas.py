from copy import deepcopy

import aggdraw
from PIL import Image, ImageTk
import Tkinter as tk

import helpers

class Canvas(object):
    """Handles the drawing of Shapes"""
    
    CONFIG = {
        "width": helpers.DEF_WIDTH,
        "height": helpers.DEF_HEIGHT,
    }
    
    def __init__(self, **kwargs):
        helpers.handle_config(self, kwargs);
        self.data = np.zeros((self.height, self.width, 3))
    
    def copy(self):
        return deepcopy(self)
    
    def draw(self, *shapes, **kwargs):
        """Draw a list of shapes to the internal pixel data array
        
        shapes -- List of Shape objects to draw
        
        Keyword arguments:
        background -- Previous frame to draw on instead of on a black
                      background
        """
        # Handle kwargs
        background = kwargs.pop("background", None)
        # Verify input
        for shape in shapes:
            assert isinstance(shape, Shape), "Can only draw shapes to a canvas"
        if background:
            assert (isinstance(background, np.ndarray),
                    "Can only use a background stored as a numpy array")
            assert (self.data.shape == background.shape,
                    "Can only use a background of the same dimensions")
        assert len(kwargs) == 0, "Only supported keyword is 'background'"
        # Handle background
        if background:
            self.data = background.copy()
        else:
            self.data = np.zeros((self.height, self.width, 3))
        # Setup the image
        self.img = helpers.image_from_array(self.data)
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
        """Setup the aggdraw transformation"""
        # Remove previous transform
        if self.hasTransform:
            if transform is None:
                self.drawing.settransform()
                self.hasTransform = False
        # Use new transform
        if transform is not None:
            self.drawing.settransform(transform.to_array())
            self.hasTransform = True
