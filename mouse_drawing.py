import cv2
import numpy as np
import yaml

CANVAS_SIZE = (600, 800)
FINAL_LINE_COLOR = (127, 0, 255) #white
WORKING_LINE_COLOR = (127, 127, 127) # gray
count = 0


class PolygonDrawer(object):
    def __init__(self, window_name):
        self.window_name = window_name
        #self.draw_frame = draw_frame
        self.done = False
        self.current = (0, 0)
        self.points = []
        self.parkpoints = []
     
    def on_mouse(self, event, x, y, buttons, user_param):
        global count
        if (self.done):
            print("d")
            self.done = False
            self.current = (0, 0)
            self.points = []
            print(self.parkpoints)
            print("e")
        if (event == cv2.EVENT_MOUSEMOVE):
            self.current = (x, y)
        elif (event == cv2.EVENT_LBUTTONDOWN):
            print ("Adding point #%d with position(%d,%d)" % (len(self.points), x, y)) #len(self.points) --> keeveni point ekada kiyala kiyanne
            self.points.append((x, y)) #join coordinates to a list
        elif (len(self.points) == 4):
            print("a")
            parking_data = {'id': '%d' % count, 'points': self.points}
            self.parkpoints.append(parking_data)
            count += 1
            #print(self.parkpoints)
            
            with open('firstprogress.yml', 'w') as outfile:
                data = yaml.safe_dump(self.parkpoints, outfile, default_flow_style=True)
                self.done = True
                print("c")
    def run(self):
        print("x")
        cv2.namedWindow(self.window_name) #must for viewing lines
        #cv2.imshow(self.window_name, np.zeros(CANVAS_SIZE, np.uint8)) #uint8 --> Unsigned integer (0 to 255)
        #cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while(not self.done):
            canvas = np.zeros(CANVAS_SIZE, np.uint8) #put frame here
            if (len(self.points) > 0):
                if (len(self.points) == 1):
                    [(x1, y1)] = (self.points).copy()
                    first_point = x1, y1
                    #(x, y) = self.points
                cv2.polylines(canvas, np.array([self.points]), False, FINAL_LINE_COLOR, 2)
                cv2.line(canvas, self.points[-1], self.current, WORKING_LINE_COLOR)
                if (len(self.points) == 4):
                    print("4th point")
                    cv2.line(canvas, self.points[-1], first_point, FINAL_LINE_COLOR, 2)
                print("f")
            cv2.imshow(self.window_name, canvas) #must 
            #if (cv2.waitKey(50) == 27):
            k1 = cv2.waitKey(1)
            if (k1 == ord('x')):
                self.done = True
                python = sys.executable
                os.execl(python, python, * sys.argv)
                cap.release()
                cv2.destroyAllWindows()
                call(["python", "my_project_v3.py"])
            elif (k1 == 26): #key for ctrl-z
                self.parkpoints.pop()
                print(self.parkpoints)
                               
        
 
if __name__ == "__main__":
    pd = PolygonDrawer("Polygon")
    image = pd.run()  
    
