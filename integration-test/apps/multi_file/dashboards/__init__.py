""" bootstrap your kervi dashboards here """
from kervi.dashboard import Dashboard, DashboardPanel, DashboardPanelGroup

#Create the dashboards for your Kervi application here.
#Standard dashboard with several panels where sensors are placed.
#Each sensor create links to one or more dashboard panels 
APP_DASHBOARD = Dashboard(
    "app",
    "My dashboard",
    [
        DashboardPanelGroup(
            [
                DashboardPanelGroup(
                    [
                        DashboardPanelGroup(
                            [
                                DashboardPanel("fan", width=70, title="Light"),
                                DashboardPanel("sensors", width=30, title="Sensors"),
                            ],
                            
                        ),
                        DashboardPanelGroup(
                            [
                                DashboardPanel("fan",  title="Light"),
                                DashboardPanel("sensors", title="Sensors"),
                                DashboardPanel("log", title="Log")
                            ],
                        ),
                    ],
                    width=60
                ),

                DashboardPanel("log", width=40, title="Log", user_log=True)
            ]
        ),
        
    ],
    is_default=True
)
# 
SYSTEM_DASHBOARD = Dashboard(
    "system",
    "System",
    panels=[
        DashboardPanelGroup(
            [
                DashboardPanel("cpu", width=40),
                DashboardPanel("memory", width=30),
                DashboardPanel("cam1", width=30),    
            ]
        ),
        DashboardPanel("disk", width=30),
        DashboardPanel("cam2", width=50),
        DashboardPanel("power", title="Power", width=20),
        DashboardPanel("log", title="Log", width=100, user_log=True)
    ]
)

from kervi.spine import Spine

s=Spine()
