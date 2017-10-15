if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.ctrl", "PCF8591 test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("input", columns=2, rows=4, title="input"))

    #define a light controller
    from kervi.controller import Controller
    from kervi.values import *
    from kervi_devices.gpio import PCF8591

    gpio = PCF8591.PCF8591Driver(0x48, 1)
    gpio["AIN0"].link_to_dashboard("dashboard.ctrl", "input")


    APP.run()