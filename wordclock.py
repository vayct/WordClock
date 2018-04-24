#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import math

class WordClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(WordClock, self).__init__(*args, **kwargs)


    def rotate(self, x, y, angle):
        return {
            "new_x": x * math.cos(angle) - y * math.sin(angle),
            "new_y": x * math.sin(angle) + y * math.cos(angle)
        }

    def scale_col(self, val, lo, hi):
        if val < lo:
            return 0
        if val > hi:
            return 255
        return 255 * (val - lo) / (hi - lo)

    def rotatingBlockMode(self):
        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 2
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        display_square = min(self.matrix.width, self.matrix.height) * 1
        min_display = cent_x - display_square / 2
        max_display = cent_x + display_square / 2

        deg_to_rad = 2 * 3.14159265 / 360
        rotation = 0

        while True:
            rotation += 2
            rotation %= 360

            for x in range(int(min_rotate), int(max_rotate)):
                for y in range(int(min_rotate), int(max_rotate)):
                    ret = self.rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
                    rot_x = ret["new_x"]
                    rot_y = ret["new_y"]

                    if x >= min_display and x < max_display and y >= min_display and y < max_display:
                        self.canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, self.scale_col(x, min_display, max_display), 255 - self.scale_col(y, min_display, max_display), self.scale_col(y, min_display, max_display))
                    else:
                        self.canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def pulsingColorsMode(self):
        continuum = 0

        while True:
            self.usleep(5 * 1000)
            continuum += 1
            continuum %= 3 * 255

            red = 0
            green = 0
            blue = 0

            if continuum <= 255:
                c = continuum
                blue = 255 - c
                red = c
            elif continuum > 255 and continuum <= 511:
                c = continuum - 256
                red = 255 - c
                green = c
            else:
                c = continuum - 512
                green = 255 - c
                blue = c

            self.canvas.Fill(red, green, blue)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)


    def writeText(self, text):
        font = graphics.Font()
        font.LoadFont("10x20B.bdf")
        textColor = graphics.Color(0, 0, 255)
        pos = self.canvas.width

	counter = 0
	while True:
            self.canvas.Clear()
            len = graphics.DrawText(self.canvas, font, pos, 21, textColor, text)
            pos -= 1
            if (pos + len < 0):
               pos = self.canvas.width
	       time.sleep(10)

            time.sleep(0.03)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
	    counter +=1

    def run(self):
    	#self.writeText("AAAAAAAAAAAAAAAAAAAA")
	#self.pulsingColorsMode()
	self.rotatingBlockMode()
# Main function
if __name__ == "__main__":
    wc = WordClock()
    if (not wc.process()):
        wc.print_help()
