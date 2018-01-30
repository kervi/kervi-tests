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
        "modules":["sensors", "controllers", "cams"]
    })

    APP.run()
