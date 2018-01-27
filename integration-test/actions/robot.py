if __name__ == '__main__':
    import time
    from kervi.application import Application

    APP = Application()

    from kervi.controllers.steering import MotorSteering
    from kervi.devices.motors.dummy_motor_driver import DummyMotorBoard

    motor_board = DummyMotorBoard()
    steering = MotorSteering()

    steering.left_speed.link_to(motor_board.dc_motors[0])
    steering.right_speed.link_to(motor_board.dc_motors[1])
    