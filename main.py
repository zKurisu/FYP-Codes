import threading
from mygrpc.python.apcontrol.apcontrol_server import run as rpcServerRun
from prometheus.myprometheus import PrometheusClient
from utils.send_apInfo import send_apInfo
# from mynet.centerless.centerless import MyNet
# from mynet.multicenter.multicenter_with_mcds import MyNet
# from mynet.multicenter.static_multicenter import MyNet
# from mynet.experiment.net3_three_ap_mesh import MyNet
from mynet.experiment.net9_mix_text import MyNet

def run(mynet):
    ###### Net start
    mynet.config()
    mynet.start()

    aps = mynet.get_ap_list()
    port_to_mesh = mynet.port_to_mesh
    send_apInfo(aps)
    hosts = mynet.get_host_list()

    ###### GRPC
    rpcthread = threading.Thread(target=rpcServerRun, name="rpcServer", args=(aps, port_to_mesh,))
    rpcthread.start()

    ###### Prometheus
    p1 = PrometheusClient(hosts[0], 11111)
    #threading.Thread(target=p1.ping_target, name="pthread_ping", args=(hosts[1],)).start()
    t1 = threading.Thread(target=p1.iperf_targets, name="pthread_iperf", args=(hosts[1:],))
    t1.start()

    ###### CLI
    mynet.cli()

    ###### Clean
    p1.clean()
    t1.join()
    mynet.stop()

if __name__ == "__main__":
    mynet = MyNet()
    run(mynet)
