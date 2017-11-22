from colour import Color

from helpers import *
from canvas import *
from shape import *
from transform import *

def main():
	# Size
	w, h = DEF_WIDTH, DEF_HEIGHT
	
	# Tests
	c = Canvas(w, h)
	t = Transform.ROTATE_ABOUT(w / 2, h / 2, math.pi)
	s = Shape(stroke_color = Color("red"), stroke_width = 2., fill_color = Color("green"), transform = t)
	c.draw(s)
	c.show()

if __name__ == "__main__":
	main()
