from time import sleep
import cv2 as cv
import datetime

# CameraController class is responsible for recording video clips
# from the camera. It uses OpenCV to capture frames from the camera
# and write them to a video file.


class CameraController:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def set_camera(self, camera):
        self.camera = camera

    # Function to record a video clip from the camera
    def recordClip(self, duration: int, filename: str):
        self.cap.release()
        self.cap = cv.VideoCapture(0)
        succeeded = False
        while (not succeeded):
            try:
                print("Recording clip...")
                failures = 0
                # Define the codec and create VideoWriter object
                fourcc = cv.VideoWriter_fourcc(*'XVID')
                out = cv.VideoWriter(filename, fourcc, 20.0, (640,  480))
                startTime = datetime.datetime.now()
                while (datetime.datetime.now() - startTime).seconds < duration:
                    ret, frame = self.cap.read()
                    if not ret:
                        sleep(0.1)
                        print("Can't receive frame (stream end?)")

                    out.write(frame)
                    #cv.imshow('frame', frame)
                    if cv.waitKey(1) == ord('q'):
                        break
                self.cap.release()
                out.release()
                cv.destroyAllWindows()
                print("Clip recorded!")
                succeeded = True
            except: 
                print("CV failed, I'm sorry, trying again")
