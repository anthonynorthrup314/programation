import aggdraw
import Tkinter as tk
from PIL import Image, ImageTk

from stage import Stage

def main():
	# Setup screen size
	WIDTH,HEIGHT = 640,320

	# Test the stage object
	stage = Stage()
	stage.show()
	return

	# Setup Tk
	root = tk.Tk()
	root.geometry('{}x{}'.format(WIDTH, HEIGHT))
	root.resizable(0, 0)

	# Create canvas
	canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
	canvas.pack()

	# Create image
	img = Image.new("RGB", (WIDTH, HEIGHT), "black")

	# Draw on the image
	d = aggdraw.Draw(img)
	p = aggdraw.Pen("white", 1)
	d.line((0, 0, WIDTH, HEIGHT), p)
	d.line((0, HEIGHT, WIDTH, 0), p)
	d.arc((0, 0, WIDTH, HEIGHT), 45, 135, p)
	d.flush()

	# Convert to Tk image
	imgP = ImageTk.PhotoImage(img)

	# Add image to canvas
	imgC = canvas.create_image(WIDTH / 2, HEIGHT / 2, image=imgP)

	# Display the window
	root.mainloop()

if __name__ == "__main__":
	main()
