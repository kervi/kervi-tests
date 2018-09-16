if __name__ == '__main__':
    from kervi.application import Application
    APP = Application({
        "network":{
            "ip": "127.0.0.1"
        }
    })
    APP.run()