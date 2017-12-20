import vshape

class Rectangle(vshape.VShape):
    CONFIG = {
        "make_closed": True,
        "width": 1.,
        "height": 1.
    }
    
    def create_points(self):
        self.set_anchors([(0, 0), (0, self.height), (self.width, self.height),
            (self.width, 0)], smooth=False)
        return self
