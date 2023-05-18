import requests, json, argparse
from termcolor import colored
from colorama import Fore, Back, Style

class DigitalOcean():

    def __init__(self):
        self.api = ''
        self.url = 'https://api.digitalocean.com/v2/droplets'
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api}'}
        self.post_data = {"type": "reboot"}
        self.response = requests.get(self.url, headers=self.headers).text
        self.data = json.loads(self.response)

    def get_details(self, data):
        dropletsNames = [droplet['name'] for droplet in data['droplets']]
        dropletsID = [dropid['id'] for dropid in data['droplets'][:]]
        dropletstatus = [dropstat['status'] for dropstat in data['droplets']]
        dropletIP = [dropletip['networks']['v4'] for dropletip in data['droplets']]

        print("\nFound the following Droplets:")
        for droplets, ids, status, ips in zip(dropletsNames, dropletsID, dropletstatus, dropletIP):
            if status == 'off':
                status_colour = Fore.RED
            elif status == 'active':
                status_colour = Fore.GREEN
            else:
                status_colour = Fore.GREEN

            print(f"\n- {droplets}")
            print(f"\tID: {ids}")
            print(f"\tStatus: {status_colour} {status} {Style.RESET_ALL}")
            for ip in ips:
                if ip['type'] == 'public':
                    print(f"\tPublic IP: {Fore.BLUE} {ip['ip_address']} {Style.RESET_ALL}")

        else:
            pass
        print("\n")
        
    def droplet_reboot(self, id):
        url = f"https://api.digitalocean.com/v2/droplets/{id}/actions"
        print(url)
        response = requests.post(url, headers=self.headers, data='{"type": "reboot"}')
        print(response.text)

    def create_droplet(self, ):
        droplet_name = input("\nName your droplet (Security-Operations-VPS-[NAME}): ")
        url = "https://api.digitalocean.com/v2/droplets"
        pdata = {"name":f"Security-Operations-VPS-{droplet_name}", "region":"lon1", "size":"4gb", "image":"66761652"}
        req = requests.post(url, headers=self.headers, json=pdata)
        print(req.text)

    def power_off_droplet(self, id=''):
        #droplet_id = input("\nDroplet ID to power off: ")
        url = f"https://api.digitalocean.com/v2/droplets/{id}/actions"
        response = requests.post(url, json={"type": "shutdown"}, headers=self.headers)
        #print(response.text)
        if response.status_code == 201:
            print("\nDroplet Powering OFF\n")
        else:
            print("\nThere was an issue powering off the droplet, check the ID.\n")

    def power_on_droplet(self, id=''):
        #droplet_id = input("\nDroplet ID to power on: ")
        url = f"https://api.digitalocean.com/v2/droplets/{id}/actions"
        response = requests.post(url, json={"type": "power_on"}, headers=self.headers)
        #print(response.text)
        if response.status_code == 201:
                print("\nDroplet Powering ON\n")
        else:
            print("\nThere was an issue powering on the droplet, check the ID.\n")

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--list', action='store_true', help='List the droplets belonging to your account.')
        parser.add_argument('-a', '--api', help='provide an API key for DigitalOcean', required=True)
        parser.add_argument('-on', '--poweron', help='power ON a Droplet by its ID', type=int)
        parser.add_argument('-off', '--poweroff', help='power OFF a Droplet by its ID', type=int)
        args = parser.parse_args()

        if args.api:
            self.api = args.api
            if args.list:
                self.get_details(self.data)
            elif args.poweron:
                self.power_on_droplet(args.poweron)
            elif args.poweroff:
                self.power_off_droplet(args.poweroff)
            else:
                parser.print_help()    

if __name__ == "__main__":
    x = DigitalOcean()
    x.run()
    

        
    


"""
ToDO List:
- If no arguments are given then list droplets
- specify an action e.g. "--reboot"
- pass the tool an ID number along with action
 
"""
