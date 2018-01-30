""" My kervi application """
from kervi.application import Application
import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    APP = Application()

    APP.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Reboot")
    APP.actions.shutdown.user_groups=["admin"]


    APP.run()
