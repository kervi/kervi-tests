import time
import zmqbus

zmq_bus_a = zmqbus.Spine()
zmq_bus_a.trigger_event("event_1", "1", "param 1 a")
zmq_bus_a.trigger_event("event_1", "2", "param 1 a")
zmq_bus_a.trigger_event("event_2", "2", "param 1 a")
zmq_bus_a.send_command("doCommand", "p1", 2)
res = zmq_bus_a.send_query("doQuery", "qp1", 3)
print("qr", res)

res = zmq_bus_a.send_query("doQuery_1", "qp1", 3)
print("qr", res)

res = zmq_bus_a.send_query("doQueryx", "qp1", 3)
print("qrx", res)


time.sleep(0)