import numpy

import aggdraw

import programation.helpers as helpers
import programation.shape as shape


class VShape(shape.Shape):
    """A shape that consists only of bezier curve paths"""

    CONFIG = {
        "dim": 2,
        "make_closed": False
    }

    def __init__(self, **kwargs):
        helpers.handle_config(self, kwargs)
        shape.Shape.__init__(self, **kwargs)
        self.points = numpy.zeros((0, self.dim))
        self.create_points()

    def draw_self(self, canvas, pen, brush):
        if self.points.shape[0] == 0:
            return
        path = "M {} {}".format(*self.points[0, 0:2])
        # Convert to:
        # [[H00, H10, A1], [H01, H11, A2], ..., [H0n-1, H1n-1, An]]
        num_triplets = int((len(self.points) - 1) / 3)
        triplets = self.points[1:].reshape(num_triplets, 3, self.dim)
        for triplet in triplets:
            # Take only the (x,y) coordinates from each point
            path += " C {} {} {} {} {} {}".format(*triplet[:, 0:2].flatten())
        if helpers.is_path_closed(self.points):
            path += " Z"
        symbol = aggdraw.Symbol(path)
        canvas.drawing.symbol((0, 0), symbol, pen, brush)

    def create_points(self):
        # For sub classes
        return self

    def set_points(self, anchors, handles0, handles1):
        """Set points array to be:
        [A0, H00, H10, A1, H01, H11, ..., An]
        """
        assert len(handles0) == len(handles1), "Handles must have same length"
        assert len(anchors) == len(handles0) + 1, "# Points = # Handles + 1"
        num_points = len(handles0) * 3
        self.points = numpy.insert(numpy.stack([handles0, handles1,
                                                anchors[1:]], axis=1)
                                   .reshape(num_points, self.dim), 0, anchors[0], axis=0)

    def get_points(self):
        """Split back into (anchors, handles0, handles1)"""
        return [self.points[i::3] for i in range(3)]

    def set_anchors(self, points, smooth=True):
        points = numpy.array(points).astype(float)
        if not points.any():
            self.points = numpy.zeros((0, self.dim))
            return
        if self.make_closed and not helpers.is_path_closed(points):
            points = numpy.append(points, points[0:1], axis=0)
        if smooth:
            # Use smoothing method to calculate handles
            self.set_points(points, *helpers.get_smooth_handles(points))
        else:
            # Handles at 1/3 and 2/3 between each pair of anchor points
            self.set_points(points, *[helpers.interpolate(points[:-1],
                                                          points[1:], alpha)
                                      for alpha in (1./3, 2./3)])

    def flatten_with_points(self):
        # pylint: disable=no-member
        return [v for v in self.flatten() if isinstance(v, VShape)
                and v.points.any()]

    def subdivide(self, count=2):
        """Split each curve into n smaller curves"""
        if count <= 1:
            return self
        icount = 1. / count
        for obj in self.flatten_with_points():
            newpoints = numpy.array([obj.points[0]])
            for i in range(obj.count_anchors() - 1):
                curve = obj.points[3 * i:3 * i + 4]
                for j in range(count):
                    newpoints = numpy.append(newpoints, helpers.split_bezier(
                        curve, j * icount, (j + 1) * icount)[1:], axis=0)
            obj.points = newpoints
        return self

    def transform_nonlinear(self, f, args, expanded=False, **kwargs):
        for obj in self.flatten_with_points():
            anchors = obj.get_points()[0]
            if expanded:
                anchors = numpy.apply_along_axis(helpers.expand, 1, anchors,
                                                 f, *args, **kwargs)
            else:
                anchors = numpy.apply_along_axis(f, 1, anchors, *args,
                                                 **kwargs)
            obj.set_anchors(anchors, smooth=True)
        return self

    def interpolate(self, other, alpha=.5):
        self.points = (1. - alpha) * self.points + alpha * other.points
        return self

    ## Point Information ##

    def count_anchors(self):
        if not self.points.any():
            return 0
        return int((len(self.points) - 1) / 3) + 1

    ## Transform Methods ##

    def shift(self, delta):
        delta = numpy.array(delta)
        self.points += delta
        return self

    def scale(self, s):
        self.points *= s
        return self
