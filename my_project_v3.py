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
##display = lcddriver.lcd()
##
## # Main body of code
##try:
##    while True:
##        # # Remember that your sentences can only be 16 characters long!
##        print("Writing to display")
##        display.lcd_display_string("Greetings Human!", 1) # Write line of text to first line of display
##        display.lcd_display_string("Demo Pi Guy code", 2) # Write line of text to second line of display
##        time.sleep(2)                                     # Give time for the message to be read
##        display.lcd_display_string("I am a display!", 1)  # Refresh the first line of display with a different message
##        time.sleep(2)                                     # Give time for the message to be read
##        display.lcd_clear()                               # Clear the display of any data
##        time.sleep(2)                                     # Give time for the message to be read
##
##except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
##    print("Cleaning up!")
##    display.lcd_clear()

################################

#from subprocess import call

#fn_yaml = r"../datasets/parking_test.yml"

#url="http://192.168.43.114:8080"
    
fn_yaml = r"../carparking/than.yml"
config = {'text_overlay': True,
          'lcd_display': True,
          'parking_overlay': True, 
          'text_update': True,
          'parking_detection': True,
          'park_sec_to_wait': 3} 

cap0= cv2.VideoCapture('../carparking/carparkingcam.mp4')
#ap0 = cv2.VideoCapture(url+"/video")
cap0.set(3, 640)
cap0.set(4, 480)
##address = "https://youtu.be/U7HRKjlXK-Y?t=28"
##cap0.open(address)

if (cap0.isOpened()== False): 
    print("Error opening video stream or file")
cap1 = cv2.VideoCapture(1)
with open(fn_yaml, 'r') as stream:
    parking_data = yaml.safe_load(stream)
parking_bounding_rects = []
for park in parking_data:
    points = np.array(park['points'])
    boundRect = cv2.boundingRect(points)
    parking_bounding_rects.append(boundRect)
parking_status = [False]*len(parking_data)   # len(parking_data) is 29
parking_buffer = [None]*len(parking_data) # output is 29 ("None")s
n = 0
#while(cap.isOpened()):
while(True):  
    spot = 0
    occupied = 0 
    # Read frame-by-frame
    n = n + 1

    ##imgResp = urllib.urlopen(url)
    ##imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    ##frame0 = cv2.imdecode(imgNp,-1)
    
    ret0, frame0 = cap0.read()
##    ret1, frame1 = cap1.read()
    if (ret0):
        if ret0 == False:
            print("Capture Error")
            break
        frame_out = frame0.copy()
##        lower = (50,50,50)
##        upper = (80,80,80)
##        mask = cv2.inRange(frame0, lower, upper)
##        avg_color_per_row = np.average(frame0, axis=0)
##        avg_color = np.average(avg_color_per_row,axis=0)
##        frame0[mask !=0] = avg_color
        frame_gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
##
##    if (ret1):
##        #2nd camera
##        if ret1 == False:
##            print("Capture Error")
##            break
##        frame_out = frame1.copy()
####        lower = (50,50,50)
####        upper = (80,80,80)
####        mask = cv2.inRange(frame1, lower, upper)
####        avg_color_per_row = np.average(frame1, axis=0)
####        avg_color = np.average(avg_color_per_row,axis=0)
####        frame1[mask !=0] = avg_color
##        frame_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        
    frame_blur = cv2.medianBlur(frame_gray,3)
    #frame_blur = cv2.GaussianBlur(frame_gray, (5,5), 3)
    #frame_blur = cv2.GaussianBlur(frame_blur, (9,9), 0)
    #ret2, thresh = cv2.threshold(frame_blur,95,255,cv2.THRESH_BINARY_INV)
    thresh = cv2.adaptiveThreshold(frame_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                    cv2.THRESH_BINARY_INV,11,2)
    
    #img_canny = cv2.Canny(frame_blur,50,200)
	
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    sizes = stats[1:, -1]; nb_components = nb_components - 1
    min_size = 300
    thresh2 = np.zeros((output.shape))
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            thresh2[output == i + 1] = 255
    

    if config['parking_detection']:
        for ind, park in enumerate(parking_data):
            boundRect = parking_bounding_rects[ind] # parking_bounding_rects[ind] represents tuples of bounding rect. e.g. (55, 416, 89, 60)
            roi_gray = thresh2[boundRect[1]:(boundRect[1]+boundRect[3]), boundRect[0]:(boundRect[0]+boundRect[2])] # crop roi for faster calculation
            nonzero = cv2.countNonZero(roi_gray)
            total = roi_gray.shape[0] * roi_gray.shape[1]
            ratio = nonzero * 100 / float(total)
            #print(ratio)
            status = (ratio <= 30) # True --> green cganged from 9 to 15
            #parking_buffer[ind] equals to numbers of frame count n in below when status changed, value of parking_buffer[ind] will change as n increments
            #(parking_status[ind]) equals FALSE when red i.e occupied else green (true)
            if status != parking_status[ind] and parking_buffer[ind]==None: # ind --> 0,1,2,3,... upto (points -1)
                parking_buffer[ind] = n  # when status changed, changes
                #when we put parking_buffer[ind] = n-20 fast changes occur in status
                #when status changes put current frame tested example by "parking_buffer[ind] = n+60", so after 60 frames changes occur
            # If status is still different than the one saved and counter is open
            elif status != parking_status[ind] and parking_buffer[ind]!=None:
                if n - parking_buffer[ind] > config['park_sec_to_wait']:
                    parking_status[ind] = status
                    parking_buffer[ind] = None     # when status changed these code set also runs
            # If status is still same and counter is open                    
            elif status == parking_status[ind] and parking_buffer[ind]!=None:
                parking_buffer[ind] = None
            
    if config['parking_overlay']:    
        for ind, park in enumerate(parking_data):
            points = np.array(park['points'])
            if parking_status[ind]:  #i.e TRUE then green
                color = (20,255,0) # GREEN rectangles
                spot = spot+1
            else: 
                color = (0,0,255)  #RED rectangles
                occupied = occupied+1
            cv2.drawContours(frame_out, [points], contourIdx=-1, #1st argument is, source image, 2nd contours to be passed as python list, 3rd index of contours (pass -1 to draw all contours, color, thickness ...)
                            color=color, thickness=2, lineType=cv2.LINE_8)            
            moments = cv2.moments(points)        
            centroid = (int(moments['m10']/moments['m00'])-3, int(moments['m01']/moments['m00'])+3)
            cv2.putText(frame_out, str(park['id']), (centroid[0]+1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame_out, str(park['id']), (centroid[0]-1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame_out, str(park['id']), (centroid[0]+1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame_out, str(park['id']), (centroid[0]-1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame_out, str(park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)

    # Draw Overlay
    if config['text_overlay']:
        cv2.rectangle(frame_out, (1, 5), (240, 15),(255,0,0), 85) 
        cv2.rectangle(frame_out, (6, 10), (238, 13),(255,127,0), 83)
        cv2.rectangle(frame_out, (6, 10), (235, 10),(255,255,255), 80)
        #str_on_frame = "Vacant: %d Occupied: %d" % (spot, occupied)

    if config['lcd_display']:
        str_on_frame = "Vacant: %d" % (spot)
        str_on_frame2 = "Occupied: %d" % (occupied)
		# Load the driver and set it to "display"
		# If you use something from the driver library use the "display." prefix first
        display = lcddriver.lcd()

		# Main body of code
        try:
            while True:
				# Remember that your sentences can only be 16 characters long!
                print("Writing to display")
                display.lcd_display_string(str_on_frame, 1) # Write line of text to first line of display
                display.lcd_display_string(str_on_frame2, 2) # Write line of text to second line of display
                time.sleep(2)                                     # Give time for the message to be read
                display.lcd_display_string(str_on_frame, 1) # Write line of text to first line of display  # Refresh the first line of display with a different message
                display.lcd_display_string(str_on_frame2, 2)
                time.sleep(2)                                     # Give time for the message to be read
                display.lcd_clear()
                time.sleep(2)                                     # Give time for the message to be read

        except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
            print("Cleaning up!")
            display.lcd_clear()
        
        
        cv2.putText(frame_out, str_on_frame, (5,30), cv2.FONT_HERSHEY_SIMPLEX, #3RD IS BOTTOM-LEFT CORNER OF THE TEXT
                            0.7, (0,0,0), 2, cv2.LINE_AA)
    if config['text_update']:
        config2 = {
            "apiKey": "AIzaSyA756NiKXSu-bsreoTqgmRP3KDsEK82DrY",
            "authDomain": "test-bbd8b.firebaseapp.com",
            "databaseURL": "https://test-bbd8b.firebaseio.com",
            "projectId": "test-bbd8b",
            "storageBucket": "test-bbd8b.appspot.com",
            "messagingSenderId": "465651733402"
        }
        firebase = pyrebase.initialize_app(config2)
        db = firebase.database()
        db.child("carparking").child("car").update({"Occupied":"%d" % (occupied)})
        db.child("carparking").child("car").update({"Vacant":"%d" % (spot)})
        
        storage = firebase.storage()
        path_on_cloud = "images/foo.jpg"
        path_local = "my_image.jpg"
        storage.child(path_on_cloud).put(path_local)
        #storage.child(path_on_cloud).download("test_download.jpg")
    # Display video
    cv2.imshow('Parking spot detection', frame_out)
    #cv2.imshow('canny', img_canny)
    #cv2.imshow('thresh', thresh)
    #cv2.imshow('thresh2', thresh2)
    #cv2.imshow('blur', frame_blur)
    #cv2.imshow('gray', frame_gray)

    cv2.imwrite("my_image.jpg", frame_out)
    
    k = cv2.waitKey(1)
    if (k == ord('q')):
        break
    elif (k == ord('c')):
        pd0 = mouse_example7_best_one_v2.PolygonDrawer("Parking Spot Detection", frame0)
        #pd1 = mouse_example7_best_one_v2.PolygonDrawer("Parking Spot Detection", frame1)
        pd0.run()
        #pd1.run()
        cap.release()
        cv2.destroyAllWindows()
        #os.execl(sys.executable, sys.executable, *sys.argv)
        while (1):
            os.system("python my_project_v3.py")
            time.sleep(0.1)
        quit()
        #call(["python", "my_project_v3.py"])
        #with open('than.yml', 'w') as outfile:
         #   yaml.dump(parking_data, outfile, default_flow_style=False)
    elif (k == 27):
        cap0.release()
        cap1.release()
        cv2.destroyAllWindows()    
