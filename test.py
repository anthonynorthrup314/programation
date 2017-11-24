from colour import Color

from helpers import *
from canvas import *
from shapes import *
from transform import *

def main():
	# Size
	w, h = DEF_WIDTH, DEF_HEIGHT
	
	# Tests
	c = Canvas(w, h)
	t = Transform.IDENTITY().shift(w / 8, h / 8).rotate_about(w / 2, h / 2, 180)
	s = TestShapeChildren(stroke_color = "red", stroke_width = 2., fill_color = Color("green"), transform = t, parent_transform = Transform.RESIZE_ABOUT(w / 2, h / 2, 1., .5))
	for shape in s.flatten():
		print shape
	c.draw(s)
	c.show()

if __name__ == "__main__":
	main()
