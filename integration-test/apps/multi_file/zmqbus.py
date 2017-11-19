import zmq
import random
import sys
import time
import inspect
import threading
import json
import pickle
from kervi.utility.named_lists import NamedLists

class _ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            data = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(data)
        return obj


class ZMQEventHandler(threading.Thread):
    def __init__(self, bus, event, handler, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True
        self.terminate = False
        self._handler = handler
        self._bus = bus
        self._event = event
        self._id = kwargs.get("id", None)
        self._groups = kwargs.get("groups", None)
        self._handler = handler

        self._has_keywords = inspect.getargspec(self._handler).keywords

    def stop(self):
        self.terminate = True

    def run(self):
        event_tag = "event:" + self._event
        if self._id:
            event_tag += ":" + self._id
        socket = self._bus._context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, event_tag)
        socket.connect('inproc://events')
        while not self.terminate:
            [topic, component_id, json_message] = socket.recv_multipart()
            message = pickle.loads(json_message)

            session_groups = message['groups']
            authorized = True
            if session_groups and self._groups:
                for group in self._groups:
                    if group in session_groups:
                        break
                else:
                    authorized = False

            if authorized:
                if self._has_keywords:
                    self._handler(message["id"], *message['args'], injected=message["injected"], scope=message["scope"])
                else:
                    self._handler(message["id"], *message['args'])

class ZMQCommandHandler(threading.Thread):
    def __init__(self, bus, command, handler, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True
        self.terminate = False
        self._handler = handler
        self._bus = bus
        self._command = command
        self._handler = handler
        self._groups = kwargs.get("groups", None)
        self._has_keywords = inspect.getargspec(self._handler).keywords

    def stop(self):
        self.terminate = True

    def run(self):
        socket = self._bus._context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, "command:"+self._command)
        socket.connect('inproc://commands')
        while not self.terminate:
            [command, json_message] = socket.recv_multipart()
            message = pickle.loads(json_message)

            session_groups = message['groups']
            authorized = True
            if session_groups and self._groups:
                for group in self._groups:
                    if group in session_groups:
                        break
                else:
                    authorized = False

            if authorized:
                if self._has_keywords:
                    self._handler(*message['args'], injected=message["injected"], scope=message["scope"])
                else:
                    self._handler(*message['args'])

class ZMQQueryHandler(threading.Thread):
    def __init__(self, bus):
        threading.Thread.__init__(self)
        self.daemon = True
        self.terminate = False
        self._bus = bus
        self._socket = self._bus._context.socket(zmq.REP)
        self._handlers = NamedLists()

    def stop(self):
        self.terminate = True

    def register_handler(self, query, func, **kwargs):
        groups = kwargs.get("groups", None)
        argspec = inspect.getargspec(func)
        self._handlers.add(query,(func, groups, argspec.keywords))
        #self._socket.setsockopt_string(zmq.SUBSCRIBE, "query:" + query)

    def call_handlers(self, query, args, session, injected):
        
        func_list = self._handlers.get_list_data(query)
        result = []
        try:
            if func_list:
                for func, groups, has_keywords in func_list:
                    
                    if session:
                        session_groups = session['groups']
                    else:
                        session_groups = None
                    authorized = True
                    
                    if session_groups != None and groups and len(groups)>0:
                        for group in groups:
                            if group in session_groups:
                                break
                        else:
                            authorized = False
                    
                    if authorized:
                        if not has_keywords:
                            sub_result = func(*args)
                            if sub_result:
                                result += [sub_result]
                        else:
                            sub_result = func(*args, injected=injected, session=session)
                            if sub_result:
                                result += [sub_result]
            if len(result) == 1:
                return result[0]
        except:
            print("Exception in query:", query)
            self.log.exception("Exception in query:" + query)

        return result
    
    def run(self):
        print("x")
        self._socket.connect('inproc://queries')
        while not self.terminate:
            [query, json_message] = self._socket.recv_multipart()
            print("y", query, json_message)
            message = pickle.loads(json_message)
            result = self.call_handlers(message["query"], message["args"], message["session"], message["injected"])
            p = pickle.dumps(result, -1)
            response_tag = "query_response:" + message['id']
            self._socket.send_multipart([response_tag.encode(), p])

class ZMQBus():
    _context = None
    _frontend = None
    _handlers = []
    _event_sock = None
    _command_sock = None
    _query_sock = None
    _query_handler = None
    def __init__(self):
        pass

    def reset_bus(self):
        self._context = zmq.Context()
        self._frontend = self._context.socket(zmq.ROUTER)
        self._frontend.bind('tcp://*:5570')
        self._event_sock = self._context.socket(zmq.PUB)
        self._event_sock.bind("inproc://events")
        self._command_sock = self._context.socket(zmq.PUB)
        self._command_sock.bind("inproc://commands")
        self._query_sock = self._context.socket(zmq.REQ)
        self._query_sock.bind("inproc://queries")

        self._query_handler = ZMQQueryHandler(self)

        #zmq.proxy(self._frontend, self._event_sock)
        #zmq.proxy(self._frontend, self._command_sock)
        #zmq.proxy(self._frontend, self._query_sock)

    def run(self):
        self._query_handler.start()

    def stop(self):
        self._query_handler.terminate()
        for handler in self._handlers:
            handler.terminate()

    def send_command(self, command, *args, **kwargs):
        injected = kwargs.get("injected", "")
        scope = kwargs.get("scope", "global")
        groups = kwargs.get("groups", None)
        session = kwargs.get("session", None)
        #self.log.debug("triggerEvent:{0}, id:{1} injected:{2}, scope:{3}", event, id, injected, scope)
        command_message = {"command":command, "args":args, "injected":injected, "scope":scope, "session":session, "groups": groups}
        jsonres = json.dumps(command_message)
        p = pickle.dumps(command_message, -1)
        command_tag = "command:" + command
        self._command_sock.send_multipart([command_tag.encode(), p])

    def register_command_handler(self, command, func, **kwargs):
        handler_thread = ZMQCommandHandler(self, command, func, **kwargs)
        handler_thread.start()
        self._handlers += [handler_thread]

    def trigger_event(self, event, id, *args, **kwargs):
        injected = kwargs.get("injected", "")
        scope = kwargs.get("scope", "global")
        groups = kwargs.get("groups", None)
        #self.log.debug("triggerEvent:{0}, id:{1} injected:{2}, scope:{3}", event, id, injected, scope)
        event_message = {'event':event, 'id':id, 'args':args, "injected":injected, "scope":scope, "groups":groups}
        jsonres = json.dumps(event_message)
        p = pickle.dumps(event_message, -1)
        event_tag = "event:" + event + ":" + id
        self._event_sock.send_multipart([event_tag.encode(), id.encode(), p])

    def register_event_handler(self, event, func, **kwargs):
        handler_thread = ZMQEventHandler(self, event, func, **kwargs)
        handler_thread.start()
        self._handlers += [handler_thread]

    def send_query(self, query, *args, **kwargs):
        injected = kwargs.get("injected", "")
        scope = kwargs.get("scope", "global")
        groups = kwargs.get("groups", None)
        session = kwargs.get("session", None)
        #self.log.debug("triggerEvent:{0}, id:{1} injected:{2}, scope:{3}", event, id, injected, scope)
        query_message = {'query':query, "id": "123", 'args':args, "injected":injected, "scope":scope, "groups":groups, "session":session}
        jsonres = json.dumps(query_message)
        p = pickle.dumps(query_message, -1)
        query_tag = "query:" + query
        self._query_sock.send_multipart([query_tag.encode(), p])
        query_id, json_result = self._query_sock.recv_multipart()
        result = pickle.loads(json_result)
        return result

    def register_query_handler(self, query, func, **kwargs):
        self._query_handler.register_handler(query, func, **kwargs)

zmq_bus = ZMQBus()
zmq_bus.reset_bus()

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


zmq_bus.register_event_handler("event_1", event_handler, id="1")
zmq_bus.register_event_handler("event_2", event_handler1, id="1")
zmq_bus.register_event_handler("event_1", event_handler2)
zmq_bus.register_command_handler("doCommand", command_handler1)
zmq_bus.register_query_handler("doQuery", query_handler1)
zmq_bus.register_query_handler("doQuery", query_handler2)

zmq_bus.run()
time.sleep(1)

zmq_bus.trigger_event("event_1", "1", "param 1")
zmq_bus.trigger_event("event_1", "2", "param 1")
zmq_bus.trigger_event("event_2", "2", "param 1")
zmq_bus.send_command("doCommand", "p1", 2)
res = zmq_bus.send_query("doQuery", "qp1", 3)
print("qr", res)

time.sleep(5)