import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    from kervi.bootstrap import ApplicationModule
    APP_MODULE = ApplicationModule({
        "info":{
            "id":"module.id",
            "name":"Module name"
        },
        "log":{
            "file":"kervi-module.log"
        },
        "network":{
            "IPAddress": nethelper.get_ip_address(),
            "IPRootAddress": nethelper.get_ip_address(),
            "IPCRootPort": 9500,
        }
    })

    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("module-dashboard", "module dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("panel", columns=2, rows=2, title="Panel dashboard"))

    APP_MODULE.run()