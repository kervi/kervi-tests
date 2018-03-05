
if __name__ == '__main__':
    from kervi.module import Module
    APP_MODULE = Module({
        "application": {
            "id": "app_1"
        },
        "module":{
            "id":"module.id",
            "name":"Module name",
            "app_connection_local": False
        },
        "log":{
            "file":"kervi-module.log"
        },
        "network":{
            "ip": "127.0.0.1",
            "module_port": "9600",
            "ipc_root_port": 9500,
            "ipc_root_address": "127.0.0.1"
        },
        "routing":{
            "kervi_io":{
                "enabled": False,
                "address": "127.0.0.1",
                "port": 5672,
                "api_key": "api_key_1"
            }
        }
    })

    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.module", "module dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("panel", columns=2, rows=2, title="Panel dashboard"))

    from kervi.sensors.sensor import Sensor
    from kervi.devices.platforms.common.sensors.memory_use import MemUseSensorDeviceDriver
    SENSOR_1 = Sensor("MemLoadSensor", "MEM", MemUseSensorDeviceDriver())
    #link to sys area top right
    SENSOR_1.link_to_dashboard("*", "sys-header")
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="value", size=2, link_to_header=True)
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="chart", size=2)

    APP_MODULE.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Module shutdown")


    APP_MODULE.run()