from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from datetime import datetime
from collections import defaultdict
import threading

class PacketCapture:
    def __init__(self):
        self.packets = []
        self.is_capturing = False
        self.capture_thread = None
        self.stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'protocol_count': defaultdict(int),
            'ip_count': defaultdict(int),
            'start_time': None
        }
    
    def identify_protocol(self, packet):
        """Identify packet protocol"""
        if packet.haslayer(TCP):
            # Check common ports
            dport = packet[TCP].dport
            sport = packet[TCP].sport
            if dport == 80 or sport == 80:
                return 'HTTP'
            elif dport == 443 or sport == 443:
                return 'HTTPS'
            elif dport == 22 or sport == 22:
                return 'SSH'
            elif dport == 21 or sport == 21:
                return 'FTP'
            elif dport == 53 or sport == 53:
                return 'DNS'
            else:
                return 'TCP'
        elif packet.haslayer(UDP):
            dport = packet[UDP].dport
            sport = packet[UDP].sport
            if dport == 53 or sport == 53:
                return 'DNS'
            elif dport == 67 or dport == 68:
                return 'DHCP'
            else:
                return 'UDP'
        elif packet.haslayer(ICMP):
            return 'ICMP'
        else:
            return 'OTHER'
    
    def process_packet(self, packet):
        """Process captured packet"""
        if not packet.haslayer(IP):
            return
        
        # Extract packet info
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        source_ip = packet[IP].src
        dest_ip = packet[IP].dst
        protocol = self.identify_protocol(packet)
        size = len(packet)
        
        # Get ports if available
        source_port = packet[TCP].sport if packet.haslayer(TCP) else (
            packet[UDP].sport if packet.haslayer(UDP) else 0
        )
        dest_port = packet[TCP].dport if packet.haslayer(TCP) else (
            packet[UDP].dport if packet.haslayer(UDP) else 0
        )
        
        packet_data = {
            'timestamp': timestamp,
            'source_ip': source_ip,
            'dest_ip': dest_ip,
            'source_port': source_port,
            'dest_port': dest_port,
            'protocol': protocol,
            'size': size
        }
        
        # Update statistics
        self.stats['total_packets'] += 1
        self.stats['total_bytes'] += size
        self.stats['protocol_count'][protocol] += 1
        self.stats['ip_count'][source_ip] += 1
        
        # Store packet (keep last 1000)
        self.packets.append(packet_data)
        if len(self.packets) > 1000:
            self.packets.pop(0)
    
    def start_capture(self, interface=None):
        """Start packet capture in background thread"""
        if self.is_capturing:
            return
        
        self.is_capturing = True
        self.stats['start_time'] = datetime.now()
        
        def capture():
            sniff(prn=self.process_packet, store=0, stop_filter=lambda x: not self.is_capturing, iface=interface)
        
        self.capture_thread = threading.Thread(target=capture, daemon=True)
        self.capture_thread.start()
    
    def stop_capture(self):
        """Stop packet capture"""
        self.is_capturing = False
    
    def get_stats(self):
        """Get current statistics"""
        duration = 0
        if self.stats['start_time']:
            duration = (datetime.now() - self.stats['start_time']).total_seconds()
        
        return {
            'total_packets': self.stats['total_packets'],
            'total_bytes': self.stats['total_bytes'],
            'active_ips': len(self.stats['ip_count']),
            'duration_seconds': int(duration),
            'is_capturing': self.is_capturing
        }
    
    def get_protocol_distribution(self):
        """Get protocol distribution for charts"""
        return dict(self.stats['protocol_count'])
    
    def get_top_talkers(self, limit=5):
        """Get top N most active IPs"""
        sorted_ips = sorted(
            self.stats['ip_count'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        return [{'ip': ip, 'count': count} for ip, count in sorted_ips]
    
    def get_recent_packets(self, limit=20):
        """Get most recent packets"""
        return self.packets[-limit:]
    
    def reset(self):
        """Reset all data"""
        self.packets = []
        self.stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'protocol_count': defaultdict(int),
            'ip_count': defaultdict(int),
            'start_time': None
        }

# Test
if __name__ == "__main__":
    capture = PacketCapture()
    print("Starting capture for 10 seconds...")
    capture.start_capture()
    
    import time
    time.sleep(10)
    
    capture.stop_capture()
    print(f"\nCaptured {capture.stats['total_packets']} packets")
    print(f"Protocol distribution: {capture.get_protocol_distribution()}")
    print(f"Top talkers: {capture.get_top_talkers()}")
