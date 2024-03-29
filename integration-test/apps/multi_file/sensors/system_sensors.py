# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

""" Module that defines core cpu sensors """

from kervi.sensors import Sensor
from kervi.devices.sensors.system import CPULoadSensorDeviceDriver
from kervi.devices.sensors.system import MemoryUseSensorDeviceDriver
from kervi.devices.sensors.system import DiskUseSensorDeviceDriver
from kervi.devices.sensors.system import CPUTempSensorDeviceDriver

CPU_SENSOR = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
CPU_SENSOR.link_to_dashboard("*", "header_right")
CPU_SENSOR.link_to_dashboard("system", "cpu", type="value", size=2, link_to_header=True)
CPU_SENSOR.link_to_dashboard("app", "sensors", type="value")
CPU_SENSOR.link_to_dashboard("system", "cpu", type="chart", chart_type="line", chart_title=None, chart_x_axis=False, chart_grid=False)

CPU_SENSOR.link_to_dashboard(type="value", size=2, link_to_header=True)
CPU_SENSOR.link_to_dashboard(type="chart")
   
CPU_SENSOR.user_groups = ["admin"]

MEM_SENSOR = Sensor("MemLoadSensor", "Memory", MemoryUseSensorDeviceDriver(), user_groups = ["admin"])
MEM_SENSOR.store_to_db = False
MEM_SENSOR.link_to_dashboard("*", "header_right")
MEM_SENSOR.link_to_dashboard("system", "memory", type="value", size=2, link_to_header=True)
MEM_SENSOR.link_to_dashboard("system", "memory", type="chart", size=2)

DISK_SENSOR = Sensor("DiskUseSensor", "Disk", DiskUseSensorDeviceDriver())
DISK_SENSOR.store_to_db = False
DISK_SENSOR.link_to_dashboard("*", "sys-header")
DISK_SENSOR.link_to_dashboard("system", "disk", type="vertical_linear_gauge", size=2)

#build in sensor that measures cpu temperature
SENSOR_CPU_TEMP = Sensor("CPUTempSensor", "CPU T", CPUTempSensorDeviceDriver())
#link to sys area top right
SENSOR_CPU_TEMP.link_to_dashboard("*", "sys-header")