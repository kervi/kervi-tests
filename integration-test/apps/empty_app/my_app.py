if __name__ == '__main__':

    from kervi.application import Application
        
    app = Application({
        "network":{
            "ip": "127.0.0.1",
            "ipc_root_address": "127.0.0.1",
            "ws_port": 9000,
        }        
    })
    app.run()