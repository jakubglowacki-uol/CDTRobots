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


rack1_origin=[105.08,334.24,50.11,2.203,-2.242,-0.051]
rack0_origin=[251.75,80.45,50.55,2.203,-2.242,-0.051]
approach=[146.54,167.55,199.42,3.055,-0.731,0]

def pick_vial(robot:URControl, rackIndex, vialIndex):
    if (rackIndex == 0):
        print("Picking from rack 0")
        rackPosX=0
        rackPosY=0
        rackPosZ_grasp=rack0_origin[2]
        rackPosZ_lift=rack0_origin[2]+50
        if (vialIndex < 4):
            rackPosX=rack0_origin[0]+(vialIndex*30)
            rackPosY=rack0_origin[1]
        else:
            rackPosX=rack0_origin[0]+((vialIndex-4)*30)
            rackPosY=rack0_origin[1]+45
    elif (rackIndex ==1):
        print("Picking from rack 1")
    else:
        print("Invalid Rack!")
    
    pre_pos=[rackPosX, rackPosY, rackPosZ_lift, rack0_origin[3], rack0_origin[4], rack0_origin[5]]
    grasp_pos=[rackPosX, rackPosY, rackPosZ_grasp, rack0_origin[3], rack0_origin[4], rack0_origin[5]]
    robot.movel_tcp(approach)
    robot.movel_tcp(pre_pos)
    robot.movel_tcp(grasp_pos)
    robot.movel_tcp(pre_pos)
    robot.movel_tcp(approach)




def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper=RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)
    gripper.move(0,125,125)
    pick_vial(robot,0,0)


    #robot.go_home()
    
def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(3.1453/180)
     return(list)

if __name__ == '__main__':
     main()
     