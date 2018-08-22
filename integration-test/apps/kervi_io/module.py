
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
            #"ip": "127.0.0.1",
            #"ip_module_port": 9600,
            "ipc_root_port": 9800,
            #"ipc_root_address": "127.0.0.1"
        },
        "routing":{
            "kervi_io":{
                "enabled": True,
                "address": "mq.kervi.io",
                "port": 5671,
                "api_user": "86a2a8aa634d42a09b90e2eb6390cbf6",
                "api_password": "5f0b164f424040658264af22c0d8f14a",
                "api_channel": "20bddf88a4434e99ba0e014de2b875c7"
            }
        }
    })

    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.module", "module dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("panel", columns=2, rows=2, title="Panel dashboard"))

    from kervi.sensors.sensor import Sensor
    from kervi.devices.platforms.common.sensors.memory_use import MemUseSensorDeviceDriver
    SENSOR_1 = Sensor("module_MemLoadSensor", "MEM", MemUseSensorDeviceDriver())
    #link to sys area top right
    SENSOR_1.link_to_dashboard("*", "sys-header")
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="value", size=2, link_to_header=True)
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="chart", size=2)

    APP_MODULE.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Module shutdown")


    APP_MODULE.run()