if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("main", "Controller Buttons", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("gpio", columns=3, rows=3, title="GPIO"))


    from kervi.hal import GPIO

    GPIO["GPIO1"].define_as_input()
    GPIO["GPIO2"].define_as_output()

    GPIO["GPIO1"].link_to_dashboard("main", "gpio")
    GPIO["GPIO2"].link_to_dashboard("main", "gpio")


    APP.run()