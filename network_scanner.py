from scapy.all import ARP, Ether, srp
import socket

class NetworkScanner:
    def __init__(self):
        self.devices = []
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "192.168.1.1"
    
    def scan_network(self, ip_range=None):
        """Scan local network for devices"""
        if not ip_range:
            local_ip = self.get_local_ip()
            # Convert 192.168.1.100 to 192.168.1.0/24
            ip_parts = local_ip.split('.')
            ip_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        
        print(f"Scanning network: {ip_range}")
        
        # Create ARP request
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        
        # Send packet and get response
        result = srp(packet, timeout=3, verbose=0)[0]
        
        devices = []
        for sent, received in result:
            # Try to get hostname
            try:
                hostname = socket.gethostbyaddr(received.psrc)[0]
            except:
                hostname = "Unknown"
            
            devices.append({
                'ip': received.psrc,
                'mac': received.hwsrc,
                'hostname': hostname
            })
        
        self.devices = devices
        return devices

# Test the scanner
if __name__ == "__main__":
    scanner = NetworkScanner()
    devices = scanner.scan_network()
    print(f"Found {len(devices)} devices:")
    for device in devices:
        print(f"  IP: {device['ip']}, MAC: {device['mac']}, Host: {device['hostname']}")
