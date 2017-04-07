""" Sample controller """
from kervi.controller import Controller
from kervi.values import *
from kervi.hal import GPIO
#Switch button shown on a dashboard
class LightController(Controller):
    def __init__(self):
        Controller.__init__(self, "lightController", "Light")
        self.type = "light"

        #define an input and link it to the dashboard panel
        self.inputs["on"] = DynamicBoolean("Light")
        self.inputs["on"].link_to_dashboard("app", "light", label_icon="light")

        self.inputs["level"] = DynamicNumber("Level")
        self.inputs["level"].min = 0
        self.inputs["level"].max = 100
        self.inputs["level"].value = 0
        self.inputs["level"].link_to_dashboard("app", "light")

        #define GPIO
        GPIO.define_as_pwm(12, 50)

    def input_changed(self, changed_input):
        self.user_log_message("changed_input:" + changed_input.component_id)
        if changed_input == self.inputs["on"]:
            if changed_input.value:
                GPIO.pwm_start(12)
            else:
                GPIO.pwm_stop(12)

        if changed_input == self.inputs["level"]:
            #change the duty_cycle on the pwm pin
            GPIO.pwm_start(12, duty_cycle=changed_input.value)

LightController()

