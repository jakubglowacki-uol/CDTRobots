import cv2 as cv
import datetime


class CameraController:
    def __init__(self):
        self.camera = None

    def set_camera(self, camera):
        self.camera = camera

    def recordClip(self, duration: int, filename: str):
        print("Recording clip...")
        cap = cv.VideoCapture(0)
        # Define the codec and create VideoWriter object
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter(filename, fourcc, 20.0, (640,  480))
        startTime = datetime.datetime.now()
        while (datetime.datetime.now() - startTime).seconds < duration:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            frame = cv.flip(frame, 0)
            # write the flipped frame
            out.write(frame)
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break

        cap.release()
        out.release()
        cv.destroyAllWindows()
        print("Clip recorded!")