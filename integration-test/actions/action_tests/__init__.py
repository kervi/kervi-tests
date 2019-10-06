
from kervi.actions import action
import time
from kervi.config import Configuration
@action(action_id="a.b.c")
def action_4(p1, p2, **kwargs):
    print("action_4 (a.b.c)", p1, p2, kwargs)
    return (p1, p2)

terminate = False
@action
def action_4_x():
    print("action_4_x start", Configuration.modules)
    
    while not terminate:
        time.sleep(.1)

    print("action_4_x done")

@action_4_x.set_interrupt
def _4_x(x):
    global terminate
    terminate = True
    print("action_4_x interupt", x)