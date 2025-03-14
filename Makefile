pre:
	sudo systemctl stop NetworkManager

staticM:
	sudo PYTHONPATH=. python multi-center/static-multi-center.py

test:
	sudo PYTHONPATH=. python experiment/3_three_ap_mesh.py

post:
	ryu-manager --ofp-tcp-listen-port 6654 ryu/simple_switch_13_post.py

Mrest:
	PYTHONPATH=.:./rest uvicorn main:app --host 0.0.0.0 --reload

multicenter:
	sudo PYTHONPATH=. python multi-center/multi-center-with-mcds.py

Centerless:
	sudo PYTHONPATH=. python centerless/centerless.py
