pre:
	sudo systemctl stop NetworkManager

run:
	sudo PYTHONPATH=. python main.py

staticM:
	sudo PYTHONPATH=. python mynet/multicenter/static-multi-center.py

test:
	sudo PYTHONPATH=. python mynet/experiment/3_three_ap_mesh.py

post:
	ryu-manager --ofp-tcp-listen-port 6654 ryu/simple_switch_13_post.py

Mrest:
	PYTHONPATH=.:./rest uvicorn rest:app --host 0.0.0.0 --reload

multicenter:
	sudo PYTHONPATH=. python mynet/multicenter/multi-center-with-mcds.py

Centerless:
	sudo PYTHONPATH=. python mynet/centerless/centerless.py

clean:
	rm *.apconf
	sudo mn -c
