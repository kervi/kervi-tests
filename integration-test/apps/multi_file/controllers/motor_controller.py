#Setup steering
from kervi.controllers.steering import MotorSteering
from kervi.devices.motors.dummy_motor_driver import DummyMotorBoard

MOTOR_BOARD = DummyMotorBoard()
STEERING = MotorSteering("steering", "motor steering")
STEERING.adaptive_speed.set_ui_parameter("tick", .01)
STEERING.adaptive_speed.persist_value = True
STEERING.adaptive_speed.max = 10
STEERING.adaptive_speed.min = -10
#STEERING.link_to_dashboard("dashboard.ctrl", "steering")

STEERING.speed.link_to_dashboard("app", "left_pad_y")
STEERING.direction.link_to_dashboard("app", "left_pad_x")

STEERING.outputs["left_speed"].link_to(MOTOR_BOARD.dc_motors[0].speed, lambda x: -2*x)
STEERING.outputs["right_speed"].link_to(MOTOR_BOARD.dc_motors[1].speed)

MOTOR_BOARD.dc_motors[2].speed.link_to_dashboard("app", "right_pad_x", pad_auto_center=True)
MOTOR_BOARD.dc_motors[3].speed.link_to_dashboard("app", "right_pad_y")
