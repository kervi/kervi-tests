import time

if __name__ == '__main__':
    from kervi.application import Application
    APP = Application(
        {
          "modules": ["action_tests"],
          "network":{
            "ip": "127.0.0.1",
            "ip_root_address": "127.0.0.1"
          }
        }
    )
    
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard(
        "app",
        "App",
        [
            DashboardPanel("actions", width="200px")
        ],
        is_default=True
    )

    from kervi.actions import action, Actions
    interupt_action = False
    @action
    def action_start():
        print("action_start")
        while not interupt_action:
            time.sleep(0.1)
        print("action_start done")

    @action_start.set_interrupt
    def action_interupt():
        global interupt_action
        print("action interupt")
        interupt_action = True

    @action(name="Action 0")
    def action_0(p1=None):
        print("action_0 start", p1)
        time.sleep(5)
        print("action_0 stop")

    action_0.link_to_dashboard("app", "actions", button_text="1",  action_parameters=[1])
    action_0.link_to_dashboard("app", "actions", label="action 2", button_text="2", action_parameters=[2])

    @action(action_id="test.action_1")
    def action_1(p1, p2):
        print("action_1", p1, p2)
        return (p1, p2)

    from kervi.controllers import Controller
    from kervi.actions import Actions
    from kervi.values import BooleanValue
    import action_file
    import threading
    class TestClass(Controller):
        def __init__(self):
            super().__init__("tc", "test controller")

            self.active = self.inputs.add("active", "Active", BooleanValue)
            self.active.value = False

            self._action_x_interupt = False

        @action(action_id="x.y")
        def action_2(self, p1, **kwargs):
            print("action_2", p1)
            self.active = True
            if p1==3:
                time.sleep(10)
            print("action_2 done")
            return p1

        @action
        def action_x(self):
            print("action_x start")
            self._action_x_interupt = False
            while not self._action_x_interupt:
                time.sleep(.1)
            print("action_x done")


        @action_x.set_interrupt
        def action_x_interupt(self):
            print("action_x interupt")
            self._action_x_interupt = True

        def controller_start(self):
            action_start(run_async=True)

            self.action_x(run_async=True)
            Actions["action_4_x"](run_async=True)
            
            print("my controller is started")
            self.action_2(4)
            print("action_1 res:", action_1("x1a", 1))
            print("test.action_1 res:", Actions["test.action_1"]("x1", 2))
            print("test.action_1 res:", Actions["test.action_1"]("x1", 3))
            print("a.b.c res:", Actions["a.b.c"]("x3", 3, keyword="test"))
            try:
                print("tc.x.y res:", Actions["tc.x.y"](3, timeout=5))
            except TimeoutError:
                print("timeoutx in tc.x.y")
            print("tc.x.y timeout:",Actions["tc.x.y"].is_running)
            print("a2 state", Actions["action_2"].state)
            print("action_4 res:", Actions["action_4"]("a", 4))
            action_start.interrupt()
            self.action_x.interrupt()
            Actions["action_4_x"].interrupt("tx")

        def input_changed(self, changed_input):
            print(changed_input)
            pass
    tc = TestClass()
    
    #tc.active.link
    APP.run()