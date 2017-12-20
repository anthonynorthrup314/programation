import sys

from colour import Color

import camera
import helpers
import shapes
import transform
import vshapes

def main(render_width=helpers.DEF_WIDTH, render_height=helpers.DEF_HEIGHT,
         render_preview=False, render_file=False,
         render_filename="./files/output/test.mp4"):
    # Size
    w, h = render_width, render_height

    # Tests
    c = camera.Camera(width=w, height=h, loop_behavior="reverse")
    t = transform.Transform.IDENTITY().shift(w / 8, h / 8).rotate_about(
    	   w / 2, h / 2, 180)
    pt = transform.Transform.RESIZE_ABOUT(w / 2, h / 2, 1., .5)
    s = shapes.TestShapeChildren(width=w, height=h, stroke_color="red",
                                 stroke_width=2., fill_color=Color("green"),
                                 transform=t, parent_transform=pt)
    b1 = shapes.BezierCurve((0, 0), (0, h), (w, h), (w, 0),
                            stroke_color="#FF00FF", stroke_width=8.)
    b2 = shapes.BezierCurve((0, 0), (0, h), (w, h), (w, 0),
                            stroke_color="aqua", stroke_width=5.,
                            slice_pos=.5, close_path=True)
    b3 = shapes.BezierCurve((0, 0), (0, h), (w, h), (w, 0),
                            stroke_color=(1., 0., 0.), stroke_width=2.,
                            slice_pos=.25)
    s.add(b1, b2, b3)
    p = shapes.Polyline((w / 4, h / 4), (w / 2, 3 * h / 4), (3 * w / 4, h / 4),
                        (w / 4, h / 4), smooth=True, stroke_color="white")
    rect = vshapes.Rectangle(width=w / 4, height=h / 4, fill_color="white")
    parts = 30
    for i in range(0, parts + 1):
        f = 1. * i / parts
        f2 = 1. * (i + 1) / (parts + 1)
        b2.slice(1. * f)
        s.update_transform(transform.Transform.RESIZE_ABOUT(w / 2, h / 2,
                                                            2. * f2,
                                                            1. * f2))
        p.points[0, :] = p.points[-1, :] = [w / 2 * f2, h / 2 * f2]
        p.update_symbol()
        rect.create_points().shift((w / 8, h / 8)).subdivide(8)\
            .transform_nonlinear(helpers.wave_func, [f], expanded=True)\
            .scale(.5)
        c.capture_frame(s, p, rect)
    if render_file:
        c.write_to_file(render_filename, show_loop=True)
    if render_preview:
        c.show()

def run_main():
    # Parse arguments
    args = {}
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        nextArg = None
        if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("-"):
            nextArg = sys.argv[i + 1]
        if arg == "-p":
            args["render_preview"] = True
        elif arg == "-f":
            args["render_file"] = True
            if nextArg is not None:
                i += 1
                args["render_filename"] = nextArg
        elif arg == "-size":
            if nextArg is None:
                print "Must provide a size"
                return
            i += 1
            if "x" in nextArg:
                size = map(int, nextArg.split("x"))[:2]
            else:
                height = int(nextArg)
                size = [int(height * 16 / 9), height]
            print "Setting size to {} by {}".format(*size)
            args["render_width"] = size[0]
            args["render_height"] = size[1]
        elif arg == "-h":
            args["render_width"] = 1920
            args["render_height"] = 1080
            print "Setting size to 1080p"
        elif arg == "-m":
            args["render_width"] = 1280
            args["render_height"] = 720
            print "Setting size to 720p"
        else:
            print "Unknown parameter: {}".format(arg)
            return
        i += 1
    if not args:
        args["render_preview"] = True
    main(**args)

if __name__ == "__main__":
    run_main()
