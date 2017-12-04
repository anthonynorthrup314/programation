import math

from colour import Color
import numpy as np
from PIL import Image
import Tkinter as tk

# Some helpers copied from 3B1B's Manim project
# https://github.com/3b1b/manim

# Constants
DEF_WIDTH = 640
DEF_HEIGHT = 480
DEF_FPS = 30

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
    return np.array([[math.cos(angle), -math.sin(angle)],
                      [math.sin(angle), math.cos(angle)]])

def image_from_array(data):
    """Convert a numpy array to a PIL image"""
    return Image.fromarray(np.uint8(data))

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
        bounds = np.array(bounds)
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

def slice_curve(t, p0, p1, p2, p3):
    """Returns a bezier curve holding [0, t] of the original
    
    t -- Location to cut, 0 < t <= 1
    """
    M = np.array([[1., 0., 0., 0.], [-3., 3., 0., 0.], [3., -6., 3., 0.],
                   [-1., 3., -3., 1.]])
    c = 1. * t
    C = np.array([[1., 0., 0., 0.], [0., c, 0., 0.], [0., 0., c**2, 0.],
                   [0., 0., 0., c**3]])
    Q = np.linalg.inv(M).dot(C).dot(M)
    return Q.dot(np.array([p0, p1, p2, p3]))

def mod_positive(a, b):
    """Return a positive mod"""
    return ((a % b) + b) % b

def get_third_vector(p0, p1, factor=None):
    """Get the vector: factor * (p1 - p0)"""
    if not factor:
        factor = 1. / 3.
    return (p1 - p0) * float(factor)

def get_third(p0, p1, factor=None):
    """Get the vector: p0 + factor * (p1 - p0)"""
    return (p0 + get_third_vector(p0, p1, factor))

def get_flat_handles(p0, p1, p2, factor=None):
    """Get the control points around p1
    
    factor -- Passed to get_third method
    """
    return np.array([get_third(p1, p0, factor), get_third(p1, p2, factor)])

def get_smooth_handles(p0, p1, p2, factor=None):
    """Get the control points around p1
    
    factor -- Passed to get_third method
    """
    third = get_third_vector(p0, p2, factor)
    return np.array([p1 - third, p1 + third])

def validate_points(*points):
    """Convert the points to a usable form, or error"""
    try:
        # Convert to float array
        points = np.array(points)
        points = points.astype(float)
        # Ensure it has the form (X,2)
        if len(points.shape) != 2 or points.shape[1] != 2:
            raise ValueError("")
        return points
    except e:
        if len(e.args) > 0:
            raise e
        raise ValueError("Points must be a list of number pairs")
