from threading import Thread
import multiprocessing
from time import sleep
import RobotController as rc
import CameraController as cc
import ViscosityClassifier as vc


class ViscotronController:
    def __init__(self, ip, port):
        self.robot = rc.RobotController(ip, port)
        self.camera = cc.CameraController()
        self.classifier = vc.ViscosityClassifier()

    def recordRawSampleData(self, noOfSamples: int):
        for i in range(noOfSamples):
            self.robot.pick_vial(0, i)
            self.robot.pre_tilt_vial()
            thread = Thread(
                target=self.camera.recordClip,
                args=(37, "Sample_" + str(i) + ".avi"),
            )
            thread.start()
            sleep(10)
            self.robot.tilt_vial()
            sleep(25)
            self.robot.untilt_vial()
            self.robot.place_vial(1, i)

    def classifyOneSample(self, sampleIndex: int):
        self.robot.pick_vial(0, sampleIndex)
        self.robot.pre_tilt_vial()
        thread = multiprocessing.Process(
            target=self.camera.recordClip,
            args=(37, "Sample_" + str(sampleIndex) + ".avi"),
        )
        thread.start()
        sleep(10)
        self.robot.tilt_vial()
        sleep(25)
        self.robot.untilt_vial()
        viscosity = self.classifier.classifyVideo(
            "Sample_" + str(sampleIndex) + ".avi"
        )
        if viscosity:
            print("Viscous Sample Detected")
        else:
            print("Non-Viscous Sample Detected")
        self.robot.place_vial(0, sampleIndex)

    def sortSamplesByViscosity(self, noOfSamples: int):
        viscIndex = 0
        for i in range(noOfSamples):
            thread = Thread(
                target=self.camera.recordClip,
                args=(37, "Sample_" + str(i) + ".avi"),
            )
            if (thread.is_alive()):
                del self.camera
                self.camera = cc.CameraController()
            self.robot.pick_vial(0, i)
            self.robot.pre_tilt_vial()
            thread.start()
            sleep(10)
            self.robot.tilt_vial()
            sleep(25)
            self.robot.untilt_vial()
            del self.classifier
            self.classifier = vc.ViscosityClassifier()
            viscosity = self.classifier.classifyVideo(
                "Sample_" + str(i) + ".avi"
            )
            if viscosity:
                print("Viscous")
                self.robot.place_vial(1, viscIndex)
                viscIndex += 1
            else:
                print("Not Viscous")
                self.robot.place_vial(0, i)
