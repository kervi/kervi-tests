""" Sample controller """
from kervi.controllers import Controller
from kervi.values import NumberValue, BooleanValue
from kervi.actions import action

class FanController(Controller):
    def __init__(self):
        Controller.__init__(self, "fan_controller", "Fan")
        
        self.type = "fan"

        self.temp = self.inputs.add_number(
            "temp",
            min=0,
            max=150,
            unit="c"
            
        )
        
        # self.temp = self.inputs.add("temp", "Temperature", NumberValue)
        # self.temp.min = 0
        # self.temp.max = 150
        # self.temp.unit = "c"

        self.trigger_temp = self.inputs.add("trigger_temp", "Trigger temperature f", NumberValue)
        self.trigger_temp.min = 0
        self.trigger_temp.max = 100
        self.trigger_temp.unit = "c"
        #remember the value when app restarts
        self.trigger_temp.persist_value = True

        self.max_temp = self.inputs.add("max_temp", "Max speed temperature", NumberValue)
        self.max_temp.min = 0
        self.max_temp.max = 100
        self.max_temp.unit = "c"
        #remember the value when app restarts
        self.max_temp.persist_value = True

        self.active = self.inputs.add("active", "Active", BooleanValue)
        self.active.value = False
        self.active.persist_value = True

        self.fan_speed = self.outputs.add("fan_speed", "Fanspeed", NumberValue)
        self.fan_on = self.outputs.add("fan_on", "Fan on", BooleanValue)

    @action(owner_class="FanControllerX")
    #@schedule(every_minutes=10, every_hour=5, every_day_at)
    def ctrl_action(self):
        print("ctrl_action")
        self.inter
    
    def on_start(self):
        print("my controller is started")

    def input_changed(self, changed_input):
        #print(changed_input)
        if self.active.value:
            temp = self.temp.value - self.trigger_temp.value
            if temp <= 0:
                self.fan_speed.value = 0
            else:
                max_span = self.max_temp.value - self.trigger_temp.value
                speed = (temp / max_span) * 100
                if speed > 100:
                    speed = 100
                self.fan_speed.value = speed
            self.fan_on.value = self.fan_speed.value > 0
        else:
            self.fan_speed.value = 0
            self.fan_on.value = False

FAN_CONTROLLER = FanController()

#link the fan controllers temp input to cpu temperature sensor
#The temp sensor is loaded in another process and linked via its id
FAN_CONTROLLER.temp.link_to("CPUTempSensor")
FAN_CONTROLLER.temp.link_to_dashboard("app", "fan")

FAN_CONTROLLER.temp.every().minute.at(":00").set(0)
FAN_CONTROLLER.temp.every().minute.at(":15").set(20)
FAN_CONTROLLER.temp.every().minute.at(":30").set(40)
FAN_CONTROLLER.temp.every().minute.at(":45").set(60)

#link the other fan controller inputs to dashboard
FAN_CONTROLLER.trigger_temp.link_to_dashboard("app", "fan")
FAN_CONTROLLER.max_temp.link_to_dashboard("app", "fan")
FAN_CONTROLLER.active.link_to_dashboard("app", "fan", button_width="100px")
FAN_CONTROLLER.fan_speed.link_to_dashboard("app", "fan")
FAN_CONTROLLER.fan_on.link_to_dashboard("app", "fan")