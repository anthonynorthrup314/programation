import helpers
import vshape

class Rectangle(vshape.VShape):
    CONFIG = {
        "make_closed": True,
        "width": 1.,
        "height": 1.
    }

    def __init__(self, **kwargs):
        self.make_closed = Rectangle.CONFIG["make_closed"]
        self.width = Rectangle.CONFIG["width"]
        self.height = Rectangle.CONFIG["height"]

        helpers.handle_config(self, kwargs)
        vshape.VShape.__init__(self, **helpers.change_kwargs(Rectangle.CONFIG,
                                                             **kwargs))

    def create_points(self):
        self.set_anchors([(0, 0), (0, self.height), (self.width, self.height),
                          (self.width, 0)], smooth=False)
        return self
