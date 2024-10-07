import requests
import argparse
import json
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

def get_access_token():
    url = "https://demo.natroy.io/api/autho"

    payload = json.dumps({
        "email": "admin@natroy.io",
        "password": "pirulo"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        res = response.json()
        return res['access_token']
    else:
        print(f"Error al obtener los dispositivos: {response.status_code}")
        return None
    print(response.text)


def create_asset(assets):
      
  acces_token = get_access_token()
  url = "https://demo.natroy.io/api/offline/asset"
  headers = {
    'Authorization': 'Bearer {}'.format(acces_token),
    'Content-Type': 'application/json'
  }

  for asset in assets:
    payload = {}
    payload = json.dumps([
      {
        "active": True,
        "host": asset.get('ip'),
        "ipAddress": asset.get('ip'),
        "status": "ACTIVE",
        "vendor": "Cisco",
        "devicetype": asset.get('deviceType'),
        "hostname": asset.get('name'),
        "model": asset.get('model'),
        "partNumber": asset.get('model'),
        "base_pid": asset.get('model'),
        "serialNumber": asset.get('sn'),
        "offline": False,
        "tags": []
      }
    ])

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 201:
      print("Asset creado: {} con IP: {}".format(asset.get('name'), asset.get('ip')))
    else:
      print("Status code distinto a 201: {}".format(response.status_code))
      print("Asset NO creado: {}".format(asset))


# Función para obtener las organizaciones y filtrar por nombre
def obtener_org_id_por_nombre(api_key, nombre_organizacion):
    url = 'https://api.meraki.com/api/v1/organizations'
    
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        organizaciones = response.json()
        
        # Filtrar la organización por nombre
        for organizacion in organizaciones:
            if organizacion['name'].lower() == nombre_organizacion.lower():
                return organizacion['id']
        
        print("Organización no encontrada.")
        return None
    else:
        print(f"Error al obtener las organizaciones: {response.status_code}")
        return None

# Función para obtener los dispositivos de la organización y sus IPs
def obtener_dispositivos_con_ips(api_key, organization_id):
    url = f'https://api.meraki.com/api/v1/organizations/{organization_id}/devices/statuses'
    
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        dispositivos = response.json()
        return dispositivos
    else:
        print(f"Error al obtener los dispositivos: {response.status_code}")
        return None

# Función para manejar los argumentos
def obtener_argumentos():
    parser = argparse.ArgumentParser(description="Obtener el Organization ID y los dispositivos con IP de Cisco Meraki por nombre.")
    
    # Añadir argumentos -o (organización) y -k (API Key)
    parser.add_argument('-o', '--organizacion', required=True, help='Nombre de la organización')
    parser.add_argument('-k', '--key', required=True, help='API Key de Cisco Meraki')

    return parser.parse_args()

# Ejecutar la función para buscar el orgID por nombre de organización y obtener los dispositivos
if __name__ == "__main__":
    # Obtener los argumentos desde la línea de comandos
    args = obtener_argumentos()
    
    # Extraer la API Key y el nombre de la organización desde los argumentos
    api_key = args.key
    nombre_organizacion = args.organizacion
    
    # Llamar a la función para obtener el orgID
    org_id = obtener_org_id_por_nombre(api_key, nombre_organizacion)
    
    if org_id:
        print(f"El ID de la organización '{nombre_organizacion}' es: {org_id}")
        
        # Llamar a la función para obtener los dispositivos con IPs
        dispositivos = obtener_dispositivos_con_ips(api_key, org_id)
        
        if dispositivos:
            print(f"Dispositivos en la organización '{nombre_organizacion}':")
            #(print(json.dumps(dispositivos, indent=2)))
            dispositivos_list = []
            for dispositivo in dispositivos:
                if dispositivo.get('lanIp'):
                    ip = dispositivo.get('lanIp')
                elif dispositivo.get('wan1Ip'):
                    ip = dispositivo.get('wan1Ip')
                else:
                    ip = dispositivo.get('publicIp')

                disp_info = {
                    'name': dispositivo.get('name', 'Sin nombre'),
                    'model': dispositivo.get('model', 'Modelo desconocido'),
                    'ip': ip,
                    'sn': dispositivo.get('serial', 'Serial no disponible'),
                    'deviceType': dispositivo.get('productType', 'productType no disponible')
                }
                dispositivos_list.append(disp_info)
                disp_info = {}
                #print(f"Dispositivo: {nombre}, Modelo: {modelo}, IP: {direccion_ip}, Serial: {serial}")

            print(dispositivos_list)
            create_asset(dispositivos_list)
        else:
            print("No se pudieron obtener los dispositivos.")
    else:
        print(f"No se encontró el ID de la organización con el nombre '{nombre_organizacion}'.")
