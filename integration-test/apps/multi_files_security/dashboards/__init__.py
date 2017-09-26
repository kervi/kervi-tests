""" bootstrap your kervi dashboards here """
from kervi.dashboard import Dashboard, DashboardPanel

#Create the dashboards for your Kervi application here.
#Standard dashboard with several panels where sensors are placed.
#Each sensor create links to one or more dashboard panels 
APP_DASHBOARD = Dashboard("app", "My dashboard", is_default=True)
APP_DASHBOARD.add_panel(DashboardPanel("fan", columns=3, rows=1, title="Light"))
APP_DASHBOARD.add_panel(DashboardPanel("sensors", columns=2, rows=1, title="Sensors"))
APP_DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=2, title="Log", user_log=True))

SYSTEM_DASHBOARD = Dashboard("system", "System")
SYSTEM_DASHBOARD.user_groups = ["admin"]
SYSTEM_DASHBOARD.add_panel(DashboardPanel("cpu", columns=2, rows=2))
SYSTEM_DASHBOARD.add_panel(DashboardPanel("memory", columns=2, rows=2))
SYSTEM_DASHBOARD.add_panel(DashboardPanel("disk", columns=1, rows=2))
SYSTEM_DASHBOARD.add_panel(DashboardPanel("cam", columns=2, rows=2))
POWER_PANEL = DashboardPanel("power", columns=2, rows=2, title="Power")
POWER_PANEL.user_groups = ["admin"]
SYSTEM_DASHBOARD.add_panel(POWER_PANEL)
SYSTEM_DASHBOARD.add_panel(DashboardPanel("log", columns=2, rows=2, title="Log", user_log=True))
