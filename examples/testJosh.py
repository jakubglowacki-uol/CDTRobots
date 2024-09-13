import os
import time
import argparse
import math
from robotiq.robotiq_gripper import RobotiqGripper
import sys
# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
def main():
        robot = URControl(ip="192.168.0.2", port=30003)
        gripper=RobotiqGripper()
        gripper.connect("192.168.0.2", 63352)
        joint_state = [2.11963058, -1.64466967,  1.62860996, -1.4112251,  -1.57491714, -0.02720052]
        robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
        gripper.move(225,125,125)
        joint_state = [2.11963058, -1.44466967,  1.62860996, -1.4112251,  -1.57491714, -0.02720052]
        robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)

if __name__ == '__main__':
     main()