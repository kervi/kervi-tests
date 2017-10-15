""" My kervi application """
from kervi.application import Application
import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    APP = Application({
        "info":{
            "id":"app",
            "name":"Test multi file app",
            "appKey":"",
        },
        "modules":["sensors", "controllers", "cams"],
        "network":{
            "IPAddress": "localhost",
            "IPRootAddress": "localhost",
            "IPCRootPort":9500,
            "WebSocketPort":9000,
            "WebPort": 8080,
            "IPCSecret":b"fd9969b3-9748-46b6-a69d-119ec2773352",
            
        },
    })

    APP.run()
