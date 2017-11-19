# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

""" Module that defines core cpu sensors """

from kervi.sensor import Sensor
from kervi_devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
from kervi_devices.platforms.common.sensors.memory_use import MemUseSensorDeviceDriver
from kervi_devices.platforms.common.sensors.disk_use import DiskUseSensorDeviceDriver
from kervi_devices.platforms.common.sensors.cpu_temp import CPUTempSensorDeviceDriver

CPU_SENSOR = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
CPU_SENSOR.link_to_dashboard("*", "header_right")
