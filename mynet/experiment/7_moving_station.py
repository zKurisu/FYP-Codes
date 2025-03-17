#! /usr/bin/python3
#  7_moving_station.py
#
#  function
#
#  Copyright (Python) Jie
#  2025-03-05
# 

from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI

from mininet.log import info, setLogLevel
import threading

def mytopo(args):
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    sta1 = net.addStation("sta1", mac="00:00:00:00:00:11")
    c0 = net.addController("c0")

    net.setPropagationModel(model="logDistance", exp=5)
    net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
    net.plotGraph(max_x=100, max_y=100)

    net.configureNodes()

    net.build()
    c0.start()

    def check_position():
        posi = sta1.position
        if posi[0] > 50:
            info("OOOOOOOOO")
        # 每隔 1 秒重新启动定时器
        threading.Timer(1, check_position).start()

    # 启动定时任务
    check_position()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    mytopo([])
