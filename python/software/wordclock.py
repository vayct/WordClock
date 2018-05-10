#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import math
import socket
from datetime import datetime
from string import digits

continuum = 0
rotation = 0

# Constants
MATRIX_W      = 32 # Number of Actual X Pixels
MATRIX_H      = 32 # Number of Actual Y Pixels
MATRIX_DEPTH  = 3  # Color Depth (RGB=3)
MATRIX_DIV    = 2  # Physical Matrix is Half of Pixel Matrix

# Colors
RED     = [255, 0,   0  ]
LIME    = [0,   255, 0  ]
BLUE    = [0,   0,   255]
YELLOW  = [255, 255, 0  ]
FUCHSIA = [255, 0,   255]
AQUA    = [0,   255, 255]
WHITE   = [255, 255, 255]

# Birthday
BIRTH_MONTH = 8
BIRTH_DAY = 29

#Color Fade Order (for Leah <3)
FADE_COLORS = [LIME, YELLOW, RED, FUCHSIA, BLUE, AQUA]



the1       =  [  0,  0,  3  ]
time1      =  [  0,  4,  4  ]
is1        =  [  0,  9,  2  ]
half       =  [  0, 12,  4  ]
a          =  [  0, 13,  1  ]
quarter    =  [  1,  0,  7  ]
twenty     =  [  1,  7,  6  ]
ten1       =  [  2,  0,  3  ]
six1       =  [  2,  3,  3  ]
sixteen    =  [  2,  3,  7  ]
two1       =  [  2, 10,  3  ]
one1       =  [  2, 12,  3  ]
eight1     =  [  3,  0,  5  ]
eighteen   =  [  3,  0,  8  ]
five1      =  [  3,  8,  4  ]
seven1     =  [  4,  0,  5  ]
seventeen  =  [  4,  0,  9  ]
nine1      =  [  4,  8,  4  ]
nineteen   =  [  4,  8,  8  ]
four1      =  [  5,  0,  4  ]
fourteen   =  [  5,  0,  8  ]
thirteen   =  [  5,  8,  8  ]
twelve1    =  [  6,  0,  6  ]
eleven1    =  [  6,  5,  6  ]
three1     =  [  6, 11,  5  ]
minute_    =  [  7,  0,  6  ]
minutes    =  [  7,  0,  7  ]
past       =  [  7,  8,  4  ]  
to         =  [  7, 11,  2  ]
two2       =  [  8,  0,  3  ]
one2       =  [  8,  2,  3  ]
eleven2    =  [  8,  6,  6  ]
nine2      =  [  8,  9,  4  ]
six2       =  [  8, 13,  3  ]
seven2     =  [  9,  0,  5  ]
three2     =  [  9,  5,  5  ]
twelve2    =  [  9, 10,  6  ]
four2      =  [ 10,  0,  4  ]
five2      =  [ 10,  5,  4  ]
eight2     =  [ 10,  8,  5  ]
ten2       =  [ 10, 12,  3  ]
end        =  [ 10, 13,  3  ]
oclock     =  [ 11,  0,  6  ]
in2 	   =  [ 11,  7,  2, ]
at         =  [ 11,  9,  2  ]
year       =  [ 11, 12,  4  ]
night      =  [ 12,  0,  5  ]
the2       =  [ 12,  4,  3  ]
morning    =  [ 12,  8,  7  ]
evening    =  [ 13,  0,  7  ]
afternoon  =  [ 13,  7,  9  ]
timezone   =  [ 14,  0,  8  ]
pm         =  [ 14,  0,  2  ]
zero_1     =  [ 15,  0,  1  ]
one_1      =  [ 15,  1,  1  ]
two_1      =  [ 15,  2,  1  ]
three_1    =  [ 15,  3,  1  ]
four_1     =  [ 15,  4,  1  ]
five_1     =  [ 15,  5,  1  ]
zero_2     =  [ 15,  6,  1  ]
one_2      =  [ 15,  7,  1  ]
two_2      =  [ 15,  8,  1  ]
three_2    =  [ 15,  9,  1  ]
four_2     =  [ 15, 10,  1  ]
five_2     =  [ 15, 11,  1  ]
six_2      =  [ 15, 12,  1  ]
seven_2    =  [ 15, 13,  1  ]
eight_2    =  [ 15, 14,  1  ]
nine_2     =  [ 15, 15,  1  ]


PST = [ [14,9,1] , [14,13,1] , [14,15,1] ]
PDT = [ [14,9,1] , [14,14,1] , [14,15,1] ]
MST = [ [14,10,1], [14,13,1] , [14,15,1] ]
MDT = [ [14,10,1], [14,14,1] , [14,15,1] ]
CST = [ [14,11,1], [14,13,1] , [14,15,1] ]
CDT = [ [14,11,1], [14,14,1] , [14,15,1] ]
EST = [ [14,12,1], [14,13,1] , [14,15,1] ]
EDT = [ [14,12,1], [14,14,1] , [14,15,1] ]

TZ_SET = [PST, PDT, MST, MDT, CST, CDT, EST, EDT]
TZ_WORDS = [ 'PST', 'PDT', 'MST', 'MDT', 'CST', 'CDT', 'EST', 'EDT' ]

#Will be used for indexing time in second to these 2 list, so there is no need for 60 if/else statements
TEN_SECOND = [zero_1, one_1, two_1, three_1, four_1, five_1]
SINGLE_SECOND = [zero_2, one_2, two_2, three_2, four_2, five_2, six_2, seven_2, eight_2, nine_2]




#Generate the appropriate word list, given a datetime object
def getTime(t=None):
    if t is None:
	    t=datetime.now()
    
    hour = t.hour
    minute = t.minute
    second = t.second

    #the word list that will be returned at the end
    words = []

    #All the words combination will contain the words "The time is"
    words += [the1, time1, is1]

    #From 1-30 minutes, words will count from the current hour
    #From 31-59, words will point to the next hour
    if minute > 30:
	    words += [to]
	    minute = 60 - minute
	    hour +=1
	    if hour == 24:
		    hour = 0
    elif  minute != 0:
	    words += [past]



    #Add "minutes" word to clock, unless it is multiple of 5
    if (minute%5 != 0) and (minute != 1):
	    words += [minutes]

    if minute == 0:
	words += [oclock]
    elif minute == 1:
    	words += [one1, minute_]
    elif minute == 2:
        words += [two1]
    elif minute == 3:
    	words += [three1]
    elif minute == 4:
    	words += [four1]
    elif minute == 5:
    	words += [five1]
    elif minute == 6:
    	words += [six1]
    elif minute == 7:
    	words += [seven1]
    elif minute == 8:
    	words += [eight1]
    elif minute == 9:
    	words += [nine1]
    elif minute == 10:
    	words += [ten1]
    elif minute == 11:
    	words += [eleven1]
    elif minute == 12:
    	words += [twelve1]
    elif minute == 13:
    	words += [thirteen]
    elif minute == 14:
    	words += [fourteen]
    elif minute == 15:
    	words += [a, quarter]
    elif minute == 16:
    	words += [sixteen]
    elif minute == 17:
    	words += [seventeen]
    elif minute == 18:
    	words += [eighteen]
    elif minute == 19:
    	words += [nineteen]
    elif minute == 20:
    	words += [twenty]
    elif minute == 21:
    	words += [twenty, one1]
    elif minute == 22:
    	words += [twenty, two1]
    elif minute == 23:
    	words += [twenty, three1]
    elif minute == 24:
    	words += [twenty, four1]
    elif minute == 25:
    	words += [twenty, five1]
    elif minute == 26:
    	words += [twenty, six1]
    elif minute == 27:
    	words += [twenty, seven1]
    elif minute == 28:
    	words += [twenty, eight1]
    elif minute == 29:
    	words += [twenty, nine1]
    elif minute == 30:
    	words += [half]


    if hour == 0:
	words += [twelve2, at, night]
    if hour == 1:
	words += [one2, in2, the2, morning]
    if hour == 2: 
	words += [two2, in2, the2, morning]
    if hour == 3:
	words += [three2, in2, the2, morning]
    if hour == 4:
	words += [four2, in2, the2, morning]
    if hour == 5:
	words += [five2, in2, the2, morning]
    if hour == 6:
	words += [six2, in2, the2, morning]
    if hour == 7:
	words += [seven2, in2, the2, morning]
    if hour == 8:
	words += [eight2, in2, the2, morning]
    if hour == 9:
	words += [nine2, in2, the2, morning]
    if hour == 10:
	words += [ten2, in2, the2, morning]
    if hour == 11:
	words += [eleven2, in2, the2, morning]
    if hour == 12:
	words += [twelve2, in2, the2, afternoon]
    if hour == 13:
	words += [one2, in2, the2, afternoon]
    if hour == 14:
	words += [two2, in2, the2, afternoon]
    if hour == 15:
	words += [three2, in2, the2, afternoon]
    if hour == 16:
	words += [four2, in2, the2, afternoon]
    if hour == 17:
	words += [five2, in2, the2, afternoon]
    if hour == 18:
	words += [six2, in2, the2, afternoon]
    if hour == 19:
	words += [seven2, in2, the2, afternoon]
    if hour == 20:
	words += [eight2, at, night]
    if hour == 21:
	words += [nine2, at, night]
    if hour == 22:
	words += [ten2, at, night]
    if hour == 23:
	words += [eleven2, at, night]


    #Add second words based on the the array index
    div10_sec = second/10
    mod10_sec = second%10
    words += [ TEN_SECOND[div10_sec], SINGLE_SECOND[mod10_sec] ]

    return words





#The class for matching the time to correct LED position and light up the LED
#Extending from SampleBase provides command-line parsing for setting up LED
#configuration if needed
class WordClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(WordClock, self).__init__(*args, **kwargs)

    
    #Rotate (x,y) point by some degree angle
    #Part of the rotatingBlockMode()
    def rotate(self, x, y, angle):
        return {
            "new_x": x * math.cos(angle) - y * math.sin(angle),
            "new_y": x * math.sin(angle) + y * math.cos(angle)
        }

    #Part of the rotatingBlockMode() for switching colors and make sure colors
    #are not out of bound
    def scale_col(self, val, lo, hi):
        if val < lo:
            return 0
        if val > hi:
            return 255
        return 255 * (val - lo) / (hi - lo)

    #Color Mode#1 of the RGBMatrix, will rotate rgb color around the center slowly
    #From hzeller / rpi-rgb-led-matrix sample library
    def rotatingBlockMode(self, coord):
    	global rotation
        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        display_square = min(self.matrix.width, self.matrix.height) * 2
        min_display = cent_x - display_square / 2
        max_display = cent_x + display_square / 2

        deg_to_rad = 2 * 3.14159265 / 360

        rotation += 1
	rotation %= 360

	for x in range(int(min_rotate), int(max_rotate)):
		for y in range(int(min_rotate), int(max_rotate)):
		    ret = self.rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
		    rot_x = ret["new_x"]
		    rot_y = ret["new_y"]

		    if x >= min_display and x < max_display and y >= min_display and y < max_display:


			trunc_x = math.trunc(rot_x + cent_x)
			trunc_y = math.trunc(rot_y + cent_y)
			test = (trunc_y, trunc_x)
			if test in coord:
				self.canvas.SetPixel(trunc_x, trunc_y, self.scale_col(x, min_display, max_display), 255 - self.scale_col(y, min_display, max_display), self.scale_col(y, min_display, max_display))
			else:
				self.canvas.SetPixel(trunc_x, trunc_y,0,0,0)
		    else:
			self.canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

	self.canvas = self.matrix.SwapOnVSync(self.canvas)

    
    #Color Mode#2 of the RGBMatrix, will pulse color from red -> green -> blue
    #From hzeller / rpi-rgb-led-matrix sample library
    #coord: Array of [(x,y)] coordinates to set the color of
    def pulsingColorsMode(self, coord):
	    global continuum
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

            #self.canvas.Fill(red, green, blue)
	    for x in range(32):
		    for y in range(32):
			    if (x,y) in coord:
				    self.matrix.SetPixel(y,x,red,green,blue)
			    else:
				    self.matrix.SetPixel(y,x,0,0,0)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
	    


    #Write scrolling text to the rgb matrix
    #From hzeller / rpi-rgb-led-matrix sample library
    #text: the text to write
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
		break
            time.sleep(0.03)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
	    counter +=1

    #Get the words for TIMEZONE
    def getTimeZone(self):
    	t = time.tzname[time.daylight]

	for i in range(len(TZ_WORDS)):
		if TZ_WORDS[i] == t:
			words = [timezone]
			words += TZ_SET[i]
			return words
	
	return []


    
    #Set how the RGBMAtrix will display
    #primary_words: array of array of the dictionary words
    def setDisplay(self,primary_words=[], clock_mode=1):
	    
	xy = []
	for word in primary_words:
		x = word[0]
		for l in range( word[2]):
			y = word[1] + l
			xy.append((x * 2, y *2 ))
			xy.append((x * 2 + 1, y * 2))
			xy.append((x * 2, y * 2 + 1))
			xy.append((x * 2 + 1, y * 2 + 1))

	   
	if clock_mode == 1:
		self.rotatingBlockMode(xy)
	elif clock_mode == 2:
		self.pulsingColorsMode(xy) 
    
    
    
    
    #For getting the IP address of LAN, based on link:
    #https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    def get_ip(self):
    	
    	IP= ((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["No IP Found"])[0])
    	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return IP

    #For testing all the time combinations quickly
    def testTime(self):
    	for h in xrange(24):
		for m in xrange(60):
			for s in xrange(60):
				self.setDisplay( getTime( datetime(2016,01,01,h,m,s)))
			
    





    #MAIN
    #A
    #I
    #N			what will be run after all configurations are done
    def run(self, clock_mode):
	
	tz =  self.getTimeZone()	

	self.writeText(self.get_ip())
	
        print "Running the Clock."
        while True:
            t = datetime.now()
            primary_words   = getTime(t)

            self.setDisplay(primary_words + tz, clock_mode)




# Main function
if __name__ == "__main__":
    wc = WordClock()
    if (not wc.process()):
        wc.print_help()
