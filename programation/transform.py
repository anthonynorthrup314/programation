from copy import deepcopy

import numpy

import programation.helpers as helpers


class Transform(object):
    """Affine transform

    | x1 |   | a b c |   | x0 |
    | y1 | = | d e f | * | y0 |
    | 1  |   | 0 0 1 |   | 1  |

    x1 = a * x0 + b * y0 + c
    y1 = d * x0 + e * y0 + f
    """

    def __init__(self, a, b, c, d, e, f):
        # Ensure proper arguments
        for v in [a, b, c, d, e, f]:
            assert helpers.is_number(v), "Parameters must be numbers"
        # Setup matrix
        self.matrix = numpy.array([[a, b, c], [d, e, f], [0., 0., 1.]])

    def __str__(self):
        return "{{Transform: [{}, {}, {}, {}, {}, {}]}}".format(
            *self.to_array())

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Transform):
            return False
        return self.matrix == other.matrix

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        return deepcopy(self)

    def to_array(self):
        """Get in a form usable by aggdraw

        Returns: (a, b, c, d, e, f)
        """
        return self.matrix.flatten()[0:6]

    def apply(self, x, y):
        """Apply the matrix to a point"""
        point = self.matrix.dot(numpy.array([[x], [y], [1]]))
        return (point[0], point[1])

    def combine(self, other):
        """Combine two transformations (self on left)"""
        self.matrix = self.matrix.dot(other.matrix)
        return self

    def merge(self, other):
        """Combine two transformations (self on right)"""
        self.matrix = other.matrix.dot(self.matrix)
        return self

    def __mul__(self, other):
        """Apply the transformation to another transformation/point"""
        if isinstance(other, Transform):
            return Transform(*self.matrix.dot(other.matrix).flatten()[0:6])
        if isinstance(other, numpy.ndarray) and other.shape == (2,):
            return self.matrix.dot(numpy.append(other, [1]))[0:2]
        if isinstance(other, tuple) and len(other) == 2:
            return self.apply(*other)
        raise TypeError("Unsupported type")

    @staticmethod
    def IDENTITY():
        """Create an Identity transformation"""
        return Transform(1, 0, 0, 0, 1, 0)

    @staticmethod
    def SHIFT(dx, dy):
        """Create a basic Shift transformation"""
        return Transform(1, 0, dx, 0, 1, dy)

    def set_shift(self, dx, dy):
        self.matrix[0:2, 2] = numpy.array([dx, dy])
        return self

    def shift(self, ddx, ddy):
        self.matrix[0:2, 2] += numpy.array([ddx, ddy])
        return self

    @staticmethod
    def SKEW_ABOUT(xcenter, ycenter, a, b, c, d):
        """Create a Skew transformation"""
        offset = numpy.array([[0], [0]])
        if xcenter != 0. or ycenter != 0.:
            # Compute the offset for unshift->transform->shift
            center = numpy.array([[xcenter], [ycenter]])
            offset = (numpy.identity(2, dtype=float)
                      - numpy.array([[a, b], [c, d]])).dot(center)
        return Transform(a, b, offset[0, 0], c, d, offset[1, 0])

    def skew_about(self, xcenter, ycenter, a, b, c, d):
        return self.merge(Transform.SKEW_ABOUT(xcenter, ycenter, a, b, c, d))

    @staticmethod
    def SKEW(a, b, c, d):
        """Create a basic Skew transformation"""
        return Transform.SKEW_ABOUT(0, 0, a, b, c, d)

    def set_skew(self, a, b, c, d):
        self.matrix[0:2, 0:2] = numpy.array([[a, b], [c, d]])
        return self

    def skew(self, a, b, c, d):
        return self.merge(Transform.SKEW(a, b, c, d))

    @staticmethod
    def RESIZE_ABOUT(xcenter, ycenter, xscalar, yscalar):
        """Create a Resize transformation"""
        return Transform.SKEW_ABOUT(xcenter, ycenter, xscalar, 0, 0, yscalar)

    def resize_about(self, xcenter, ycenter, xscalar, yscalar):
        return self.merge(Transform.RESIZE_ABOUT(xcenter, ycenter, xscalar,
                                                 yscalar))

    @staticmethod
    def RESIZE(xscalar, yscalar):
        """Create a basic Resize transformation"""
        return Transform.RESIZE_ABOUT(0, 0, xscalar, yscalar)

    def set_resize(self, xscalar, yscalar):
        return self.set_skew(xscalar, 0, 0, yscalar)

    def resize(self, xscalar, yscalar):
        return self.skew(xscalar, 0, 0, yscalar)

    @staticmethod
    def SCALE_ABOUT(xcenter, ycenter, scalar):
        """Create a Scale transformation"""
        return Transform.RESIZE_ABOUT(xcenter, ycenter, scalar, scalar)

    def scale_about(self, xcenter, ycenter, scalar):
        return self.merge(Transform.SCALE_ABOUT(xcenter, ycenter, scalar))

    @staticmethod
    def SCALE(scalar):
        """Create a basic Scale transformation"""
        return Transform.SCALE_ABOUT(0, 0, scalar)

    def set_scale(self, scalar):
        return self.set_resize(scalar, scalar)

    def scale(self, scalar):
        return self.resize(scalar, scalar)

    @staticmethod
    def ROTATE_ABOUT(xcenter, ycenter, angle):
        """Create a Rotation transform"""
        return Transform.SKEW_ABOUT(xcenter, ycenter,
                                    *helpers.rotation_matrix(angle).flatten())

    def rotate_about(self, xcenter, ycenter, angle):
        return self.merge(Transform.ROTATE_ABOUT(xcenter, ycenter, angle))

    @staticmethod
    def ROTATE(angle):
        """Create a basic Rotation transformation"""
        return Transform.ROTATE_ABOUT(0, 0, angle)

    def set_rotate(self, angle):
        return self.set_skew(*helpers.rotation_matrix(angle).flatten())

    def rotate(self, angle):
        return self.merge(Transform.ROTATE(angle))
