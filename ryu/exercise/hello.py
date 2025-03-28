from ryu.base import app_manager
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import HANDSHAKE_DISPATCHER
from ryu.controller import ofp_event

class HelloController(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(HelloController, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPHello, HANDSHAKE_DISPATCHER)
    def hello_handler(self, ev):
        self.logger.info(ev)
