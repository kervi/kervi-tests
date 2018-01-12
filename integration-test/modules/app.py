if __name__ == '__main__':
    from kervi.application import Application
    APP = Application(
        {
            "info":{
                "id":"app",
                "name":"Test multi file app",
                "appKey":"",
            },
            "network":{
                "IPAddress": "127.0.0.1",
                "IPRootAddress": "127.0.0.1",
                "IPCRootPort":9500,
                "WebSocketPort":9000,
                "WebPort": 8080,
                "IPCSecret":b"fd9969b3-9748-46b6-a69d-119ec2773352",
                
            },
        }
    )

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.app", "app dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("cpu", columns=2, rows=4, title=None))


    from kervi.sensors.sensor import Sensor
    from kervi.devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
    SENSOR_1 = Sensor("CPULoadSensor", "CPU", CPULoadSensorDeviceDriver())
    #link to sys area top right
    SENSOR_1.link_to_dashboard("*", "sys-header")
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_1.link_to_dashboard("dashboard.app", "cpu", type="value", size=2, link_to_header=True)
    SENSOR_1.link_to_dashboard("dashboard.app", "cpu", type="chart", size=2)

    APP.run()