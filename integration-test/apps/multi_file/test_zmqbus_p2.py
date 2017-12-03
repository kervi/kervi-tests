import time
import zmqbus

zmqbus._init_spine("p2", 9501, "tcp://127.0.0.1:9500", "127.0.0.1")
zmq_bus = zmqbus.Spine()
zmq_bus.run()
#time.sleep(1)

print("start test")
zmq_bus.trigger_event("event_1", "1", "param 1 p2")
zmq_bus.trigger_event("event_1", "2", "param 1")
zmq_bus.trigger_event("event_2", "2", "param 1")
zmq_bus.send_command("doCommand", "p1", 2)
res = zmq_bus.send_query("doQuery", "qp1", 3)
print("qr", res)

res = zmq_bus.send_query("doQuery_1", "qp1", 3)
print("qr", res)


res = zmq_bus.send_query("doQueryx", "qp1", 3)
print("qrx", res)

#time.sleep(5)
print("close")
zmq_bus.stop()
print("done")