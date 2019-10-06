if __name__ == '__main__':
    import time
    from kervi.application import Application

    APP = Application()

    from kervi.dashboards import Dashboard, DashboardPanel
    Dashboard(
        "app",
        "App",
        [
            DashboardPanel("gate", title="Gate")
        ],
        is_default=True
    )

    Dashboard(
        "settings",
        "Settings",
        [
            DashboardPanel("gate", width="200px", title="Gate")
        ]
    )
    
    from kervi.actions import action
    
    @action(name="Move gate")
    def move_gate(p1="p1d", **kwargs):
        print("Move gate", p1, kwargs.get("kw1", None))
        while not exit_action:
            print("in loop")
            time.sleep(1)
        print("move gate interrupted")

    terminate_my_action = False
    @action
    def my_action(p1="pd", **kwargs):
        global terminate_my_action
        print("my_action", p1, kwargs.get("kw1", None), time.ctime())
        terminate_my_action = False
        while not terminate_my_action:
            print("wait for terminate")
            time.sleep(1)
        print("my action done")

    @my_action.set_interrupt
    def my_action_interrupt():
        global terminate_my_action
        print("my_action interrupt", time.ctime())
        terminate_my_action = True
    
    move_gate.run_every().minute.at(":30").until(":35").do("P!", kw1=10)

    my_action.run_every().minute.at(":58").until(":02").do("P!x", kw1=20)
    #my_action.run_every(1).day.from("10:30").to().day.("10:35").do("P!", kw1=10)
    #my_action.run_every().minute.at(":15").do("P!x", kw1=20)

    move_gate.link_to_dashboard("app", "gate", type="switch", interrupt_enabled=True, inline=True, button_text="Move gate", button_icon="arrow-up", label=None)
    move_gate.link_to_dashboard("app", "gate", interrupt_enabled=True, inline=True, button_text="Move gate", button_icon="arrow-up", label=None)
    my_action.link_to_dashboard("app", "gate", interrupt_enabled=True, inline=True, button_text="My action", label=None)

    APP.run()