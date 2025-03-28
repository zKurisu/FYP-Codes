from ryu.base import app_manager
from ryu.app.wsgi import WSGIApplication, ControllerBase, route
from webob import Response
import json

class SimpleSwitch(app_manager.RyuApp):
    _CONTEXTS = { 'wsgi': WSGIApplication }

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        wsgi = kwargs['wsgi']
        wsgi.register(RestTest, { "ryu_application": self })

class RestTest(ControllerBase):
    def __init__(self, req, link, data, **configs):
        super(RestTest, self).__init__(req, link, data, **configs)

    @route("Test", "/hello/{name}", methods=["GET"])
    def _handle_hello(self, req, name, **kwargs):
        print(f"Oh my {name}")
        data = {"Jie": "hello", "Kurise": "love"}
        body = json.dumps(data).encode('utf-8')
        return Response(content_type="application/json", body=body)
