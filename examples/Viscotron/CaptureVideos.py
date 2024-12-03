import RobotController as rc
import CameraController as cc
robotController = rc("192.168.0.2", 30002)
cameraController = cc()
robotController.pick_vial(0, 0)
#robotController.pre_tilt_vial()
#cameraController.recordClip(30, "vial0.mp4")
#robotController.tilt_vial()
#robotController.untilt_vial()
robotController.place_vial(1, 0)
