# Add the directory containing robotiq_preamble.py to the Python search path
from time import sleep
from robotiq.robotiq_gripper import RobotiqGripper
from utils.UR_Functions import URfunctions as URControl

# Class to control the robot and gripper
# The robot is controlled using the URControl class
# The gripper is controlled using the RobotiqGripper class


class RobotController:
    def __init__(self, ip: str, port: int):
        # Initialize the robot and gripper
        self.robot = URControl(ip=ip, port=port)
        self.gripper = RobotiqGripper()
        self.gripper.connect(ip, 63352)

        # Define all the cartesian positions used in the task
        # (mm,mm,mm,rad,rad,rad) (X,Y,Z,Rx,Ry,Rz)
        self.plane = [
            -224.46,
            -271.21,
            7.61,
            0.028,
            0.048,
            4.749,
        ]  # The base calibration plane

        # Origin positions for both racks
        self.rack1_origin = [94.8, 350, 50, 2.22, -2.223, -0.00]
        self.rack0_origin = [273.41, 57.5, 50, 2.220, -2.223, -0.00]

        # General pounce/approach pos
        self.approach = [146.54, 167.55, 199.42, 3.055, -0.731, 0]

        # Positions around camera
        self.camera_pre = [102.43, 15.57, 335.67, 3.040, 0.694, 0.049]
        self.camera_origin = [152.12, -103.82, 137.85, 3.141, 0.082, 0]
        self.camera_tilt = [146.01, -104.02, 135.11, 2.254, 0.091, 2.172]

    # Function to move the vial to the pre-tilt position
    def pre_tilt_vial(self):
        self.robot.movel_reference(self.plane, self.approach)
        self.robot.movel_reference(self.plane, self.camera_pre)
        self.robot.movel_reference(self.plane, self.camera_origin)
        print("Pre-tilting complete")

    # Function to tilt the vial
    def tilt_vial(self):
        self.robot.movel_reference(self.plane, self.camera_tilt)
        print("Tilting complete")

    # Function to untilt the vial and return to the approach position
    def untilt_vial(self):
        self.robot.movel_reference(self.plane, self.camera_origin)
        self.robot.movel_reference(self.plane, self.camera_pre)
        self.robot.movel_reference(self.plane, self.approach)
        print("Untilting complete")

    # Function to place a vial in a rack
    # rackIndex: 0 or 1
    # vialIndex: 0-7 for rack 0, 0-3 for rack 1
    def place_vial(self, rackIndex: int, vialIndex: int):
        if rackIndex == 0:
            print("placing in rack 0")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack0_origin[2]
            rackPosZ_lift = self.rack0_origin[2] + 80
            if vialIndex < 4:
                rackPosX = self.rack0_origin[0] + (vialIndex * 26.6)
                rackPosY = self.rack0_origin[1]
            elif vialIndex >= 4 and vialIndex < 8:
                rackPosX = self.rack0_origin[0] + ((vialIndex - 4) * 26.6)
                rackPosY = self.rack0_origin[1] + 45
            else:
                print("Invalid Vial Index!")
        elif rackIndex == 1:
            print("placng in rack 1")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack1_origin[2]
            rackPosZ_lift = self.rack1_origin[2] + 80
            if vialIndex < 4:
                rackPosX = self.rack1_origin[0] + (vialIndex * 26.6)
                rackPosY = self.rack1_origin[1]
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
        self.gripper.move(80, 125, 125)
        self.robot.movel_reference(self.plane, pre_pos)
        self.robot.movel_reference(self.plane, self.approach)
        print("Placing complete")

    # Function to pick a vial from a rack
    # rackIndex: 0 or 1
    # vialIndex: 0-7 for rack 0, 0-3 for rack 1
    def pick_vial(self, rackIndex: int, vialIndex: int):
        if rackIndex == 0:
            print("Picking from rack 0")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack0_origin[2]
            rackPosZ_lift = self.rack0_origin[2] + 80
            if vialIndex < 4:
                rackPosX = self.rack0_origin[0] + (vialIndex * 26.6)
                rackPosY = self.rack0_origin[1]
            elif vialIndex >= 4 and vialIndex < 8:
                rackPosX = self.rack0_origin[0] + ((vialIndex - 4) * 26.6)
                rackPosY = self.rack0_origin[1] + 45
            else:
                print("Invalid Vial Index!")
        elif rackIndex == 1:
            print("Picking from rack 1")
            rackPosX = 0
            rackPosY = 0
            rackPosZ_grasp = self.rack1_origin[2]
            rackPosZ_lift = self.rack1_origin[2] + 80
            if vialIndex < 4:
                rackPosX = self.rack1_origin[0] + (vialIndex * 26.6)
                rackPosY = self.rack1_origin[1]
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
        self.gripper.move(80, 125, 125)
        self.robot.movel_reference(self.plane, pre_pos)
        self.robot.movel_reference(self.plane, grasp_pos)
        self.gripper.move(255, 125, 125)
        self.robot.movel_reference(self.plane, pre_pos)
        self.robot.movel_reference(self.plane, self.approach)
        print("Picking complete")
