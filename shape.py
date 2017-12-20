from copy import deepcopy

from colour import Color

import aggdraw

import helpers
import transform

class Shape(object):
    """Defines default values for other shapes"""

    CONFIG = {
        "name": None,
        "children": [],
        "stroke_color": Color("white"),
        "stroke_width": 1.,
        "stroke_alpha": 1.,
        "fill_color": None,
        "fill_alpha": 1.,
        "transform": transform.Transform.IDENTITY(),
        "parent_transform": None,
        "global_transform": None,
    }

    def __init__(self, **kwargs):
        self.name = Shape.CONFIG["name"]
        self.children = Shape.CONFIG["children"]
        self.stroke_color = Shape.CONFIG["stroke_color"]
        self.stroke_width = Shape.CONFIG["stroke_width"]
        self.stroke_alpha = Shape.CONFIG["stroke_alpha"]
        self.fill_color = Shape.CONFIG["fill_color"]
        self.fill_alpha = Shape.CONFIG["fill_alpha"]
        self.transform = Shape.CONFIG["transform"]
        self.parent_transform = Shape.CONFIG["parent_transform"]
        self.global_transform = Shape.CONFIG["global_transform"]

        self.brush = self.pen = None

        helpers.handle_config(self, kwargs)
        if self.name is None:
            self.name = self.__class__.__name__
        self.validate_children()
        self.update_transform()
        self.handle_colors()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return deepcopy(self)

    def has_loop(self, child):
        """Return if there is a reference loop"""
        if child == self:
            return True
        for subchild in child.children:
            if self.has_loop(subchild):
                return True
        return False

    def validate_child(self, child):
        """Make sure the child is valid

        Child must be a Shape object, and there can't be a reference
        loop
        """
        if not isinstance(child, Shape):
            raise ValueError("Children must be Shapes")
        if self.has_loop(child):
            raise ValueError("Shape trees can not contain loops")

    def validate_children(self):
        """Make sure the current children are valid"""
        for child in self.children:
            self.validate_child(child)
        # Remove duplicates
        self.children = reduce(lambda r, e: (r + [e]) if e not in r else r,
                               self.children, [])

    def add(self, *children):
        """Validate and add new children uniquely"""
        for child in children:
            self.validate_child(child)
            if child not in self.children:
                self.children.append(child)
        self.update_transform()

    def remove(self, *children):
        """Remove a child shape if present"""
        for child in children:
            if isinstance(child, Shape) and child in self.children:
                self.children.remove(child)

    def flatten(self):
        """Return the entire shape tree as a single array"""
        result = [self]
        for child in self.children:
            result += child.flatten()
        return result

    def handle_colors(self):
        """Ensure color properties are Color objects"""
        self.stroke_color = helpers.to_color(self.stroke_color)
        self.fill_color = helpers.to_color(self.fill_color)

    def get_pen(self):
        """Create a pen from stroke properties"""
        # No stroke?
        if (self.stroke_color is None or self.stroke_width <= 0. or
                self.stroke_alpha <= 0.):
            return None
        return aggdraw.Pen(self.stroke_color.hex_l, width=self.stroke_width,
                           opacity=int(255 * self.stroke_alpha))

    def get_brush(self):
        """Create a brush from fill properties"""
        # No fill?
        if self.fill_color is None or self.fill_alpha <= 0.:
            return None
        return aggdraw.Brush(self.fill_color.hex_l,
                             opacity=int(255 * self.fill_alpha))

    def update_transform(self, parent_transform=False):
        """Update and/or propogate parent transform

        parent_transform -- If provided (not default value of False),
                            store as instance parent_transform
        """
        if parent_transform is False:
            parent_transform = self.parent_transform
        self.parent_transform = parent_transform
        if self.transform:
            self.global_transform = self.transform.copy()
            if self.parent_transform:
                self.global_transform.merge(self.parent_transform)
        else:
            self.global_transform = self.parent_transform.copy()
        # Update children
        for child in self.children:
            child.update_transform(self.global_transform)

    def pre_draw(self, canvas):
        """Set up the transform and aggdraw objects"""
        canvas.set_transform(self.global_transform)
        self.pen = self.get_pen()
        self.brush = self.get_brush()

    def post_draw(self):
        """Clean up the aggdraw objects"""
        del self.brush
        del self.pen

    def draw_self(self, canvas, pen, brush):
        """Draw the shape to the canvas with the given pen and brush"""
        # Implemented in child classes
        pass

    def draw(self, canvas):
        """Perform drawing events and draw children"""
        self.pre_draw(canvas)
        self.draw_self(canvas, self.pen, self.brush)
        for child in self.children:
            child.draw(canvas)
