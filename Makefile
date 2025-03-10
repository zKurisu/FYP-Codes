staticM:
	sudo PYTHONPATH=. python multi-center/static-multi-center.py

fastapi:
	PYTHONPATH=. uvicorn main:app --host 0.0.0.0 --reload

multicenter:
	sudo PYTHONPATH=. python multi-center/multi-center-with-mcds.py

Centerless:
	sudo PYTHONPATH=. python centerless/centerless.py
