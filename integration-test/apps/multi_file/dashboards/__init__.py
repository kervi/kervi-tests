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
                DashboardPanel("fan", width=40, title="Light"),
                DashboardPanel("sensors", width=20, title="Sensors"),
                DashboardPanel("log", width=40, title="Log", user_log=True)
            ]
        ),
        DashboardPanelGroup(
            [
                DashboardPanel("fan", width=20, title="Light"),
                DashboardPanel("sensors", width=20, title="Sensors"),
                DashboardPanel("log", width=60, title="Log", user_log=True)
            ]
        ),

    ],
    is_default=True
)

SYSTEM_DASHBOARD = Dashboard(
    "system",
    "System",
    panels=[
        DashboardPanelGroup(
            [
                DashboardPanel("cpu", columns=2, rows=2),
                DashboardPanel("memory", columns=2, rows=2),
                DashboardPanel("disk", columns=1, rows=2)
            ]
        ),
        DashboardPanel("power", columns=2, rows=2, title="Power"),
        DashboardPanel("log", columns=2, rows=2, title="Log", user_log=True)
    ]
)
