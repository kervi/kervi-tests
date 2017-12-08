import time
import kervi.spine as spine

def value_changed(component_id, value, log):
    print("wc", component_id, value, log)


spine._init_spine("p2", 9510, "tcp://127.0.0.1:9500")
s = spine.Spine()
s.register_event_handler("dynamicValueChanged", value_changed)
s.run()        
time.sleep(5)

print("start test")
#zmq_bus.trigger_event("event_1", "1", "param 1 p2")
#zmq_bus.trigger_event("event_1", "2", "param 1")
#zmq_bus.trigger_event("event_2", "2", "param 1")
#zmq_bus.send_command("doCommand", "p1", 2)

res = s.send_query("GetApplicationInfo")
print("app info", res)

#res = s.send_query("getComponentInfo")
#print("component info", res)



try:
    while True:

        
        time.sleep(1)
        #break
except KeyboardInterrupt:
    pass
print("close")
s.stop()
print("done")