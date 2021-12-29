from kervi.application import Application

APP = Application()

from kervi.actions import action
from kervi.devices.motors.LN298 import LN298DeviceDriver
from kervi.hal import GPIO

motor_controller = LN298DeviceDriver(None, GPIO[12], GPIO[11], None, GPIO[13], GPIO[15])
motor = motor_controller.stepper_motors[0]
@action()
def test_forward():
    print("forward")
    motor.speed.value = 10
    motor.position.value = 10
    motor.step(4000, 0.01, 2, step_async=True)

@test_forward.set_interrupt()
def test_forward_interrupt():
    print("fwi")
    motor.stop()

@action()
def test_backward():
    print("backward")
    motor.step(-4000, 0.01, 1, step_async=True)
    print("backward done")

@test_backward.set_interrupt()
def test_backward_interrupt():
    print("bwi")
    motor.stop()



test_forward.link_to_dashboard()
test_backward.link_to_dashboard()


APP.run()