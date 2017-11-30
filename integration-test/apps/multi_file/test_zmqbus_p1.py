import time
import zmqbus

zmqbus._init_spine("p1", 9500)
#zmq_bus.connect_to_root()

def event_handler(event_id, param_1):
    print("event 1, h1", param_1)

def event_handler1(event_id, param_1, **kwargs):
    print("event 2", param_1)

def event_handler2(event_id, param_1):
    print("event 1, h2", event_id, param_1)

def command_handler1(param_1, param_2, **kwargs):
    print("commmand", param_1, param_2)

def query_handler1(param_1, param_2, **kwargs):
    print("query 1 ", param_1, param_2)
    return {"x":"test x"}

def query_handler2(param_1, param_2, **kwargs):
    print("query 2", param_1, param_2)
    return {"y":"test y"}

def query_handler3(param_1, param_2, **kwargs):
    print("query_1 3", param_1, param_2)
    return {"y":"test y"}


zmq_bus = zmqbus.Spine()

zmq_bus.register_event_handler("event_1", event_handler, id="1")
zmq_bus.register_event_handler("event_2", event_handler1, id="1")
zmq_bus.register_event_handler("event_1", event_handler2)
zmq_bus.register_command_handler("doCommand", command_handler1)
zmq_bus.register_query_handler("doQuery", query_handler1)
zmq_bus.register_query_handler("doQuery", query_handler2)
zmq_bus.register_query_handler("doQuery_1", query_handler2)
print("x")
zmq_bus.run()

print("y")
time.sleep(0)

zmq_bus.trigger_event("event_1", "1", "param 1 a")

import test_zmqbus_p1a

print("p1 ready")
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pass

