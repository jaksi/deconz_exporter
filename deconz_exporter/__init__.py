import argparse
from os import path
from time import sleep
from wsgiref.simple_server import make_server

import requests
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY, GaugeMetricFamily


class DeconzCollector:
    def __init__(self, api_path, api_key):
        self.api_path = api_path
        self.api_key = api_key

    def collect(self):
        temperature = GaugeMetricFamily(
            "deconz_temperature_celsius", "deCONZ temperature sensor data", labels=["name"]
        )
        humidity = GaugeMetricFamily(
            "deconz_humidity_ratio", "deCONZ humidity sensor data", labels=["name"]
        )
        pressure = GaugeMetricFamily(
            "deconz_pressure_pascals", "deCONZ pressure sensor data", labels=["name"]
        )
        for sensor in requests.get(f"{self.api_path}/{self.api_key}/sensors").json().values():
            if sensor["type"] == "ZHATemperature":
                temperature.add_metric([sensor["name"]], sensor["state"]["temperature"] / 100)
            elif sensor["type"] == "ZHAHumidity":
                humidity.add_metric([sensor["name"]], sensor["state"]["humidity"] / 10000)
            elif sensor["type"] == "ZHAPressure":
                pressure.add_metric([sensor["name"]], sensor["state"]["pressure"] * 100)
        yield temperature
        yield humidity
        yield pressure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key_file", default="api_key")
    parser.add_argument("--listen_host", default="")
    parser.add_argument("--listen_port", default=9759)
    args = parser.parse_args()
    device = requests.get("https://dresden-light.appspot.com/discover").json()[0]
    api_path = f"http://{device['internalipaddress']}:{device['internalport']}/api"
    if path.isfile(args.api_key_file):
        with open(args.api_key_file) as api_key_file:
            api_key = api_key_file.read()
    else:
        unlocked = False
        while not unlocked:
            response = requests.post(api_path, json={"devicetype": "deconz_exporter"})
            if response.status_code != 403:
                response.raise_for_status()
            if response.status_code == 200:
                unlocked = True
            else:
                print("Press the button")
                sleep(10)
        api_key = response.json()[0]["success"]["username"]
        with open(args.api_key_file, "w") as api_key_file:
            api_key_file.write(api_key)
    REGISTRY.register(DeconzCollector(api_path, api_key))
    app = make_wsgi_app(REGISTRY)
    httpd = make_server(args.listen_host, args.listen_port, app)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
