import requests

# Constants
API_TOKEN = ''
ANSIBLE_DROPLET_NAME = 'ansible-automation-platform-tf'
EVENT_DRIVEN_DROPLET_NAME = 'event-driven-droplet-tf'
INVENTORY_FILE_PATH = '/root/ansible-automation-platform-setup-bundle-2.4-1-x86_64/inventory'
HOSTS_FILE_PATH = '/etc/hosts'

def get_droplet_id(api_token, droplet_name):
    url = 'https://api.digitalocean.com/v2/droplets'
    headers = {'Authorization': f'Bearer {api_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        droplets = data['droplets']
        for droplet in droplets:
            if droplet['name'] == droplet_name:
                return droplet['id']
        print(f'Droplet with name {droplet_name} not found.')
        return None
    else:
        print(f'Error fetching droplets info: {response.status_code} - {response.text}')
        return None

def get_droplet_ip(api_token, droplet_id):
    url = f'https://api.digitalocean.com/v2/droplets/{droplet_id}'
    headers = {'Authorization': f'Bearer {api_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        ip_address = data['droplet']['networks']['v4'][0]['ip_address']
        return ip_address
    else:
        print(f'Error fetching droplet info: {response.status_code} - {response.text}')
        return None

def update_inventory_file(file_path, ansible_ip, event_driven_ip):
    # Read the inventory file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    ansible_ip_replaced = False
    event_driven_added = False

    # Go through each line and update the required fields
    for line in lines:
        if line.startswith('automationplatform.zapto.org'):
            # Replace the line with the droplet's IP and ansible_collection
            new_lines.append(f'{ansible_ip} ansible_collection=local\n')
            ansible_ip_replaced = True
        elif line.startswith('[automationedacontroller]') and not event_driven_added:
            new_lines.append(line)
            # Add the event-driven droplet IP under [automationedacontroller]
            new_lines.append(f'{event_driven_ip} ansible_ssh_user=root\n')
            event_driven_added = True
        elif line.startswith('automationedacontroller_pg_host='):
            # Update the automationedacontroller_pg_host field with ansible droplet IP
            new_lines.append(f"automationedacontroller_pg_host='{ansible_ip}'\n")
        else:
            new_lines.append(line)

    if not ansible_ip_replaced:
        print(f'Error: "automationplatform.zapto.org ansible_collection=local" not found in {file_path}')
    if not event_driven_added:
        print(f'Error: "[automationedacontroller]" not found in {file_path}')

    # Write the updated lines back to the inventory file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

    print(f'Updated inventory file at {file_path}.')

def update_hosts_file(new_ip_ansible, new_ip_event_driven, hosts_file_path):
    search_line = new_ip_ansible  # Look for ansible droplet's IP

    with open(hosts_file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    ansible_ip_found = False

    for line in lines:
        new_lines.append(line)
        if line.strip() == search_line:
            # Insert the event-driven droplet IP just below ansible droplet IP
            new_lines.append(f'{new_ip_event_driven}\n')
            ansible_ip_found = True

    if not ansible_ip_found:
        print(f'Error: "{search_line}" not found in {hosts_file_path}')

    # Write the changes back to the file
    with open(hosts_file_path, 'w') as file:
        file.writelines(new_lines)

    if ansible_ip_found:
        print(f'Added public IP {new_ip_event_driven} to {hosts_file_path}.')

def main():
    # Get Ansible Automation Platform droplet info
    ansible_droplet_id = get_droplet_id(API_TOKEN, ANSIBLE_DROPLET_NAME)
    if not ansible_droplet_id:
        return

    ansible_ip_address = get_droplet_ip(API_TOKEN, ansible_droplet_id)
    if not ansible_ip_address:
        return

    # Get Event-Driven droplet info
    event_driven_droplet_id = get_droplet_id(API_TOKEN, EVENT_DRIVEN_DROPLET_NAME)
    if event_driven_droplet_id:
        event_driven_ip_address = get_droplet_ip(API_TOKEN, event_driven_droplet_id)
        if event_driven_ip_address:
            # Update inventory and hosts files
            update_inventory_file(INVENTORY_FILE_PATH, ansible_ip_address, event_driven_ip_address)
            update_hosts_file(ansible_ip_address, event_driven_ip_address, HOSTS_FILE_PATH)
        else:
            print(f'Error: Unable to fetch IP for "{EVENT_DRIVEN_DROPLET_NAME}".')
    else:
        print(f'Error: Droplet "{EVENT_DRIVEN_DROPLET_NAME}" not found or not up.')

if __name__ == '__main__':
    main()
