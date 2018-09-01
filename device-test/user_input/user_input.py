if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()


    from kervi.user_input import UserInput

    user_input = UserInput(listen_to_keyboard=True, listen_to_mouse=True)

    user_input.key.link_to_dashboard()
    user_input.mouse_x.link_to_dashboard()
    user_input.mouse_y.link_to_dashboard()
    user_input.mouse_wheel.link_to_dashboard()

    APP.run()