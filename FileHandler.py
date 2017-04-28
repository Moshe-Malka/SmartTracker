import base64
import threading
import time
import os
from time import gmtime, strftime

class FileHandlerThread (threading.Thread):
    def __init__(self, threadID):
        print "<FileHandlerThread> FileHandlerThread initialized"
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.running = True
        self.images_path = "C:\\Users\\User\\Desktop\\SmartTracker_prj\\images\\"
        self.out_files_path = "C:\\Users\\User\\Desktop\\SmartTracker_prj\\out\\"
        self.out_filename = "out_"
        self.file_format = ".txt"
        
    def run(self):
        print "<FileHandlerThread> FileHandlerThread running"
        while self.running:
            try:
                images_dir_list = os.listdir(self.images_path)
                out_dir_list = os.listdir(self.out_files_path)
                if( len(images_dir_list) == 1 and "done.in" not in out_dir_list):
                    print "<FileHandlerThread> image file is present in directory"
                    #file exsits in images directory
                    encoded_string = ''
                    image = self.images_path + os.listdir(self.images_path)[0]
                    #image reading
                    with open(image, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                        #outFilesArr = divided into an array.
                        #each file stores a 100 lenght string.
                        outFilesArr = self.splitStringToArray(encoded_string, 1000)
                        #check if the payloadArr is not empty.                
                    if len(outFilesArr)>0:
                        #itirate over each base64 string in the array,
                        #and send it to our broker.
                        out_dir = self.makeDir(getCurrentTimastamp())
                        for i in range(len(outFilesArr)):
                            #writing out text files 
                            with open(out_dir+
                                      self.out_filename+
                                      str(i)+
                                      self.file_format, "w") as text_file:
                                text_file.write(outFilesArr[i])
                    print "<FileHandlerThread> finished writing out files"
                    # deleting image files.
                    self.removeImagesFromFolder()
                    print "<FileHandlerThread> finished deleting image file"
                    # end of writing out files.
                    # create a file indicating the proccess is finished
                    self.createDoneFile()
                    print "<FileHandlerThread> finished creating done.in file"
                else:
                    self.removeImagesFromFolder()
                    time.sleep(1)
            except IOError :
                print "<FileHandlerThread> error listing files in: "+ self.images_path
                
    def dir_checker(self):
        try:
            dir_list = os.listdir(self.images_path)
            if(len(dir_list)>0):
                return True
            else:
                return False
        except IOError :
            print "<FileHandlerThread> error listing files in: "+self.images_path

    def createDoneFile(self):
        try:
            with open(self.out_files_path+"done.in", "w") as done_file:
                    done_file.write("done")
        except IOError :
            print "<FileHandlerThread> error creating done.in file in : " + self.out_files_path

    def removeImagesFromFolder(self):
        try:
            if(self.dir_checker()):
                d_list = os.listdir(self.images_path)
                for img_file in d_list:
                        os.remove(self.images_path+img_file)
        except IOError :
            print "<FileHandlerThread> error removeing image files from: " + self.images_path

    def splitStringToArray(self, encoded_string, n):
        return [encoded_string[i:i+n] for i in range(0, len(encoded_string), n)]

    def stop(self):
        self.running = False

    def makeDir(self, path):
        try:
            d = os.mkdir(self.out_files_path + path)
            return d
        except IOError :
            print "<FileHandlerThread> error making a directory in: " + self.out_files_path
        print "<FileHandlerThread> Created path: "+self.out_files_path + path

    def getCurrentTimastamp():
        return strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        
if __name__ == '__main__':    
    t = FileHandlerThread(1)
    t.start()            
            
    
