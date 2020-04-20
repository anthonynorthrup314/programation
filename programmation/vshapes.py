import programmation.helpers as helpers
import programmation.vshape as vshape


class Rectangle(vshape.VShape):
    CONFIG = {
        "make_closed": True,
        "width": 1.,
        "height": 1.
    }

    def __init__(self, **kwargs):
        helpers.handle_config(self, kwargs)
        vshape.VShape.__init__(self, **kwargs)

    def create_points(self):
        self.set_anchors([(0, 0), (0, self.height), (self.width, self.height),
                          (self.width, 0)], smooth=False)
        return self
