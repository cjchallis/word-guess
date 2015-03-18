import textwrap
from scene import text, tint

def text_lines(txt, fnt, w, x, y, size1):
		lines = textwrap.wrap(txt, w)
		i = 0
		size = size1
		for l in lines:
			text(l, fnt, size, x, y + size * ((len(lines)-1.0)/2.0 - i))
			i += 1

def change_color(col):
	tint(col.r, col.g, col.b)
