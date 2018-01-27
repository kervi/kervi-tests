if __name__ == '__main__':
    import time
    from kervi.application import Application

    APP = Application()
    
    from kervi.dashboards import Dashboard, DashboardPanel
    Dashboard(
        "app",
        "App",
        [
            DashboardPanel("gate", title="Gate")
        ],
        is_default=True
    )

    Dashboard(
        "settings",
        "Settings",
        [
            DashboardPanel("gate", width="200px", title="Gate")
        ]
    )

    from kervi.controllers.controller import Controller
    from kervi.actions import action, Actions
    from kervi.values import DynamicNumber, DynamicBoolean
    
    class GateController(Controller):
        def __init__(self, controller_id="gate_controller", name="Gate controller"):
            super().__init__(controller_id, name)

            self.gate_speed = self.inputs.add("speed", "Gate speed", DynamicNumber)
            self.gate_speed.value = 100
            self.gate_speed.min = 0
            self.gate_speed.persist_value = True

            self.lo_end_stop = self.inputs.add("lo_end_stop", "low end stop", DynamicBoolean)
            self.hi_end_stop = self.inputs.add("hi_end_stop", "High end stop", DynamicBoolean)

            self.gate_motor_speed = self.outputs.add("gate_motor_speed", "Gate motor speed", DynamicNumber)

            self._stop_move = False

        @action(name="Move gate")
        def move_gate(self, open=True):
            if open:
                print("open gate")
                if not self.hi_end_stop.value:
                    self._stop_move = False
                    self.gate_motor_speed.value = self.gate_speed.value
                    while not self._stop_move and not self.hi_end_stop.value:
                        time.sleep(0.1)
                    self.gate_motor_speed.value = 0
                if self.hi_end_stop.value:
                    print("Gate open")
                else:
                    print("Gate stopped")
            else:
                print("close gate:")
                if not self.lo_end_stop.value:
                    self._stop_move = False
                    self.gate_motor_speed.value = -1 * self.gate_speed.value
                    while not self._stop_move and not self.lo_end_stop.value:
                        time.sleep(0.1)
                    self.gate_motor_speed.value = 0
                if self.lo_end_stop.value:
                    print("Gate closed")
                else:
                    print("Gate stopped")

        @move_gate.set_interupt
        def interupt_move_gate(self):
            print("stop move")
            self._stop_move = True

        @action(name="Stop gate")
        def stop_gate(self):
            print("stop gate:")
            self._stop_move = True

        def on_start(self):
            print("gate controller is started")
            self.gate_motor_speed.value = 0

        def input_changed(self, changed_input):
            pass

    gate_controller = GateController()
    gate_controller.move_gate.link_to_dashboard("app", "gate", inline=True, button_text=None, button_icon="arrow-up", label=None, action_parameters=[True])
    gate_controller.move_gate.link_to_dashboard("app", "gate", inline=True, button_text=None, button_icon="arrow-down", label=None, action_parameters=[False])

    gate_controller.link_to_dashboard("settings", "gate")

    from kervi.devices.motors.dummy_motor_driver import DummyMotorBoard

    motor_board = DummyMotorBoard()
    gate_controller.gate_motor_speed.link_to(motor_board.dc_motors[0].speed)

    from kervi.hal import GPIO
    GPIO["GPIO2"].define_as_input()
    GPIO["GPIO3"].define_as_input()

    gate_controller.lo_end_stop.link_to(GPIO["GPIO2"])
    gate_controller.hi_end_stop.link_to(GPIO["GPIO3"])

    APP.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Reboot")

    APP.run()