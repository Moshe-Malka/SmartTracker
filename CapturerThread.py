import cv2
import threading

class CapturerThread(threading.Thread):
    def __init__(self,threadID):
        print "<CapturerThread> CapturerThread initialized"
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.running = False
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.file_path = "C:\\Users\\User\\Desktop\\SmartTracker_prj\\images\\"
        self.capture_index = 0
        self.filename = "out_"
        self.format = ".jpg"
        self.frameRate = 1000
        
    def start(self):
        self.running = True
        super(CapturerThread, self).start()
        
    def run(self):
        print "<CapturerThread> CapturerThread running"
        cap = cv2.VideoCapture(0)
        while self.running:
            _, frame = cap.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = self.face_cascade.detectMultiScale(gray, 1.3, 5)    

            #len(face) => 1 or 0
            if len(face)>0:
                #print '<CapturerThread> found intruder ! ('+str(self.capture_index)+')'
                self.capture_index += 1
                # save every 1000'th frame. 
                if self.capture_index % self.frameRate == 1:
                    #save a file only if the directory is empty
                    if(len(os.listdir(self.file_path))==0):
                        print '<CapturerThread> saved image to directory ('+str(self.capture_index)+')'
                        #save frame to jpeg file.
                        cv2.imwrite(self.file_path+self.filename+
                                    str(self.capture_index)+self.format, frame)

            for (x,y,w,h) in face:
                
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 255), 2)

                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)

            # delete after finishing code...
            cv2.imshow('SmartTracker', frame)

            # need to delete after compleation
            k = cv2.waitKey(1)
            #Esc to stop
            if k== 27:
                self.running = False
                break
        print "<CapturerThread> user hit Esc - exiting CapturerThread " 
        cv2.destroyAllWindows()
        cap.release()

    def stop(self):
        self.running = False
        
if __name__ == '__main__':    
    t = CapturerThread(1)
    t.start()
