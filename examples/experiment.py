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

HOST = "192.168.0.2"
PORT = 30003

def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper=RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)
    gripper.move(0,125,125)
    joint_state=degreestorad([138.83,-43.74,64.3,-114.82,-92.91,53.26])
    robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    
    joint_state=degreestorad([137.19,-40.59,64.48,-113.82,-87.65,48.67])
    robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    gripper.move(255,125,125)
    joint_state=degreestorad([138.83,-43.74,64.3,-114.82,-92.91,53.26])
    robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    joint_state=degreestorad([129.47,-63.2,93.06,-119.1,-91.31,33.43])
    robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    joint_state=degreestorad([129.52,-61.55,92.83,-118.06,-91.31,33.45])
    robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    gripper.move(0,125,125)
    joint_state=degreestorad([129.53,-68.61,81.36,-99.53,-91.25,33.37])
    robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    joint_state=degreestorad([144.16,-44.85,110.74,-214.52,-139.21,109.44])
    #robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    joint_state=degreestorad([142.39,-63.66,71.45,-96.70,-97.29,157.08])
    #robot.move_joint_list(joint_state, 0.1, 0.1, 0.02)
    
def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(3.1453/180)
     return(list)

if __name__ == '__main__':
     main()
     