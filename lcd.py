import urllib3
import yaml
import numpy as np
import cv2
import mouse_example7_best_one_v2
import sys
import os, time
import pyrebase
import lcddriver

##########################


################################

config = {'text_overlay': True} 

#while(cap.isOpened()):
while(True):  
    str_on_frame = "Vacant: %d Occupied: %d" % (2, 3)

	if config['text_overlay']:
		display = lcddriver.lcd()

		# # Main body of code
		try:
			while True:
				# # Remember that your sentences can only be 16 characters long!
				print("Writing to display")
				display.lcd_display_string("Greetings Human!", 1) # Write line of text to first line of display
				display.lcd_display_string("Demo Pi Guy code", 2) # Write line of text to second line of display
				time.sleep(2)                                     # Give time for the message to be read
				display.lcd_display_string("I am a display!", 1)  # Refresh the first line of display with a different message
				time.sleep(2)                                     # Give time for the message to be read
				display.lcd_clear()                               # Clear the display of any data
				time.sleep(2)                                     # Give time for the message to be read

		except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
			print("Cleaning up!")
			display.lcd_clear()
   


   
