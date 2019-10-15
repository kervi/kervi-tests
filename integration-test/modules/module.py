import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    from kervi.module import Module
    APP_MODULE = Module({
        "info":{
            "id":"module.id",
            "name":"Module name"
        },
        "log":{
            "file":"kervi-module.log"
        },
        "network" : {
            "ipc_root_port": 9500,
            "ipc_root_address": "127.0.0.1"
        }
        
    })

    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.module", "module dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("panel", columns=2, rows=2, title="Panel dashboard"))

    from kervi.sensors import Sensor
    from kervi.devices.sensors.system import MemoryUseSensorDeviceDriver
    SENSOR_1 = Sensor("MemLoadSensor", "MEM", MemoryUseSensorDeviceDriver())
    #link to sys area top right
    SENSOR_1.link_to_dashboard("*", "sys-header")
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="value", size=2, link_to_header=True)
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="chart", size=2)

    APP_MODULE.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Module shutdown")


    from kervi.streams import stream_observer
    from kervi.streams import stream_images, stream_observer
    from kervi.vision.region import region_observer, Region, Regions
    from imutils.video import VideoStream

    import datetime
    import imutils
    import time
    import cv2 
    import numpy as np

    firstFrame = None
    firstPicture = True
    lastRegion = None

    @stream_observer(stream_id="cam1")
    def my_observer(this_observer, stream_event, stream_data):
        
        global firstFrame, firstPicture, lastRegion
        if not stream_data:
            return
        #stream_images("xx", stream_data)
        nparr = np.fromstring(stream_data, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        frame = imutils.resize(img_np, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
        else:
            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
        
            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 2000:
                    continue
        
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            
                Regions.clear()
                Region("motion", "cam1", x, y, caption="Occupied", width=w, height=h)
                # show the frame and record if the user presses a key
                #if firstPicture:
                #    firstPicture = False
            #cv2.imshow("Security Feed", frame)
            return_frame = cv2.imencode(".jpg", frame)[1].tostring()
            return return_frame



    APP_MODULE.run()