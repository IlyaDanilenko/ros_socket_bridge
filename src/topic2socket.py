#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy, pickle, socket, os
from rospy import Subscriber
from visualization_msgs.msg import Marker, MarkerArray

class Topic2SocketNode():

    def callback1(self, data):
        self.__msg = pickle.dumps(data)

    def __init__(self, interface, port):
        self.__msg = b''
        self.port = port
        self.ip = os.popen(f'ip addr show {interface}').read().split("inet ")[1].split("/")[0]
        self.__subscriber1 = Subscriber("/visualization_marker", Marker)

        self.__socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket1.bind((self.ip, self.port))

        # self.__socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.__socket2.bind((self.ip, self.port + 1))

    def spin(self):
        conn, addr = self.__socket1.accept()
        self.__socket1.sendto(self.__msg, addr)


if __name__ == "__main__":
    rospy.init_node("topic2socket_node")

    port = rospy.get_param(rospy.search_param("port"))
    if type(port) == dict:
        port = 1107

    interface = rospy.get_param(rospy.search_param("interface"))
    if type(interface) == dict:
        interface = "eth0"

    topic2socket_node = Topic2SocketNode(interface, port)

    while not rospy.is_shutdown():
        topic2socket_node.spin()