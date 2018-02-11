""" My kervi application """
from kervi.application import Application
import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    APP = Application({
        "application":{
            "id":"app",
            "name":"Test multi file app",
            "appKey":"1234",
        },
        "modules":["sensors", "controllers", "cams"],
        "network":{
            "ip": "127.0.0.1",
            "ip_root_address": "127.0.0.1"
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
                "default": "us-imperial",
            }
        }
    })

    APP.run()
