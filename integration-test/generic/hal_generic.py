if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard", "GPIO", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("gpio", columns=2, rows=4, title="GPIO Width 0"))
    DASHBOARD.add_panel(DashboardPanel("gpio_inline", columns=3, rows=4, title="button inline"))

    from kervi.hal import GPIO

    GPIO["GPIO1"].define_as_output()
    GPIO["GPIO1"].link_to_dashboard("dashboard", "gpio")

    GPIO["GPIO1"].pwm["duty_cycle"].link_to_dashboard("dashboard", "gpio")
    GPIO["GPIO1"].pwm["active"].link_to_dashboard("dashboard", "gpio")

    GPIO["DAC1"].link_to_dashboard("dashboard", "gpio")


    APP.run()