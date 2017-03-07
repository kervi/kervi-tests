if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.app", "app dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("button", columns=2, rows=4, title="button Width 0"))
    

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller, UIButtonControllerInput

    
    APP.run()