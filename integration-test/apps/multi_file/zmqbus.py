import zmq
import random
import sys
import time
import inspect
import threading
import json
import pickle
import uuid
from kervi.utility.named_lists import NamedLists
import kervi.utility.nethelper as nethelper

_KERVI_COMMAND_ADDRESS = "inproc://kervi_commands"
_KERVI_QUERY_ADDRESS = "inproc://kervi_query"
_KERVI_EVENT_ADDRESS = "inproc://kervi_events"

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

class ProcessConnection:
    def __init__(self, bus):
        self.address = None
        self._bus = bus
        self._signal_socket = self._bus._context.socket(zmq.PUB)
        pass

    def connect(self, address):
        self.address = address
        cr = self._signal_socket.connect(address)
        time.sleep(1)
        signal_message = {"address": self._bus._signal_address}
        p = pickle.dumps(signal_message, -1)
        signal_tag = "signal:connect"
        self.send_package([signal_tag.encode(), p])
        

    def register(self, address):
        #print("register", address)
        self.address = address
        self._signal_socket.connect(address)

    def disconnect(self):
        pass

    def send_query(self, package):
        self.send_package(package)

    def send_package(self, package):
        #print("send_package", self.address, package)
        self._signal_socket.send_multipart(package)

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

    def run(self):
        self._socket.connect(_KERVI_QUERY_ADDRESS)
        while not self.terminate:
            [tag, json_message] = self._socket.recv_multipart()
            message = pickle.loads(json_message)
            result = self._bus._handle_message(tag.decode('utf-8'), message)
            p = pickle.dumps(result, -1)
            response_tag = "query_response:" + message['responseId']
            self._socket.send_multipart([response_tag.encode(), p])

class ZMQMessageThread(threading.Thread):
    def __init__(self, bus, socket):
        threading.Thread.__init__(self)
        self._bus = bus
        self._socket = socket
        self.daemon = True
        self._terminate = False

    def register(self, tag):
        #print("r", tag)
        self._socket.setsockopt_string(zmq.SUBSCRIBE, tag)

    def stop(self):
        self._terminate = True

    def run(self):
        while not self._terminate:
            [tag, json_message] = self._socket.recv_multipart()

            message = pickle.loads(json_message)
            #print("t", tag, message)
            self._bus._handle_message(tag.decode('utf-8'), message)

class ZMQBus():
    _context = None
    _handlers = NamedLists()
    _connections = []
    _event_sock = None
    _command_sock = None
    _query_sock = None

    def __init__(self):
        #print("sc", self._context)
        pass

    def reset_bus(self, signal_port, ip="127.0.0.1", root_address=None, event_port=None):
        #self._flow_in_address = "tcp://*:" + str(flow_in_port)
        self._handlers = NamedLists()
        self._query_id_count = 0
        self._uuid_handler = uuid.uuid4().hex
        self._is_root = not root_address == None
        self._root_address = root_address
        self._signal_address = "tcp://"+ ip +":" + str(signal_port)
        self._context = zmq.Context()
        self._signal_socket = self._context.socket(zmq.SUB)
        #self._handlers += [ZMQSignalHandler(self, self._on_connect, self._on_register)]

        self._event_socket = self._context.socket(zmq.PUB)
        self._event_socket.bind(_KERVI_EVENT_ADDRESS)

        self._event_socket_sub = self._context.socket(zmq.SUB)
        self._event_socket_sub.connect(_KERVI_EVENT_ADDRESS)

        self._command_socket = self._context.socket(zmq.PUB)
        self._command_socket.bind(_KERVI_COMMAND_ADDRESS)

        self._command_socket_sub = self._context.socket(zmq.SUB)
        self._command_socket_sub.connect(_KERVI_COMMAND_ADDRESS)

        self._query_socket = self._context.socket(zmq.REQ)
        self._query_socket.bind(_KERVI_QUERY_ADDRESS)

        self._message_handler = ZMQMessageThread(self, self._signal_socket)
        self._query_handler = ZMQQueryHandler(self)
        self._event_handler = ZMQMessageThread(self, self._event_socket_sub)
        self._command_handler = ZMQMessageThread(self, self._command_socket_sub)

        self._register_handler("signal:connect", self._on_connect)
        self._message_handler.register("signal:connect")

    def _register_handler(self, tag, func, **kwargs):
        groups = kwargs.get("groups", None)
        argspec = inspect.getargspec(func)
        self._handlers.add(tag, (func, groups, argspec.keywords))

    def _handle_message(self, tag, message):
        func_list = self._handlers.get_list_data(tag)
        result = []
        session = None
        session_groups = None
        if "session" in message:
            session = message["session"]
            if session:
                session_groups = session['groups']
            else:
                session_groups = None

        if "injected" in message:
            injected = message["injected"]
        else:
            injected = None
        
        message_args = []
        if "id" in message:
            message_args += [message["id"]]

        if "address" in message:
            message_args += [message["address"]]
        
        if "args" in message:
            message_args += message["args"]
        try:
            if func_list:
                for func, groups, has_keywords in func_list:
                    authorized = True
                    if session_groups != None and groups and len(groups)>0:
                        for group in groups:
                            if group in session_groups:
                                break
                        else:
                            authorized = False
                    
                    if authorized:
                        if not has_keywords:
                            sub_result = func(*message_args)
                            if sub_result:
                                result += [sub_result]
                        else:
                            sub_result = func(*message_args, injected=message["injected"], scope=message["scope"])
                            if sub_result:
                                result += [sub_result]
            if len(result) == 1:
                return result[0]
        except Exception as e:
            raise e

        return result
    
    def run(self):
        #print("run", self._signal_address)
        self._query_handler.start()
        self._signal_socket.bind(self._signal_address)
        
        self._message_handler.start()
        self._event_handler.start()
        self._command_handler.start()
        
        if self._root_address:
            self.connect_to_root()

    def stop(self):
        self._message_handler.stop()
        self._event_handler.stop()
        self._command_handler.stop()

    def _on_connect(self, address):
        print("on_connect", address)
        connection = ProcessConnection(self)
        connection.register(address)
        self._connections += [connection]
    
    def connect_to_root(self):
        print("connect to root")
        connection = ProcessConnection(self)
        connection.connect(self._root_address)
        self._connections += [connection]
    
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
        self._command_socket.send_multipart([command_tag.encode(), p])

    def register_command_handler(self, command, func, **kwargs):
        tag = "command:"+command
        self._register_handler(tag, func, **kwargs)
        self._command_handler.register(tag)
        self._signal_socket.setsockopt_string(zmq.SUBSCRIBE, tag)

    def trigger_event(self, event, id, *args, **kwargs):
        injected = kwargs.get("injected", "")
        scope = kwargs.get("scope", "global")
        groups = kwargs.get("groups", None)
        session = kwargs.get("session", None)
        event_message = {'event':event, 'id':id, 'args':args, "injected":injected, "scope":scope, "groups":groups, "session":session}
        #jsonres = json.dumps(event_message)
        p = pickle.dumps(event_message, -1)
        event_tag = "event:" + event + ":" + id
        package = [event_tag.encode(), p]
        self._event_socket.send_multipart(package)
        
        if scope == "global":
            for connection in self._connections:
                connection.send_package(package)

    def register_event_handler(self, event, func, **kwargs):
        tag = "event:"+event
        tag_id = kwargs.get("id", None)
        if tag_id:
            tag += ":" + tag_id
        self._register_handler(tag, func, **kwargs)
        self._event_handler.register(tag)
        self._signal_socket.setsockopt_string(zmq.SUBSCRIBE, tag)

    def add_response_event(self, event):
        self.response_list += [event]

    def resolve_response(self, message):
        for event in self.response_list:
            if event["id"] == message["id"]:
                event["response"] = message["response"]
                event["eventSignal"].set()
    
    def send_query(self, query, *args, **kwargs):
        self._query_id_count += 1
        injected = kwargs.get("injected", "")
        scope = kwargs.get("scope", "global")
        groups = kwargs.get("groups", None)
        session = kwargs.get("session", None)
        query_message = {'query':query, "id":uuid_handler, "responseAddress": self._signal_address, 'args':args, "injected":injected, "scope":scope, "groups":groups, "session":session}
        jsonres = json.dumps(query_message)
        p = pickle.dumps(query_message, -1)
        query_tag = "query:" + query
        self._query_socket.send_multipart([query_tag.encode(), p])
        query_id, json_result = self._query_socket.recv_multipart()
        result = pickle.loads(json_result)

        return result

    def register_query_handler(self, query, func, **kwargs):
        self._register_handler("query:"+query, func, **kwargs)

S = None
def _init_spine(spine_port, root_address = None, ip = "127.0.0.1"):
    global S
    S = ZMQBus()
    S.reset_bus(spine_port, ip, root_address)
    

def Spine():
    #print("S", S)
    return S