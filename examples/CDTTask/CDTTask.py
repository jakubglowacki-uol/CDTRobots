import RobotController as rc

robotController = rc("192.168.0.2", 30002)
robotController.pick_vial(0, 0)
robotController.inspect_vial()
robotController.place_vial(1, 0)