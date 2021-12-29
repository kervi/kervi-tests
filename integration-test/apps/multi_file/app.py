""" My kervi application """
from kervi.application import Application
import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    APP = Application({
        "development":{
            "debug_threads": False
        },
        "application":{
            "id":"app_1",
            "name":"Test multi file app",
            "appKey":"1234",
        },
        #"unit_system":  "us-imperial",
        "modules":["sensors", "controllers", "cams"],
        "network":{
            #"ip": "127.0.0.1",
            #"ipc_root_address": "127.0.0.1",
            #"ws_port": 9000,
        },
        "texts":{
            "ui":{
                "login":"Sign in"
            }
        },
        "plugins":{
            "kervi.plugin.authentication.plain": True,
            
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
            
        },
        "plain_users": {
            "anonymous":{
                "enabled": True,
                "groups":[]
            },
            "admin":{
                "enabled": True,
                "password":"1234",
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
        }
    })
    APP.actions.reboot.link_to_dashboard("*", "header_right")
    APP.run()
