if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()
   

    from kervi.devices.gpio.dummy_gpio import GPIODummyDriver

    GPIO = GPIODummyDriver()

    GPIO["AIN0"].define_as_input()
    GPIO["AIN1"].define_as_input()
    GPIO["AIN2"].define_as_input()
    GPIO["AIN3"].define_as_input()

    GPIO["AIN0"].link_to_dashboard()
    GPIO["AIN1"].link_to_dashboard()
    GPIO["AIN2"].link_to_dashboard()
    GPIO["AIN3"].link_to_dashboard()

    GPIO["AOUT0"].define_as_input()
    GPIO["AOUT1"].define_as_input()
    GPIO["AOUT2"].define_as_input()
    GPIO["AOUT3"].define_as_input()

    GPIO["AOUT0"].link_to_dashboard()
    GPIO["AOUT1"].link_to_dashboard()
    GPIO["AOUT2"].link_to_dashboard()
    GPIO["AOUT3"].link_to_dashboard()

    APP.run()