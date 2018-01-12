import time

if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()
    
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard(
        "app",
        "App",
        [
            DashboardPanel("controller")
        ],
        is_default=True
    )

    from kervi.actions import action, Actions

    @action
    def action_1(p1, p2):
        print("action_1", p1, p2)

    from kervi.controllers.controller import Controller
    from kervi.actions import Actions
    from kervi.values import DynamicBoolean
    class TestClass(Controller):
        def __init__(self):
            super().__init__("tc", "test controller")

            self.active = self.inputs.add("active", "Active", DynamicBoolean)
            self.active.value = False

        @action
        def action_2(self, p1, **kwargs):
            print("action_2", p1)
            time.sleep(10)
            print("action_2 done")

        def on_start(self):
            print("my controller is started")
            Actions()["action_1"].execute("x1", 2)
            if not Actions()["action_2"].execute(3, timeout=15):
                print("a2 timeout")
            print("a2 state", Actions()["action_2"].state)

        def input_changed(self, changed_input):
            pass
    tc = TestClass()
    #tc.active.link
    APP.run()