import socket
import math
from utils import util
import numpy as np
import time
import struct
HOST = "192.168.0.2"
PORT = 30003

def main():
    #tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #tcp_socket.connect((HOST, PORT))
    joint_state=degreestorad([93.77,-89.07,89.97,-90.01,-90.04,0.0])
    move_joint_list(joint_state, 1.4, 1.05, 0.02)
    #go_home()

def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)

def move_joint_list(q, v = 0.5, a = 0.2, r = 0.05):
    """
    move the arm according joint state
    :param q: joint state list
    :param v: vel
    :param a: acc
    :param r: blend radius
    """
    tool_pos_tolerance = [0.001, 0.001, 0.001, 0.05, 0.05, 0.05]
    joint_positions = ','.join([f"{pos}" for pos in q])
    tcp_command = f"def process():\n"
    tcp_command += f"  movej([{joint_positions}], a={a}, v={v}, a={r})\n"
    tcp_command += "end\n"
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()
    actual_pos = get_current_joint_positions()
    target_rpy = util.rv2rpy(q[3], q[4], q[5])
    rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])
    while not (all([np.abs(actual_pos[j] - q[j]) <tool_pos_tolerance[j] for j in range(3)])
               and all([np.abs(rpy[j] - target_rpy[j]) < tool_pos_tolerance[j+3] for j in range(3)])):
        actual_pos = get_current_joint_positions()
        rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])
        time.sleep(0.01)


def get_current_joint_positions():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    state_data =  tcp_socket.recv(1500)
    actual_joint_positions = parse_tcp_state_data(state_data, 'joint_data')
    # joint_positions_degrees = np.rad2deg(np.asarray(actual_joint_positions))
    tcp_socket.close()
    return np.asarray(actual_joint_positions)
def parse_tcp_state_data( data, subpasckage):
    dic = {'MessageSize': 'i', 'Time': 'd', 'q target': '6d', 'qd target': '6d', 'qdd target': '6d',
            'I target': '6d',
            'M target': '6d', 'q actual': '6d', 'qd actual': '6d', 'I actual': '6d', 'I control': '6d',
            'Tool vector actual': '6d', 'TCP speed actual': '6d', 'TCP force': '6d', 'Tool vector target': '6d',
            'TCP speed target': '6d', 'Digital input bits': 'd', 'Motor temperatures': '6d', 'Controller Timer': 'd',
            'Test value': 'd', 'Robot Mode': 'd', 'Joint Modes': '6d', 'Safety Mode': 'd', 'empty1': '6d',
            'Tool Accelerometer values': '3d',
            'empty2': '6d', 'Speed scaling': 'd', 'Linear momentum norm': 'd', 'SoftwareOnly': 'd',
            'softwareOnly2': 'd',
            'V main': 'd',
            'V robot': 'd', 'I robot': 'd', 'V actual': '6d', 'Digital outputs': 'd', 'Program state': 'd',
            'Elbow position': 'd', 'Elbow velocity': '3d'}
    ii = range(len(dic))
    for key, i in zip(dic, ii):
        fmtsize = struct.calcsize(dic[key])
        data1, data = data[0:fmtsize], data[fmtsize:]
        fmt = "!" + dic[key]
        dic[key] = dic[key], struct.unpack(fmt, data1)

    if subpasckage == 'joint_data':  # get joint data
        q_actual_tuple = dic["q actual"]
        joint_data= np.array(q_actual_tuple[1])
        return joint_data
    elif subpasckage == 'cartesian_info':
        Tool_vector_actual = dic["Tool vector actual"]  # get x y z rx ry rz
        cartesian_info = np.array(Tool_vector_actual[1])
        return cartesian_info

def go_home():
    joint_state = [1.6898278, -0.118682, -2.8710666, -1.7318902, 0.009250245, 0.001919862]
    move_joint_list(joint_state, 1.4, 1.05, 0.02)


if __name__ == '__main__':
    main()