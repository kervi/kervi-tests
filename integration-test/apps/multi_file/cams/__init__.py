""" include the cam modules here"""

from kervi.vision.camera import CameraStreamer
CAMERA = CameraStreamer("cam1", "camera 1", "zip_streamer", zip_file="C:/Users/tim/Downloads/example_01.zip")
CAMERA.link_to_dashboard("app")
CAMERA.link_to_dashboard("system", "cam1")
CAMERA.link_to_dashboard("system", "cam2")
