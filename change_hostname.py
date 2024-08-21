from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'host': '100.100.1.141', 
    'username': 'natroy2',
    'password': 'natroy2',
    'session_log': 'session_log.txt'
}

net_connect = ConnectHandler(**device)

new_hostname = 'Router-1941'
config_commands = [f'hostname {new_hostname}']
net_connect.send_config_set(config_commands)

output = net_connect.send_command("show run | include hostname")
print(output)

net_connect.disconnect()

