if __name__ == '__main__': # this line is important in windows
    from kervi.application import Application
    app = Application({
        "network":{
            "ip": "127.0.0.1",
            "ipc_root_address": "127.0.0.1"
        }
    })
    import layout
    import simple_link
    app.run()