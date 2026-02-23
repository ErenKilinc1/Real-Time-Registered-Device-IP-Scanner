import time
import urllib3
from ciscoaxl import axl
from zeep import Client, helpers
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CUCMScanner:
    def __init__(self, ip, username, password, version='12.5'):
        self.ip = ip
        self.username = username
        self.password = password
        self.version = version
        self.output_file = "cucm_registered_ips.txt"
        self.ucm = axl(username=self.username, password=self.password, cucm=self.ip, cucm_version=self.version)

    def get_device_list(self, model_filter=None):
        raw_phones = self.ucm.get_phones()
        target_names = []
        for raw_p in raw_phones:
            p = helpers.serialize_object(raw_p)
            product = p.get('product', '')
            name = p.get('name')
            if not model_filter or (model_filter.lower() in product.lower()):
                if name:
                    target_names.append(name)
        return target_names

    def get_active_ips(self, device_names):
        ris_wsdl = f"https://{self.ip}:8443/realtimeservice2/services/RISService70?wsdl"
        ris_endpoint = f"https://{self.ip}:8443/realtimeservice2/services/RISService70"

        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(self.username, self.password)
        ris_transport = Transport(session=session, timeout=30)
        ris_client = Client(ris_wsdl, transport=ris_transport)
        ris_service = ris_client.create_service('{http://schemas.cisco.com/ast/soap}RisBinding', ris_endpoint)

        active_ips = []
        chunk_size = 100

        for i in range(0, len(device_names), chunk_size):
            if i > 0:
                time.sleep(4.2)

            chunk = device_names[i:i + chunk_size]
            criteria = {
                'MaxReturnedDevices': chunk_size,
                'DeviceClass': 'Any',
                'Model': 255,
                'Status': 'Registered',
                'SelectBy': 'Name',
                'SelectItems': {'item': [{'Item': name} for name in chunk]},
                'Protocol': 'Any'
            }

            try:
                ris_response = ris_service.selectCmDevice(StateInfo="", CmSelectionCriteria=criteria)
                ris_data = helpers.serialize_object(ris_response)
                nodes = ris_data['SelectCmDeviceResult']['CmNodes']['item']
                for node in nodes:
                    if node.get('CmDevices') and node['CmDevices'].get('item'):
                        for dev in node['CmDevices']['item']:
                            if dev.get('IPAddress') and dev['IPAddress'].get('item'):
                                ip = dev['IPAddress']['item'][0].get('IP')
                                if ip and ip != "None":
                                    active_ips.append(f"{dev['Name']} - {ip}")
                                    print(f"REGISTERED: {dev['Name']} -> {ip}")
            except Exception:
                continue

        return active_ips

    def save_to_file(self, data):
        if data:
            with open(self.output_file, "w") as f:
                for line in data:
                    f.write(line + "\n")


if __name__ == "__main__":
    CUCM_IP = 'ip_addr'
    USER = 'user.name'
    PASS = 'password'

    model_input = input("Model giriniz (tüm modeller için ENTER): ").strip()
    scanner = CUCMScanner(CUCM_IP, USER, PASS)

    devices = scanner.get_device_list(model_filter=model_input)

    if devices:
        results = scanner.get_active_ips(devices)
        scanner.save_to_file(results)
        print(f"\nToplam Aktif Cihaz Sayısı: {len(results)}")
    else:
        print(f"\nHata: '{model_input}' modeline ait bir cihaz bulunamadı.")