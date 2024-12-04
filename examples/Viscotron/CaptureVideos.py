from threading import Thread
from time import sleep
import RobotController as rc
import CameraController as cc

def recordVid():
    cameraController.recordClip(37, "Viscous_S3.avi")

robotController = rc.RobotController("192.168.0.2", 30002)
cameraController = cc.CameraController()
robotController.pick_vial(0, 0)
robotController.pre_tilt_vial()
thread = Thread(target = recordVid, args = ())
thread.start()
sleep(10)
robotController.tilt_vial()
sleep(25)
robotController.untilt_vial()
robotController.place_vial(1, 0)




