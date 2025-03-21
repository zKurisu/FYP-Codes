from prometheus_client import Histogram, Gauge, Info, start_http_server
from scapy.all import rdpcap, Scapy_Exception
from collections import defaultdict
import threading
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

        self.loss_gauge = Gauge(f"packet_loss_rate_g_{host.name}", f"Packet loss rate gause for {host.name}", ["dst_host"])
        self.pcap = f"{host.name}-tcpdump.pcap"
        self.prev_sent_packets = {}
        self.prev_received_packets = {}
        print(f"Host {self.host.name} start: [tcpdump -i {self.host.name}-eth0 -w {self.pcap} &] ")
        self.host.cmd(f"tcpdump -i {self.host.name}-eth0 -w {self.pcap} &")
        self.timer = threading.Timer(10.0, self.calculate_packet_loss)
        self.timer.start()
        self.running = True

    def ping_latency_ms(self, dst_host):
        histogram = Histogram(f"ping_latency_ms_{self.host.name}", "Ping latency measure Histogram", buckets=[20.0, 40.0, 60.0, 80.0, 100.0, 150.0, 200.0])
        gauge = Gauge(f"ping_latency_ms_g_{self.host.name}", "Ping latency measure Gauge", ["evaluate"])
        while self.running:
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
    
    def iperf_bd(self, dst_hosts):
        gauge = Gauge(f"iperf_bd_g_{self.host.name}", f"Iperf test for {self.host.name} as client", ["dst_host"])
        for dst_host in dst_hosts:
            print(f"{dst_host.name} run iperf -s...")
            dst_host.cmd(f"iperf -s &")
        
        while self.running:
            for dst_host in dst_hosts:
                result = self.host.cmd(f"iperf -c {dst_host.IP()}")
                
                output_lines = result.splitlines()
                bandwidth = float(0)
                if output_lines:
                    last_line = output_lines[-1]
                    if "Mbits/sec" in last_line:
                        bandwidth = float(last_line.split()[6])
                        gauge.labels(dst_host=f"{dst_host.name}").set(bandwidth)
                
                gauge.labels(dst_host=f"{dst_host.name}").set(bandwidth)
                print(f"{self.host.name} iperf -c {dst_host.name}: {bandwidth}Mbits/sec")
    
    def iperf_targets(self, dst_hosts):
        print(f"Iperf Test, run Prometheus client on {self.port}...")
        start_http_server(self.port)
        self.iperf_bd(dst_hosts)
    
    def calculate_packet_loss(self):
        # 读取 pcap 文件
        print(f"Timer for analyze pcap file is started...")
        try:
            packets = rdpcap(self.pcap)

            # 统计发送和接收的数据包数量
            sent_packets = defaultdict(int)  # 记录发送到每个目标 IP 的数据包数量
            received_packets = defaultdict(int)  # 记录从每个目标 IP 接收到的数据包数量

            for pkt in packets:
                if pkt.haslayer("IP"):
                    if pkt["IP"].src == self.host.IP():
                        # 统计发送的数据包
                        dst_ip = pkt["IP"].dst
                        sent_packets[dst_ip] += 1
                    elif pkt["IP"].dst == self.host.IP():
                        # 统计接收的数据包
                        src_ip_of_received = pkt["IP"].src
                        received_packets[src_ip_of_received] += 1

            # 计算每个目标 IP 的丢包率
            for dst_ip in sent_packets:
                prev_sent_packets = self.prev_sent_packets[dst_ip] if self.prev_sent_packets.get(dst_ip) else 0
                prev_received_packets = self.prev_received_packets[dst_ip] if self.prev_received_packets.get(dst_ip) else 0

                sent = sent_packets[dst_ip] - prev_sent_packets
                received = received_packets.get(dst_ip, 0) - prev_received_packets
                if sent > 0:
                    if received > sent:
                        print(f"Warning: Received packets ({received}) > Sent packets ({sent}) for {dst_ip}. Possible duplicate packets or incomplete capture.")
                        loss_rate = 0  # 如果接收的数据包多于发送的数据包，丢包率设为 0
                    else:
                        print(f"Warning: Received packets ({received}) > Sent packets ({sent}) for {dst_ip}. Possible duplicate packets or incomplete capture.")
                        loss_rate = (sent - received) * 100 / sent
                    print(f"Packet loss rate from {self.host.IP()} to {dst_ip}: {loss_rate:.2f}%")
                    self.loss_gauge.labels(dst_host=f"{dst_ip}").set(float(loss_rate))
                else:
                    print(f"No packets sent from {self.host.IP()} to {dst_ip}.")
            
            self.prev_sent_packets = sent_packets
            self.prev_received_packets = received_packets
        except Scapy_Exception as e:
            print(f"No data now: {e}")
        finally:
            # 重新启动定时器
            self.timer = threading.Timer(10.0, self.calculate_packet_loss)
            self.timer.start()

    def clean(self):
        self.running = False
        if self.timer:
            self.timer.cancel()
