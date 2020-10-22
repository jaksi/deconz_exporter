import argparse
from os import makedirs, path
from time import sleep

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key_file", default="api_key")
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
    print(requests.get(f"{api_path}/{api_key}/sensors").json())


if __name__ == "__main__":
    main()
