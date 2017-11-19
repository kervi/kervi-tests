from kervi.application import Application
import time



if __name__ == '__main__':
    def module_loaded(module_name):
        print("module:", module_name)    

    app = Application()
    app.spine.register_event_handler("moduleLoaded", module_loaded)

    app._xrun()

    process_info = app.spine.send_query("getProcessInfo")
    print("pi", process_info)
    time.sleep(10)
    
    app.stop()
