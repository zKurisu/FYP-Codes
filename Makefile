RYU_short_path="ryu/short_path.py"
RYU_simple_monitor="ryu/simple_monitor_13.py"
RYU_hello="ryu/exercise/hello.py"
RYU_rest="ryu/exercise/rest_mapper.py"
RYU_current=${RYU_short_path}
Prometheus_bin="prometheus/ori/prometheus"
Prometheus_config="prometheus/ori/test.yml"

pre:
	sudo systemctl stop NetworkManager

run:
	sudo PYTHONPATH=. python main.py

Mprom:
	./${Prometheus_bin} --config.file=${Prometheus_config} --web.enable-lifecycle

Mrest:
	PYTHONPATH=.:./rest uvicorn rest:app --host 0.0.0.0 --reload

Mryu:
	ryu-manager --observe-links --ofp-tcp-listen-port 6654 ${RYU_current}

post:
	ryu-manager --observe-links --ofp-tcp-listen-port 6654 ryu/simple_switch_13_post.py

TrpcS:
	PYTHONPATH=. python testRPCServer.py

TrpcC:
	PYTHONPATH=. python testRPCClient.py

clean:
	rm *.apconf
	sudo mn -c
