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
        "unit_system":  "us-imperial",
        "modules":["sensors", "controllers", "cams"],
        "network":{
            "ip": "127.0.0.1",
            "ipc_root_address": "127.0.0.1"
        },
        "texts":{
            "ui":{
                "login":"Sign in"
            }
        },
        "plugins":{
            "authentication": {
                "kervi.plugin.authentication.plain": True
            },
            "messaging":{
                "kervi.plugin.messaging.email": {
                    "enabled": False,
                    "smtp": {
                        "sender_name": "Kervi",
                        "sender_address": "kervi@example.com",
                        "server": "localhost",
                        "port": "25",
                        "user": "",
                        "password": "",
                        "tls": False
                    }
                }
            }
        },
        "plain_users": {
            "anonymous":{
                "enabled": True,
                "groups":[]
            },
            "admin":{
                "enabled": True,
                "password":"",
                "groups":["admin"],
                "name": "Administrator",
                "addresses": {
                    "email": "admin@example.com",
                    "phone": ""
                }
            }
        },
        "messaging": {
            "default_channels": ["user_log"]
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
