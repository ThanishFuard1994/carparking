import mouse_example7_best_one_v2
import sys
import os, time
#import pyrebase
import lcddriver

config = {'text_overlay': True} 
            

    # Draw Overlay
    if config['text_overlay']:
        
        str_on_frame = "Vacant: %d Occupied: %d" % (2, 3)




		display = lcddriver.lcd()

		# # Main body of code
		try:
			while True:
				# # Remember that your sentences can only be 16 characters long!
				print("Writing to display")
				display.lcd_display_string(str_on_frame, 1) # Write line of text to first line of display
				display.lcd_display_string("Demo Pi Guy code", 2) # Write line of text to second line of display
				time.sleep(2)                                     # Give time for the message to be read
				display.lcd_display_string("I am a display!", 1)  # Refresh the first line of display with a different message
				time.sleep(2)                                     # Give time for the message to be read
				display.lcd_clear()                               # Clear the display of any data
				time.sleep(2)                                     # Give time for the message to be read

		except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
			print("Cleaning up!")
			display.lcd_clear()
        
        
        cv2.putText(frame_out, str_on_frame, (5,30), cv2.FONT_HERSHEY_SIMPLEX, #3RD IS BOTTOM-LEFT CORNER OF THE TEXT
                            0.7, (0,0,0), 2, cv2.LINE_AA)
   
