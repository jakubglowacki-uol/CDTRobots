import os
from threading import Thread
from robotiq.robotiq_gripper import RobotiqGripper
import sys

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "robotiq"))

from utils.UR_Functions import URfunctions as URControl


class RobotController:
    def __init__(self, ip, port):
        self.robot = URControl(ip=ip, port=port)
        self.gripper = RobotiqGripper()
        self.gripper.connect(ip, 63352)

        self.plane = [404.87, 41.71, 560.79, 2.221, 2.221, 0]

        self.rack1_origin = [105.08, 334.24, 50.11, 2.203, -2.242, -0.051]
        self.rack0_origin = [251.75, 80.45, 50.55, 2.203, -2.242, -0.051]
        self.approach = [146.54, 167.55, 199.42, 3.055, -0.731, 0]

        self.camera_origin = [0, 0, 0, 0, 0, 0]
        self.camera_tilt = [0, 0, 0, 0, 0, 0]

    def inspect_vial(self):
        self.robot.movel_reference(self.plane, self.approach)
        self.robot.movel_reference(self.plane, self.camera_origin)
        self.robot.movel_reference(self.plane, self.camera_tilt)
        Thread.sleep(10)
        self.robot.movel_reference(self.plane, self.camera_origin)
        self.robot.movel_reference(self.plane, self.approach)
        print("Tilting complete")

    def place_vial(self, rackIndex: int, vialIndex: int):
        if rackIndex == 0:
            print("Picking from rack 0")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack0_origin[2]
            rackPosZ_lift = self.rack0_origin[2] + 50
            if vialIndex < 4:
                rackPosX = self.rack0_origin[0] + (vialIndex * 30)
                rackPosY = self.rack0_origin[1]
            elif vialIndex >= 4 and vialIndex < 8:
                rackPosX = self.rack0_origin[0] + ((vialIndex - 4) * 30)
                rackPosY = self.rack0_origin[1] + 45
            else:
                print("Invalid Vial Index!")
        elif rackIndex == 1:
            print("Picking from rack 1")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack1_origin[2]
            rackPosZ_lift = self.rack1_origin[2] + 50
            if vialIndex < 4:
                rackPosY = self.rack1_origin[1] + (vialIndex * 30)
                rackPosX = self.rack1_origin[0]
            else:
                print("Invalid Vial Index!")
        else:
            print("Invalid Rack!")

        pre_pos = [
            rackPosX,
            rackPosY,
            rackPosZ_lift,
            self.rack0_origin[3],
            self.rack0_origin[4],
            self.rack0_origin[5],
        ]
        grasp_pos = [
            rackPosX,
            rackPosY,
            rackPosZ_grasp,
            self.rack0_origin[3],
            self.rack0_origin[4],
            self.rack0_origin[5],
        ]
        self.robot.movel_reference(self.plane, self.approach)
        self.robot.movel_reference(self.plane, pre_pos)
        self.robot.movel_reference(self.plane, grasp_pos)
        self.gripper.move(255, 125, 125)
        self.robot.movel_reference(self.plane, pre_pos)
        self.robot.movel_reference(self.plane, self.approach)
        print("Placing complete")

    def pick_vial(self, rackIndex: int, vialIndex: int):
        if rackIndex == 0:
            print("Picking from rack 0")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack0_origin[2]
            rackPosZ_lift = self.rack0_origin[2] + 50
            if vialIndex < 4:
                rackPosX = self.rack0_origin[0] + (vialIndex * 30)
                rackPosY = self.rack0_origin[1]
            elif vialIndex >= 4 and vialIndex < 8:
                rackPosX = self.rack0_origin[0] + ((vialIndex - 4) * 30)
                rackPosY = self.rack0_origin[1] + 45
            else:
                print("Invalid Vial Index!")
        elif rackIndex == 1:
            print("Picking from rack 1")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack1_origin[2]
            rackPosZ_lift = self.rack1_origin[2] + 50
            if vialIndex < 4:
                rackPosY = self.rack1_origin[1] + (vialIndex * 30)
                rackPosX = self.rack1_origin[0]
            else:
                print("Invalid Vial Index!")
        else:
            print("Invalid Rack!")

        pre_pos = [
            rackPosX,
            rackPosY,
            rackPosZ_lift,
            self.rack0_origin[3],
            self.rack0_origin[4],
            self.rack0_origin[5],
        ]
        grasp_pos = [
            rackPosX,
            rackPosY,
            rackPosZ_grasp,
            self.rack0_origin[3],
            self.rack0_origin[4],
            self.rack0_origin[5],
        ]
        self.robot.movel_reference(self.plane, self.approach)
        self.gripper.move(255, 125, 125)
        self.robot.movel_reference(self.plane, pre_pos)
        self.robot.movel_reference(self.plane, grasp_pos)
        self.gripper.move(100, 125, 125)
        self.robot.movel_reference(self.plane, pre_pos)
        self.robot.movel_reference(self.plane, self.approach)
        print("Picking complete")
