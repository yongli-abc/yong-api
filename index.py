from flask import Flask, Response
from libpurecoollink.dyson import DysonAccount
from libpurecoollink.const import FanSpeed, FanMode, NightMode, Oscillation, \
    FanState, StandbyMonitoring, QualityTarget, ResetFilter, HeatMode, \
    FocusMode, HeatTarget
from config import config

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/dyson/start")
def dyson_start():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    dyson_account = DysonAccount(config["account"], config["password"], config["language"])
    logged = dyson_account.login()
    if not logged:
        response = Response(status=500)
    else:
        devices = dyson_account.devices()

        connected = devices[0].auto_connect()

        if not connected:
            response = Response(status=500)
        else:
            devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_2)
            devices[0].disconnect
            response = Response(status=200)

    return response

@app.route("/dyson/stop")
def dyson_stop():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    dyson_account = DysonAccount(config["account"], config["password"], config["language"])
    logged = dyson_account.login()
    if not logged:
        response = Response(status=500)
    else:
        devices = dyson_account.devices()

        connected = devices[0].auto_connect()

        if not connected:
            response = Response(status=500)
        else:
            devices[0].set_configuration(fan_mode=FanMode.OFF)
            devices[0].disconnect
            response = Response(status=200)

    return response

if __name__ == "__main__":
    app.debug = False
    app.run()