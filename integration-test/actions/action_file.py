
from kervi.actions import action, Actions

@action
def action_4(p1, p2):
    print("action_4", p1, p2)
    Actions["test.action_1"]("a", "b")