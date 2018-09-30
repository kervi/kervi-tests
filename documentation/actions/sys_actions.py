if __name__ == '__main__':
        from kervi.application import Application
        APP = Application()

        APP.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Device shutdown")
        APP.actions.reboot.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Device Reboot")
        APP.actions.restart.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="App restart")
        APP.actions.stop.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="App stop")

        APP.run()