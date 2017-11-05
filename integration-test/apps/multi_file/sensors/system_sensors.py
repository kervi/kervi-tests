# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

""" Module that defines core cpu sensors """

from kervi.sensor import Sensor
from kervi_devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
from kervi_devices.platforms.common.sensors.memory_use import MemUseSensorDeviceDriver
from kervi_devices.platforms.common.sensors.disk_use import DiskUseSensorDeviceDriver
from kervi_devices.platforms.common.sensors.cpu_temp import CPUTempSensorDeviceDriver

CPU_SENSOR = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
CPU_SENSOR.store_to_db = False
CPU_SENSOR.link_to_dashboard("*", "header_right")
CPU_SENSOR.link_to_dashboard("system", "cpu", type="value", link_to_header=True)
CPU_SENSOR.link_to_dashboard("app", "sensors", type="value")
CPU_SENSOR.link_to_dashboard("system", "cpu", type="chart", label=None, chart_buttons=None, chart_grid=None)

MEM_SENSOR = Sensor("MemLoadSensor", "Memory", MemUseSensorDeviceDriver())
MEM_SENSOR.store_to_db = False
MEM_SENSOR.link_to_dashboard("*", "header_right")
MEM_SENSOR.link_to_dashboard("system", "memory", type="value", link_to_header=True)
# MEM_SENSOR.link_to_dashboard("app", "sensors", type="value")
MEM_SENSOR.link_to_dashboard("system", "memory", type="chart", chart_interval="5min", label=None)

DISK_SENSOR = Sensor("DiskUseSensor", "Disk", DiskUseSensorDeviceDriver())
DISK_SENSOR.store_to_db = False
DISK_SENSOR.link_to_dashboard("*", "sys-header")
DISK_SENSOR.link_to_dashboard("system", "disk", type="vertical_linear_gauge", size=5)

#build in sensor that measures cpu temperature
SENSOR_CPU_TEMP = Sensor("CPUTempSensor", "CPU T", CPUTempSensorDeviceDriver())
#link to sys area top right
SENSOR_CPU_TEMP.link_to_dashboard("*", "sys-header")