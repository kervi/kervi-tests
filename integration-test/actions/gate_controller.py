if __name__ == '__main__':
    import time
    from kervi.application import Application

    APP = Application({
        "network":{
        "ip": "127.0.0.1",
        "ipc_root_address": "127.0.0.1"
        }
    })
    
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

    from kervi.controllers import Controller
    from kervi.actions import action, Actions
    from kervi.values import NumberValue, BooleanValue


    class GPIOSimulator(Controller):
        def __init__(self, controller_id="gpio_simulator_controller", name="Gate controller"):
            super().__init__(controller_id, name)

            self.gpio1 = self.outputs.add("gpio1", "GPIO1", BooleanValue)
            self.gpio2 = self.outputs.add("gpio2", "GPIO2", NumberValue)
            self.gpio2_in = self.inputs.add("gpio2_in", "GPIO2", NumberValue)

            self.gpio3 = self.outputs.add("gpio3", "GPIO3", BooleanValue)
            self.gpio4 = self.outputs.add("gpio4", "GPIO4", BooleanValue)
            self.gpio3_in = self.inputs.add("gpio3_in", "GPIO3", BooleanValue)
            self.gpio4_in = self.inputs.add("gpio4_in", "GPIO4", BooleanValue)

            self.gpio5 = self.outputs.add("gpio5", "GPIO5", NumberValue)
            self.gpio5_in = self.inputs.add("gpio5_in", "GPIO5", NumberValue)


        def input_changed(self, input):
            if input == self.gpio2_in:
                self.gpio2.value = input.value
            if input == self.gpio3_in:
                self.gpio3.value = input.value
            if input == self.gpio4_in:
                self.gpio4.value = input.value

            if input == self.gpio5_in:
                self.gpio5.value = input.value

    class GateController(Controller):
        def __init__(self, controller_id="gate_controller", name="Gate controller"):
            super().__init__(controller_id, name)

            self.gate_speed = self.inputs.add("speed", "Gate speed", NumberValue)
            self.gate_speed.value = 100
            self.gate_speed.min = 0
            self.gate_speed.persist_value = True

            self.lo_end_stop = self.inputs.add("lo_end_stop", "low end stop", BooleanValue)
            self.hi_end_stop = self.inputs.add("hi_end_stop", "High end stop", BooleanValue)

            self.gate_motor_speed = self.outputs.add("gate_motor_speed", "Gate motor speed", NumberValue)

            #self._stop_move = False

        @action(name="Move gate")
        def move_gate(self, open=True, speed=None):
            if not speed:
                speed = self.gate_speed.value
            if open:
                print("open gate", open)
                if not self.hi_end_stop.value:
                    self.gate_motor_speed.value = speed
                    while not exit_action and not self.hi_end_stop.value:
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
                    self.gate_motor_speed.value = -1 * speed
                    while not exit_action and not self.lo_end_stop.value:
                        time.sleep(0.1)
                    self.gate_motor_speed.value = 0
                if self.lo_end_stop.value:
                    print("Gate closed")
                else:
                    print("Gate stopped")

        # @move_gate.set_interrupt
        # def interupt_move_gate(self, p1=None):
        #     print("stop move", p1)
        #     self._stop_move = True

        # @action(name="Stop gate")
        # def stop_gate(self):
        #     print("stop gate:")
        #     self._stop_move = True

        def controller_start(self):
            print("gate controller is started")
            self.gate_motor_speed.value = 0

        def input_changed(self, changed_input):
            pass

    gpio_simulator = GPIOSimulator()
    gpio_simulator.gpio1.link_to_dashboard()
    gpio_simulator.gpio2_in.link_to_dashboard()
    gpio_simulator.gpio3_in.link_to_dashboard()
    gpio_simulator.gpio4_in.link_to_dashboard()
    gpio_simulator.gpio5_in.link_to_dashboard()

    gate_controller = GateController()
    gate_controller.move_gate.link_to_dashboard("app", "gate", inline=True, button_text="open", button_icon="arrow-up", label=None, action_parameters=[True, 30], type="switch")
    gate_controller.move_gate.link_to_dashboard("app", "gate", inline=True, button_text="close", button_icon="arrow-up", label=None, action_parameters=[False, 40], type="switch")
    gate_controller.move_gate.link_to_dashboard("app", "gate", inline=True, button_text=None, button_icon="arrow-down", label=None, action_parameters=[True])

    gate_controller.move_gate.link_to(
        gpio_simulator.gpio1,
        action_parameters=[50],
        interrupt_parameters=["d"],
        pass_value = True
    )

    gate_controller.move_gate.link_to(
        "gpio_simulator_controller.gpio2_in",
        trigger_value = lambda x: x > 10,
        trigger_interrupt_value = lambda x: x < 10,
        #action_parameters=[50],
        interrupt_parameters=["d"],
        pass_value = True
    )

    Actions["gate_controller.move_gate"].link_to(
        "gpio_simulator_controller.gpio5",
        trigger_value = lambda x: x > 5,
        trigger_interrupt_value = lambda x: x < 5,
        #action_parameters=[50],
        interrupt_parameters=["d"],
        pass_value = True
    )

    gate_controller.link_to_dashboard("settings", "gate")

    from kervi.devices.motors.dummy_motor_driver import DummyMotorBoard

    motor_board = DummyMotorBoard()
    gate_controller.gate_motor_speed.link_to(motor_board.dc_motors[0].speed)

    gate_controller.lo_end_stop.link_to(gpio_simulator.gpio3)
    gate_controller.hi_end_stop.link_to(gpio_simulator.gpio4)

    APP.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Reboot")

    APP.run()