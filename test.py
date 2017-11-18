import aggdraw, PIL, Tkinter
from PIL import Image, ImageTk

# Setup screen size
WIDTH,HEIGHT = 640,320

# Setup Tk
root = Tkinter.Tk()
root.geometry('{}x{}'.format(WIDTH, HEIGHT))
root.resizable(0, 0)

# Create canvas
canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Create image
img = PIL.Image.new("RGB", (WIDTH, HEIGHT), "black")

# Draw on the image
d = aggdraw.Draw(img)
p = aggdraw.Pen("white", 1)
d.line((0, 0, WIDTH, HEIGHT), p)
d.line((0, HEIGHT, WIDTH, 0), p)
d.arc((0, 0, WIDTH, HEIGHT), 45, 135, p)
d.flush()

# Convert to Tk image
imgP = PIL.ImageTk.PhotoImage(img)

# Add image to canvas
imgC = canvas.create_image(WIDTH / 2, HEIGHT / 2, image=imgP)

# Display the window
root.mainloop()
