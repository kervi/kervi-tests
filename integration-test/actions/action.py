import time

if __name__ == '__main__':
    from kervi.application import Application
    APP = Application(
        {
          "modules":["action_tests"],
          "network":{
            "IPAddress": "127.0.0.1",
            "IPRootAddress": "127.0.0.1"
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

    from kervi.controllers.controller import Controller
    from kervi.actions import Actions
    from kervi.values import DynamicBoolean
    import action_file
    class TestClass(Controller):
        def __init__(self):
            super().__init__("tc", "test controller")

            self.active = self.inputs.add("active", "Active", DynamicBoolean)
            self.active.value = False

        @action(action_id="x.y")
        def action_2(self, p1, **kwargs):
            print("action_2", p1)
            self.active = True
            if p1==3:
                time.sleep(10)
            print("action_2 done")

        def on_start(self):
            print("my controller is started")
            self.action_2(4)
            action_1("x1a", 1)
            Actions["test.action_1"]("x1", 2)
            Actions["test.action_1"]("x1", 2)
            Actions["a.b.c"]("x3", 3)
            if not Actions["tc.x.y"](3, timeout=5):
                print("a2 timeout")
            print("a2 state", Actions["action_2"].state)
            Actions["action_4"]("a", 4)
        def input_changed(self, changed_input):
            print(changed_input)
            pass
    tc = TestClass()
    
    #tc.active.link
    APP.run()