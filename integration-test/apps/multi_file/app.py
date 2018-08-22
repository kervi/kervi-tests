""" My kervi application """
from kervi.application import Application
import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    APP = Application({
        "application":{
            "id":"app_1",
            "name":"Test multi file app",
            "appKey":"1234",
        },
        "modules":["sensors", "controllers", "cams"],
        "network":{
            "ip": "127.0.0.1",
            "ipc_root_address": "127.0.0.1"
        },
        "authentication":{
            "users":{
                "admin": {
                    "email":"tim@wentzlau.dk"
                }
            }
        },
        "display":{
            "unit_systems":{
                "default": "metric",
            }
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

    APP.run()
