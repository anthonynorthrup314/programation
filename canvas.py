from copy import deepcopy

import numpy

import aggdraw

import helpers
import shape

class Canvas(object):
    """Handles the drawing of Shapes"""

    CONFIG = {
        "width": helpers.DEF_WIDTH,
        "height": helpers.DEF_HEIGHT
    }

    def __init__(self, **kwargs):
        self.drawing = self.hasTransform = self.img = False

        helpers.handle_config(self, kwargs)
        self.data = numpy.zeros((self.height, self.width, 4))

    def copy(self):
        return deepcopy(self)

    def draw(self, *shapes_, **kwargs):
        """Draw a list of shapes to the internal pixel data array

        shapes_ -- List of Shape objects to draw

        Keyword arguments:
        background -- Previous frame to draw on instead of on a black
                      background
        """
        # Handle kwargs
        background = kwargs.pop("background", None)
        # Verify input
        for shape_ in shapes_:
            assert isinstance(shape_, shape.Shape), \
                   "Can only draw shapes to a canvas"
        if background:
            assert isinstance(background, numpy.ndarray), \
                   "Can only use a background stored as a numpy array"
            assert self.data.shape == background.shape, \
                   "Can only use a background of the same dimensions"
        assert not kwargs, "Only supported keyword is 'background'"
        # Handle background
        if background:
            self.data = background.copy()
        else:
            self.data = numpy.zeros((self.height, self.width, 4))
        # Setup the image
        self.img = helpers.image_from_array(self.data)
        self.drawing = aggdraw.Draw(self.img)
        self.hasTransform = False
        # Draw each shape
        for shape_ in shapes_:
            shape_.draw(self)
        # Cleanup
        self.drawing.flush()
        del self.hasTransform
        del self.drawing
        self.data = numpy.array(self.img)
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
