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

    from kervi.devices.motors.dummy_motor_driver import DummyMotorBoard

    motor_board = DummyMotorBoard()

    from kervi.hal import GPIO
    hi_switch = GPIO["GPIO2"]
    lo_switch = GPIO["GPIO3"]

    hi_switch.define_as_input()
    lo_switch.define_as_input()

    stop_move = False

    from kervi.actions import action
    @action(name="Move gate")
    def move_gate(open=True):
        global stop_move
        if open:
            print("open gate")
            if not hi_switch.value:
                stop_move = False
                motor_board.dc_motors[0].speed.value = 50
                while not stop_move and not hi_switch.value:
                    time.sleep(0.1)
                motor_board.dc_motors[0].speed.value = 0
            if hi_switch.value:
                print("Gate open")
            else:
                print("Gate stopped")
        else:
            print("close gate:")
            if not lo_switch.value:
                stop_move = False
                motor_board.dc_motors[0].speed.value = -50
                while not stop_move and not lo_switch.value:
                    time.sleep(0.1)
                motor_board.dc_motors[0].speed.value = 0
            if lo_switch.value:
                print("Gate closed")
            else:
                print("Gate stopped")

    @action(name="Stop gate")
    def stop_gate():
        global stop_move
        print("stop gate:")
        stop_move = True

    move_gate.link_to_dashboard("app", "gate", inline=True, button_text=None, button_icon="arrow-up", label=None, action_parameters=[True])
    move_gate.link_to_dashboard("app", "gate", inline=True, button_text=None, button_icon="arrow-down", label=None, action_parameters=[False])
    stop_gate.link_to_dashboard("app", "gate", inline=True, button_text=None, button_icon="stop", label=None)

    APP.run()