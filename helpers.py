import math

from colour import Color
import numpy
import PIL.Image
import scipy.linalg, scipy.misc

# Some helpers copied from 3B1B's Manim project
# https://github.com/3b1b/manim

# Constants
DEF_WIDTH = 640
DEF_HEIGHT = 480
DEF_FPS = 30
ZERO_TOLERANCE = .1

def filter_locals(local_args):
    """Remove the usual local variables
    
    Source: manim
    """
    excluded = ["self", "kwargs"]
    result = local_args.copy()
    for key in excluded:
        result.pop(key, local_args)
    return result

def combine_configs(configs):
    """Combine configurations, first appearence takes priority
    
    Source: manim
    """
    all_items = list()
    for config in configs:
        all_items += config.items()
    config = dict()
    for item in all_items:
        key, value = item
        if key not in config:
            config[key] = value
        else:
            # Combine two child configs
            if isinstance(value, dict) and isinstance(config[key], dict):
                config[key] = combine_configs(config[key], value)
    return config

def handle_config(self, kwargs, local_args={}):
    """Set up object variables based on configs
    
    Source: manim
    """
    # Get all superclass configurations
    superclasses = [self.__class__]
    configs = list()
    while len(superclasses) > 0:
        superclass = superclasses.pop()
        superclasses += superclass.__bases__
        if hasattr(superclass, "CONFIG"):
            configs.append(superclass.CONFIG)
    # Create priority order of configs
    all_configs = [kwargs, filter_locals(local_args), self.__dict__]
    all_configs += configs
    self.__dict__ = combine_configs(all_configs)

def change_kwargs(kwargs, **changes):
    """Modify an existing kwargs object"""
    result = kwargs.copy()
    for key,value in changes.items():
        result[key] = value
    return result

def is_number(val):
    """Return if a value is a number"""
    try:
        return not math.isnan(float(val))
    except:
        return False
    return True

def degtorad(angle):
    """Convert degrees to radians"""
    return angle * math.pi / 180.

def rotation_matrix(angle):
    """Compute the usual rotation matrix"""
    angle = degtorad(angle)
    return numpy.array([[math.cos(angle), -math.sin(angle)],
                      [math.sin(angle), math.cos(angle)]])

def image_from_array(data):
    """Convert a numpy array to a PIL image"""
    return PIL.Image.fromarray(numpy.uint8(data))

def to_color(col):
    """Convert different color representations to a Color object"""
    try:
        if col == None:
            return col
        if isinstance(col, Color):
            return col
        if isinstance(col, str):
            return Color(col)
        if isinstance(col, tuple) or isinstance(col, list):
            if len(col) == 3:
                return Color(rgb=col)
            if len(col) == 4:
                t = col[0]
                col = (col[1], col[2], col[3])
                if t == "hsl":
                    return Color(hsv=col)
                if t == "rgb":
                    return Color(rgb=col)
                raise ValueError("Invalid color type: {}".format(t))
            raise ValueError()
        if isinstance(col, dict):
            return Color(**col)
        raise ValueError()
    except ValueError as e:
        if len(e.args) > 0:
            raise e
        raise ValueError("Invalid color format: {}".format(col))

def validate_bounds(bounds):
    """Convert the bounds to a usable form, or error"""
    try:
        # Convert to float array
        bounds = numpy.array(bounds)
        bounds = bounds.astype(float)
        # Ensure it has 4 elements
        bounds = bounds.flatten()
        if bounds.shape != (4,):
            raise ValueError("")
        # Non-zero size?
        if bounds[0] == bounds[2] or bounds[1] == bounds[3]:
            raise ValueError("Bounds must have non-zero size")
        return bounds
    except e:
        if len(e.args) > 0:
            raise e
        raise ValueError("Bounds must be a list of 4 numbers")

def validate_points(*points):
    """Convert the points to a usable form, or error"""
    try:
        # Convert to float array
        points = numpy.array(points)
        points = points.astype(float)
        # Ensure it has the form (X,2)
        if len(points.shape) != 2 or points.shape[1] != 2:
            raise ValueError("")
        return points
    except e:
        if len(e.args) > 0:
            raise e
        raise ValueError("Points must be a list of number pairs")

def get_flat_handles(points):
    count = len(points) - 1
    dim = points.shape[1]
    if count < 1:
        return numpy.zeros((2, 0, dim))
    handles = numpy.zeros((2, count, dim))
    for i in range(count):
        handles[0, i, :] = points[i] + (points[i + 1] - points[i]) / 3.
        handles[1, i, :] = points[i + 1] + (points[i] - points[i + 1]) / 3.
    return handles

def is_path_closed(points):
    return scipy.linalg.norm(points[0] - points[-1]) <= ZERO_TOLERANCE

def get_smooth_handles(points):
    """Get handles for a smooth bezier curve spline
    
    Sources:
    https://www.particleincell.com/2012/bezier-splines/
        ~ Equations referenced
    https://github.com/3b1b/manim/blob/master/helpers.py
        ~ get_smooth_handle_points
    """
    count = len(points) - 1
    dim = points.shape[1]
    is_closed = is_path_closed(points)
    A = numpy.zeros((2 * count, 2 * count))
    B = numpy.zeros((2 * count, dim))
    # First row
    if is_closed: # Eq 2
        A[0, [-2, -1, 0, 1]] = [1, -2, 2, -1]
    else: # Eq 3
        A[0, 0:2] = [2, -1]
        B[0] = points[0]
    # Middle
    for i in range(1, count):
        j = 2 * i - 1
        # Eq 1
        A[j, j : j + 2] = [1, 1]
        B[j] = 2 * points[i]
        # Eq 2
        A[j + 1, j - 1 : j + 3] = [1, -2, 2, -1]
    # Last row
    if is_closed: # Eq 1
        A[-1,[-1, 0]] = [1, 1]
        B[-1] = 2 * points[0]
    else: # Eq 4
        A[-1, -2:] = [-1, 2]
        B[-1] = points[-1]
    # Solving: A * X = B
    if is_closed: # Solve as whole matrix
        X = scipy.linalg.solve(A, B)
    else: # Solve as banded matrix
        l, u = 2, 1
        AB = numpy.zeros((l + u + 1, 2 * count))
        AB[0, 1:] = numpy.diag(A, 1)
        AB[1] = numpy.diag(A)
        AB[2, :-1] = numpy.diag(A, -1)
        AB[3, :-2] = numpy.diag(A, -2)
        X = scipy.linalg.solve_banded((l,u), AB, B)
    # Parse results
    P1s = X[0::2]
    P2s = X[1::2]
    return numpy.array([P1s, P2s])

def calc_bezier(points, t):
    n = len(points) - 1
    result = numpy.zeros(points.shape[1])
    for i,v in enumerate(points):
        result += scipy.misc.comb(n,i) * (t**i) * ((1-t)**(n-i)) * v
    return result

def split_bezier(points, a, b):
    """Split a bezier curve for [a, b]
    
    Sources:
    https://pomax.github.io/bezierinfo/#splitting
    https://github.com/3b1b/manim/blob/master/helpers.py
        ~ partial_bezier_points
    """
    a_to_1 = numpy.array([
        calc_bezier(points[i:], a)
        for i in range(len(points))
    ])
    return numpy.array([
        calc_bezier(a_to_1[:i+1], (b-a)/(1.-a))
        for i in range(len(points))
    ])
