import math
from transform import *

w, h = 640, 480

print Transform.IDENTITY()
print Transform.IDENTITY().shift(w / 4, 0)
print Transform.IDENTITY().shift(w / 4, 0).rotate_about(w / 2, h / 2, math.pi)
