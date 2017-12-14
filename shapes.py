import aggdraw
import numpy

import helpers
import shape

class TestShape(shape.Shape):
    """Just has an example drawing"""
    
    def draw_self(self, canvas, pen, brush):
        w, h = helpers.DEF_WIDTH, helpers.DEF_HEIGHT
        d = canvas.drawing
        d.line((0, 0, w, h), pen)
        d.line((0, h, w, 0), pen)
        d.arc((0, 0, w, h), 45, 135, pen)
        d.chord((0, 0, w, h), 135, 225, pen, brush)
        d.pieslice((0, 0, w, h), 225, 315, pen, brush)
        s = aggdraw.Symbol("M {} {} C {} {}, {} {}, {} {} Z".format(
            w / 2, h / 2, 2 * w / 3, h / 3, 5 * w / 6, 2 * h / 3, w, h / 2))
        d.symbol((0, 0, w, h), s, pen, brush)

class TestShapeChildren(shape.Shape):
    """Testing child shapes"""
    
    def __init__(self, **kwargs):
        shape.Shape.__init__(self, **kwargs)
        # Remove transform information from kwargs for children
        ckwargs = kwargs.copy()
        for key in ["transform", "parent_transform", "global_transform"]:
            ckwargs.pop(key, kwargs)
        # Create children
        w,h = helpers.DEF_WIDTH, helpers.DEF_HEIGHT
        bounds = (0, 0, w, h)
        self.add(
            Line((0, 0), (w, h), **ckwargs),
            Line((0, h), (w, 0), **ckwargs),
            Arc(bounds, 45, 135, **ckwargs),
            Chord(bounds, 135, 225, **ckwargs),
            PieSlice(bounds, 225, 315, **ckwargs),
            Symbol("M {} {} C {} {}, {} {}, {} {} Z".format(
                w / 2, h / 2, 2 * w / 3, h / 3, 5 * w / 6, 2 * h / 3, w,
                h / 2), **ckwargs)
        )

class BoundedShape(shape.Shape):
    """A shape with bounds"""
    
    def __init__(self, bounds, **kwargs):
        bounds = helpers.validate_bounds(bounds)
        helpers.handle_config(self, kwargs, locals())
        shape.Shape.__init__(self, **kwargs)

class Line(BoundedShape):
    """Simple line"""
    
    def __init__(self, p0, p1, **kwargs):
        points = helpers.validate_points(p0, p1)
        BoundedShape.__init__(self, points, **kwargs)
    
    def draw_self(self, canvas, pen, brush):
        canvas.drawing.line(self.bounds, pen)

class SliceShape(BoundedShape):
    """Part of a circle"""
    
    def __init__(self, bounds, start_angle, end_angle, **kwargs):
        for v in [start_angle, end_angle]:
            assert isinstance(v, int), "Angles must be integers"
        helpers.handle_config(self, kwargs, locals())
        BoundedShape.__init__(self, bounds, **kwargs)

class Arc(SliceShape):
    """Simple arc"""
    
    def draw_self(self, canvas, pen, brush):
        canvas.drawing.arc(self.bounds, self.start_angle, self.end_angle, pen)

class Chord(SliceShape):
    """Simple chord"""
    
    def draw_self(self, canvas, pen, brush):
        canvas.drawing.chord(self.bounds, self.start_angle, self.end_angle,
                             pen, brush)

class PieSlice(SliceShape):
    """Simple pie slice"""
    
    def draw_self(self, canvas, pen, brush):
        canvas.drawing.pieslice(self.bounds, self.start_angle, self.end_angle,
                                pen, brush)

class Symbol(shape.Shape):
    """SVG path object"""
    
    def __init__(self, path, **kwargs):
        assert isinstance(path, str), "Path must be a string"
        helpers.handle_config(self, kwargs, locals())
        self.update_symbol()
        shape.Shape.__init__(self, **kwargs)
    
    def draw_self(self, canvas, pen, brush):
        canvas.drawing.symbol((0, 0), self.symbol, pen, brush)
    
    def path_string(self):
        """Return the shape as an SVG path string"""
        return self.path
    
    def update_symbol(self):
        """Update the internal aggdraw Symbol object"""
        self.symbol = aggdraw.Symbol(self.path_string())

class BezierCurve(Symbol):
    """A cubic bezier curve"""
    
    CONFIG = {
        "slice_pos": 1.,
        "close_path": False
    }
    
    def __init__(self, p0, p1, p2, p3, **kwargs):
        anchors = helpers.validate_points(p0, p1, p2, p3)
        assert anchors.shape[0] == 4, "You can only supply four points"
        helpers.handle_config(self, kwargs, dict(anchors=anchors))
        Symbol.__init__(self, "", **kwargs)
    
    def draw_self(self, canvas, pen, brush):
        if self.slice_pos != 0.:
            Symbol.draw_self(self, canvas, pen, brush)
    
    def path_string(self):
        path = "M {} {} C {} {}, {} {}, {} {}".format(*self.drawn.flatten())
        if self.close_path:
            path += " Z"
        return path
    
    def update_symbol(self):
        self.drawn = helpers.split_bezier(self.anchors, 0, self.slice_pos)
        Symbol.update_symbol(self)
    
    def slice(self, t):
        """Set the drawn curve to be a slice of the original"""
        self.slice_pos = t
        self.update_symbol()

class Polyline(Symbol):
    """Multiple line segments"""
    
    CONFIG = {
        "smooth": False,
        "smooth_factor": None
    }
    
    def __init__(self, *points, **kwargs):
        points = helpers.validate_points(*points)
        helpers.handle_config(self, kwargs, locals())
        Symbol.__init__(self, "", **kwargs)
    
    def path_string(self):
        path = "M {} {}".format(self.points[0, 0], self.points[0, 1])
        for i in range(self.handles.shape[1]):
            triplet = numpy.array([self.handles[0, i, :], self.handles[1, i, :],
                                self.points[i + 1, :]])
            path += " C {} {}, {} {}, {} {}".format(*triplet.flatten())
        if helpers.is_path_closed(self.points):
            path += " Z"
        return path
    
    def update_symbol(self):
        self.create_handles()
        Symbol.update_symbol(self)
    
    def create_handles(self):
        if self.smooth:
            self.handles = helpers.get_smooth_handles(self.points)
        else:
            self.handles = helpers.get_flat_handles(self.points)
