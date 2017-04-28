import paho.mqtt.publish as pub
import threading
import os
import time

class MessagingThread (threading.Thread):
    def __init__(self, threadID):
        print "<MessagingThread> MessagingThread initialized"
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.running = True
        self.topic = "/sender/image/"# need to listen on /sender/image/# topic   
        self.hostname = "test.mosquitto.org"
        self.port = 1883
        self.qos = 0
        self.out_files_path = "C:\\Users\\User\\Desktop\\SmartTracker_prj\\out\\"

    def run(self):
        print "<MessagingThread> MessagingThread running"
        #run
        while self.running:
            if(len(os.listdir(self.out_files_path))==1):
                out_dir = self.dir_listing()
                if ("done.in" in out_dir):
                    numbers = self.getFilesNumbering(out_dir)
                    index = 0
                    # itirate over files in the directory
                    for text_file in os.listdir(out_dir):
                        #read each file
                        if(text_file != "done.in"):
                            with open(out_dir + '\\' + text_file , "r") as f:                        
                                #send file content
                                self.pubMsg(self.topic+str(numbers[index]), f.read(), self.hostname, self.port, self.qos )
                                time.sleep(2)
                        index += 1
                else:              
                    print "<MessagingThread> no files in the directory: "+out_dir
                    break
                #delete all files (including done.in)
                print "<MessagingThread> deleting all files in out directory"
                self.deleteOutFiles()

    def pubMsg(self,topic, payload, hostname, port, qos):
        pub.single(topic=topic, payload=payload,
                   hostname=hostname, port=port, qos=qos)        
        print "topic = "+topic
        print "payload = "+payload[0:10]+"..."
        print "hostname = "+hostname
        print "port = "+str(port)
        print "qos = "+str(qos)
        print "<MessagingThread> Message Sent" 

    def deleteOutFiles(self):
        try:
            out_dir = os.listdir(self.dir_listing())
            #delete all files in out directory
            for t_file in out_dir:
                os.remove(out_dir+t_file)
        except IOError:
            print("<MessagingThread> Error trying to delete the out files.")
            
    def getFilesNumbering(self, out_dir):
        try:            
            numbers = []
            if(len(os.listdir(out_dir))>0):
                for f in os.listdir(out_dir):
                    if (f != "done.in"):
                        filename = f.split(".")[0]
                        number = filename.split("_")[1]
                        numbers.append(number)
            return numbers
        except IndexError :
            print "<MessagingThread> IndexError: list index out of range."

    def dir_listing(self):
        try:
            return self.out_files_path + os.listdir(self.out_files_path)[0]
        except IndexError :
            print "<MessagingThread> error listing files in: "+self.out_files_path

    def stop(self):
        self.running = False
        
if __name__ == '__main__':    
    t = MessagingThread(1)
    t.start()        
