
from PIL import ImageTk, Image
import numpy as np
import math
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))
from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper=RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)
    gripper.move(0,125,125)
    joint_state = [0.00000744, -1.57083954, 1.57082969, -1.57077511, -1.57079918, -0.00003463]
    robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
    joint_state = degreestorad([-5.61,-83.95,112.70,-119.79,-90.07,-5.48])
    robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
    gripper.move(255,125,125)
    joint_state = degreestorad([-5.61,-88.51,105.96,-107.5,-90.03,-5.53])
    robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
    joint_state = degreestorad([-1.36,-88.22,102.71,-104.52,-90.03,-1.29])
    robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
    joint_state = degreestorad([-1.95,-83.1,112.78,-119.71,-90.08,-1.81])
    robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)
    gripper.move(0,125,125)
    joint_state = [0.00000744, -1.57083954, 1.57082969, -1.57077511, -1.57079918, -0.00003463]
    robot.move_joint_list(joint_state, 0.25, 0.5, 0.02)


def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)    
    

if __name__=="__main__":
     main()