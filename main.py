import threading
from mygrpc.python.apcontrol.apcontrol_server import APCrpcserver
from prometheus.myprometheus import PrometheusClient
from mynet.centerless.centerless_with_mcds import MyNet
# from mynet.centerless.centerless_move import MyNet
# from mynet.multicenter.multicenter_with_mcds import MyNet
# from mynet.multicenter.static_multicenter import MyNet

def run(mynet):
    ###### Net start
    mynet.config()
    mynet.start()

    hosts = mynet.get_host_list()

    ###### GRPC
    r1 = APCrpcserver(mynet)
    rpcthread = threading.Thread(target=r1.run, name="rpcServer")
    rpcthread.start()

    ###### Prometheus
    # p1 = PrometheusClient(hosts[0], 11111)
    
    # pthread = threading.Thread(target=p1.ping_target, name="pthread_ping", args=(hosts[1:],))
    # pthread = threading.Thread(target=p1.iperf_targets, name="pthread_iperf", args=(hosts[1:],))
    # pthread.start()

    ###### CLI
    mynet.cli()

    ###### Clean
    r1.stop()
    rpcthread.join()
    # p1.clean()
    # pthread.join()
    mynet.stop()

if __name__ == "__main__":
    mynet = MyNet(ap_number=5)
    run(mynet)
