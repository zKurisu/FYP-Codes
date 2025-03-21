from prometheus_client import Histogram, Gauge, Info, start_http_server
import re

class PrometheusClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.info = Info(f"mininet_host_info_{host.name}", "Mininet Host information")
        self.info.info({
          "ip": self.host.IP(),
          "hostname": self.host.name,
          "clientport": str(port)
        })

    def ping_latency_ms(self, dst_host):
        histogram = Histogram(f"ping_latency_ms_{self.host.name}", "Ping latency measure Histogram", buckets=[20.0, 40.0, 60.0, 80.0, 100.0, 150.0, 200.0])
        gauge = Gauge(f"ping_latency_ms_g_{self.host.name}", "Ping latency measure Gauge", ["evaluate"])
        while True:
            ping_output = self.host.cmd(f"ping -c 10 {dst_host.IP()}") # 需要确认这里是否会阻塞 -- Yes
            # print(ping_output)

            latency_times = re.findall(r"time=(\d+\.?\d*) ms", ping_output)
            for latency in latency_times:
                histogram.observe(float(latency))
            
            result = re.search(r"rtt min/avg/max/mdev = (.*) ms", ping_output)
            all_metric = result.groups()[0] if result else "0/0/0/0"
            # print(all_metric)
            min, avg, max, mdev = all_metric.split("/")

            gauge.labels(evaluate="min").set(float(min))
            gauge.labels(evaluate="avg").set(float(avg))
            gauge.labels(evaluate="max").set(float(max))
            gauge.labels(evaluate="mdev").set(float(mdev))

    def ping_target(self, dst_host):
        print(f"Ping Test, run Prometheus client on {self.port}...")
        start_http_server(self.port)
        self.ping_latency_ms(dst_host)
    
    def run_iperf(self, dst_host, gauge):
        result = self.host.cmd(f"iperf -c {dst_host.name}")
        
        output_lines = result.splitlines()
        bandwidth = float(0)
        if output_lines:
            last_line = output_lines[-1]
            if "Mbits/sec" in last_line:
                bandwidth = float(last_line.split()[6])
                gauge.labels(dst_host=f"{dst_host.name}").set(bandwidth)
        
        gauge.labels(dst_host=f"{dst_host.name}").set(bandwidth)
        # print(f"{self.host.name} iperf -c {dst_host.name}: {bandwidth}Mbits/sec")

    def iperf_bd(self, dst_hosts):
        gauge = Gauge(f"iperf_bd_g_{self.host.name}", f"Iperf test for {self.host.name} as client", ["dst_host"])
        for dst_host in dst_hosts:
            print(f"{dst_host.name} run iperf -s...")
            dst_host.cmd(f"iperf -s &")
        
        while True:
            for dst_host in dst_hosts:
                self.run_iperf(dst_host, gauge)
    
    def iperf_targets(self, dst_hosts):
        print(f"Iperf Test, run Prometheus client on {self.port}...")
        start_http_server(self.port)
        self.iperf_bd(dst_hosts)
