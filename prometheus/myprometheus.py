from prometheus_client import Histogram, Gauge, Info, start_http_server
import re

class PrometheusClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.histogram = Histogram(f"ping_latency_ms_{host.name}", "Ping latency measure Histogram", buckets=[20.0, 40.0, 60.0, 80.0, 100.0, 150.0, 200.0])
        self.gauge = Gauge(f"ping_latency_ms_g_{host.name}", "Ping latency measure Gauge", ["evaluate"])
        self.info = Info(f"mininet_host_info_{host.name}", "Mininet Host information")
        self.info.info({
          "ip": self.host.IP(),
          "hostname": self.host.name,
          "clientport": str(port)
        })

    def ping_latency_ms(self, dst_host):
        while True:
            ping_output = self.host.cmd(f"ping -c 10 {dst_host.IP()}") # 需要确认这里是否会阻塞 -- Yes
            # print(ping_output)

            latency_times = re.findall(r"time=(\d+\.?\d*) ms", ping_output)
            for latency in latency_times:
                self.histogram.observe(float(latency))
            
            result = re.search(r"rtt min/avg/max/mdev = (.*) ms", ping_output)
            all_metric = result.groups()[0] if result else "0/0/0/0"
            # print(all_metric)
            min, avg, max, mdev = all_metric.split("/")

            self.gauge.labels(evaluate="min").set(float(min))
            self.gauge.labels(evaluate="avg").set(float(avg))
            self.gauge.labels(evaluate="max").set(float(max))
            self.gauge.labels(evaluate="mdev").set(float(mdev))

    def ping_target(self, dst_host):
        print(f"Run Prometheus client on {self.port}...")
        start_http_server(self.port)
        self.ping_latency_ms(dst_host)

