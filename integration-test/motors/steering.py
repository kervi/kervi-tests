if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.ctrl", "Controller Buttons", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("steering", columns=3, rows=3, title="steering"))
    DASHBOARD.add_panel(DashboardPanel("ctrl", columns=3, rows=4, title="Controller"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

     #Create a streaming camera server
    from kervi.camera import CameraStreamer
    CAMERA = CameraStreamer("cam1", "camera 1")
    #link camera as background
    CAMERA.link_to_dashboard("dashboard.ctrl")

    from kervi.sensor import Sensor
    from kervi_devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
    from kervi_devices.platforms.common.sensors.memory_use import MemUseSensorDeviceDriver

    CPU_SENSOR = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
    CPU_SENSOR.store_to_db = False
    CPU_SENSOR.link_to_dashboard("*", "header_right")
    CPU_SENSOR.link_to_dashboard("*", "footer_left")
    CPU_SENSOR.link_to_dashboard("*", "footer_center")
    CPU_SENSOR.link_to_dashboard("*", "footer_right")

    MEM_SENSOR = Sensor("MemLoadSensor", "Memory", MemUseSensorDeviceDriver())
    MEM_SENSOR.store_to_db = False
    MEM_SENSOR.link_to_dashboard("*", "header_right")

    #Setup steering
    from kervi.steering import MotorSteering
    from kervi.devices.motors.dummy_motor_driver import DummyMotorBoard

    from kervi.devices.motors.LN298 import LN298DeviceDriver
    MOTOR_BOARD = DummyMotorBoard()
    STEERING = MotorSteering("steering", "motor steering")
    STEERING.adaptive_speed.set_ui_parameter("tick", .01)
    STEERING.adaptive_speed.persist_value = True
    STEERING.adaptive_speed.max = 10
    STEERING.adaptive_speed.min = -10
    STEERING.link_to_dashboard("dashboard.ctrl", "steering")

    STEERING.speed.link_to_dashboard("dashboard.ctrl", "left_pad_y")
    STEERING.direction.link_to_dashboard("dashboard.ctrl", "left_pad_x")

    STEERING.outputs["left_speed"].link_to(MOTOR_BOARD.dc_motors[0].speed, lambda x: -2*x)
    STEERING.outputs["right_speed"].link_to(MOTOR_BOARD.dc_motors[1].speed)

    MOTOR_BOARD.dc_motors[2].speed.link_to_dashboard("dashboard.ctrl", "right_pad_x", pad_auto_center=True)
    MOTOR_BOARD.dc_motors[3].speed.link_to_dashboard("dashboard.ctrl", "right_pad_y")


    MOTOR_BOARD.servo_motors[0].position.link_to(CAMERA.pan)
    MOTOR_BOARD.servo_motors[0].position.link_to(CAMERA.tilt)

    APP.run()
