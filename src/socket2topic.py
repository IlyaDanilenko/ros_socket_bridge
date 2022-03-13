#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy, pickle, socket
from rospy import Publisher
from visualization_msgs.msg import Marker

class Socket2TopicNode():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.__socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.publisher = Publisher("/visualization_marker", Marker, queue_size=10)
    
    def spin(self):
        self.__socket1.connect((self.ip, self.port))
        data = self.__socket1.recv(1024)
        self.__socket1.close()
        marker = pickle.loads(data)
        print(marker)

if __name__ == "__main__":
    rospy.init_node("socket2topic_node")

    port = rospy.get_param(rospy.search_param("port"))
    if type(port) == dict:
        port = 1107

    ip = rospy.get_param(rospy.search_param("ip"))
    if type(ip) == dict:
        interface = "onti.ddns.net"

    socket2topic_node = Socket2TopicNode()
