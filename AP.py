import paramiko

def get_ap_list(wlc_ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(wlc_ip, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command('show ap summary')
    ap_list = stdout.read().decode('utf-8')
    
    ssh.close()
    return ap_list

wlc_ip = '10.21.255.118'
username = 'ext_plencinas@vistaenergy.com'
password = 'Miami2025!.'
ap_list = get_ap_list(wlc_ip, username, password)
print(ap_list)  # Now send this data to your 3rd party app
