import ibmiotf.application

import time
from datetime import datetime, timedelta

from functools import partial
from threading import Thread
from tornado import gen

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc

import math

#save curdoc
doc = curdoc()

#coldstart visualization
coldstart_data = {'a':[0], 'b':[0],'c':[0], 'd':[0],'e':[0],'f':[0],'g':[0],'h':[0],'latitude':[51.749499], 'longitude':[-1.268661]}
coldstart_data["deviceid"] = [""]
time_coldstart = datetime.now() - timedelta(hours=1)
coldstart_data["eventtime"] = [time_coldstart.strftime("%Y-%m-%d %H:%M:%S")]
coldstart_data["eventtime_dt"] = [datetime.strptime(coldstart_data["eventtime"][0], "%Y-%m-%d %H:%M:%S")]


ds = ColumnDataSource(data=coldstart_data)

fig_plot = figure(plot_width=800, plot_height=650, x_axis_type='datetime')
fig_plot.title.text = 'Sensors readings from dev1'

fig_plot.xaxis.major_label_orientation = math.pi/4

fig_plot.line(x='eventtime_dt', y='a', source=ds, line_color="red",line_width=2,alpha=0.8)
fig_plot.line(x='eventtime_dt', y='b', source=ds, line_color="blue",line_width=2,alpha=0.8)
fig_plot.line(x='eventtime_dt', y='c', source=ds, line_color="green",line_width=2,alpha=0.8)
fig_plot.line(x='eventtime_dt', y='d', source=ds, line_color="orange",line_width=2,alpha=0.8)
fig_plot.line(x='eventtime_dt', y='e', source=ds, line_color="black",line_width=2,alpha=0.8)
fig_plot.line(x='eventtime_dt', y='f', source=ds, line_color="yellow",line_width=2,alpha=0.8)
fig_plot.line(x='eventtime_dt', y='g', source=ds, line_color="purple",line_width=2,alpha=0.8)
fig_plot.line(x='eventtime_dt', y='h', source=ds, line_color="brown",line_width=2,alpha=0.8)



@gen.coroutine
def update(new_data):
    #print("stream new data to plot")
    ds.stream(new_data)


##conect to Bluemix
org = "******"
appid = "visapp"
token = "*************"
devtype ="dev_rpi3"
api_key = "****************"


def myAppEventCallback(event):

    data = event.data
    data["deviceid"] = event.deviceId
    data["eventtime"] = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    data["eventtime_dt"] = datetime.strptime(data["eventtime"], "%Y-%m-%d %H:%M:%S")

    print(data)

    if data["deviceid"]  == 'dev1':
        new_data = {'a': [data["a"]], 'b': [data["b"]], 'c': [data["c"]], 'd': [data["d"]], 'e': [data["e"]], 'f': [data["f"]],
                    'g': [data["g"]], 'h': [data["h"]],
                    'latitude': [data["latitude"]], 'longitude': [data["longitude"]],
                    "deviceid": [data["deviceid"]],"eventtime": [data["eventtime"]], "eventtime_dt": [data["eventtime_dt"]]}

        print("received new data")
        # but update the document from callback
        doc.add_next_tick_callback(partial(update, new_data = new_data))



def blocking_task():
    appOptions = {"org": org, "id": appid, "auth-method": "token", "auth-key": api_key, "auth-token": token}
    appCli = ibmiotf.application.Client(appOptions)

    appCli.connect()
    print("connected")
    appCli.subscribeToDeviceEvents(deviceType=devtype, event="sensors_reading")
    appCli.deviceEventCallback = myAppEventCallback

    print("while true")
    while True:
        time.sleep(1)



thread = Thread(target=blocking_task)
thread.start()



curdoc().add_root(fig_plot)




