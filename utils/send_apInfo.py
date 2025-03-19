import requests
import json

def send_apInfo(aps):
    apInfo = {}
    for ap in aps:
        intfInfo = []
        ports = ap.ports

        # 遍历字典，获取接口名与端口号的对应关系
        for intf, port in ports.items():
            if port != 0:
                print(f"Interface: {intf.name}, Port: {port}")
                intfInfo.append({
                "name": intf.name,
                "port": port,
                "mac": ap.MAC(intf.name)
                })
        apInfo[ap.name] = intfInfo

        try:
            url = "http://127.0.0.1:8000/process_apInfo"
            json_data = json.dumps(apInfo)
            response = requests.post(url, json_data)
            response.raise_for_status()
            msg = response.json()["msg"]
            print(msg)
        except requests.exceptions.RequestException as e:
            print("Failed to send apInfo for FastAPI")

## Example: ap1-wlan2 -> ap1-mp2
def wlan_to_mesh(intfName):
    if intfName.find("wlan") == -1:
        exit("intfName should contail [wlan]")
    return intfName.replace("wlan", "mp")
