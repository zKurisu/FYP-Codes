import threading
from mygrpc.python.apcontrol.apcontrol_server import run as rpcServerRun
from prometheus.myprometheus import PrometheusClient
from utils.send_apInfo import send_apInfo
# from mynet.centerless.centerless import MyNet
# from mynet.multicenter.multicenter_with_mcds import MyNet
# from mynet.multicenter.static_multicenter import MyNet
from mynet.experiment.net3_three_ap_mesh import MyNet

def run(mynet):
    ###### Net start
    mynet.config()
    mynet.start()

    aps = mynet.get_ap_list()
    send_apInfo(aps)
    hosts = mynet.get_host_list()

    ###### GRPC
    rpcthread = threading.Thread(target=rpcServerRun, name="rpcServer", args=(aps,))
    rpcthread.start()

    ###### Prometheus
    # p1 = PrometheusClient(hosts[0], 11111)
    # pthread = threading.Thread(target=p1.ping_target, name="pthread", args=(hosts[1],))
    # pthread.start()

    ###### CLI
    mynet.cli()

    ###### Clean
    mynet.stop()

if __name__ == "__main__":
    mynet = MyNet()
    run(mynet)
