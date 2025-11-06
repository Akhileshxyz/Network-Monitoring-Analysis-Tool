# Network Monitoring & Analysis Tool

A Python-based network monitoring application that captures and analyzes network traffic in real-time with an intuitive web dashboard.

## 🎯 Project Overview

This project was built to gain hands-on experience with network protocols, packet analysis, and full-stack development. While production environments use tools like Wireshark or Nagios, building this from scratch provided deep insights into how network monitoring works at the packet level.

## ✨ Features

- 🔍 **Network device scanner** - Discover all devices on your local network
- 📦 **Real-time packet capture** - Live network traffic analysis
- 📊 **Protocol distribution visualization** - Visual breakdown of traffic by protocol
- 🔝 **Top talkers analysis** - Identify most active IP addresses
- 📥 **CSV export functionality** - Export captured data for analysis
- 🎨 **Beautiful web dashboard** - Modern, responsive interface

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Root/Administrator privileges (for packet capture)
- Network interface access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Akhileshxyz/Network-Monitoring-Analysis-Tool
cd Network-Monitoring-Analysis-Tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

**Linux/Mac:**
```bash
sudo python app.py
```

**Windows (Run as Administrator):**
```bash
python app.py
```

Access the dashboard at: **http://localhost:5000**

## 📋 Dashboard Features

### Network Scanner
- Automatically discovers all devices on your local network
- Displays IP addresses, MAC addresses, and hostnames
- Quick identification of connected devices

### Packet Capture
- Real-time packet analysis with live updates
- Protocol identification (TCP, UDP, HTTP, HTTPS, DNS, ICMP, SSH, FTP, DHCP)
- Traffic statistics and bandwidth monitoring
- Top talker identification

### Visualizations
- **Protocol distribution pie chart** - See traffic breakdown by protocol
- **Top talkers bar chart** - Identify most active devices
- **Recent packets table** - Detailed packet information with timestamps

### Data Export
- Export captured packets to CSV format
- Includes timestamp, source/destination IPs, ports, protocol, and packet size
- Timestamped filenames for easy organization

## 🛠️ Technical Stack

- **Backend**: Python 3.8+, Flask
- **Packet Analysis**: Scapy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Visualization**: Chart.js
- **Data Processing**: Pandas

## 📐 Architecture

```
Network Interface
       ↓
Scapy Packet Capture → Packet Analyzer → In-Memory Data Store
       ↓                                           ↓
Network Scanner ─────────────────────→   Flask REST API
                                                   ↓
                                         HTML/JS Dashboard
```

## 💡 Why I Built This

As part of my journey to understand networking fundamentals and strengthen my Python skills, I wanted to understand how professional network monitoring tools work under the hood. This project helped me learn:

- Packet capture and analysis using Scapy
- Network protocols at the application and transport layers
- Real-time data processing with Python threading
- RESTful API design and implementation
- Full-stack web application development
- Data visualization techniques

## 🎓 Technical Highlights

- **Multi-threaded packet capture** for non-blocking performance
- **Real-time dashboard updates** via REST API polling (2-second intervals)
- **Protocol identification** based on port analysis and packet inspection
- **Memory management** - Maintains only last 1000 packets to prevent overflow
- **Responsive design** - Works across desktop and mobile devices
- **CSV export** with timestamped filenames

## 🔧 Challenges & Solutions

### 1. Permission Requirements
**Challenge**: Packet capture requires root/administrator privileges.  
**Solution**: Implemented proper error handling and clear documentation for users.

### 2. Threading Complexity
**Challenge**: Flask blocking during packet capture.  
**Solution**: Used daemon threads to run packet capture in the background without blocking the web server.

### 3. Performance Optimization
**Challenge**: Memory usage growing with continuous packet capture.  
**Solution**: Limited storage to 1000 most recent packets with automatic cleanup.

### 4. Cross-Platform Compatibility
**Challenge**: Different network interfaces on Windows vs Linux/Mac.  
**Solution**: Auto-detection of local IP and dynamic network range calculation.

## 📊 Project Structure

```
network-monitor/
├── app.py                 # Flask server with REST API endpoints
├── packet_capture.py      # Packet capture and analysis logic
├── network_scanner.py     # Network device discovery
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── static/
│   ├── css/
│   │   └── style.css     # Dashboard styling
│   └── js/
│       └── dashboard.js   # Frontend logic and API calls
└── templates/
    └── index.html        # Dashboard HTML template
```

## 🚀 Future Enhancements

- [ ] Packet filtering by protocol, IP, or port
- [ ] WebSocket integration for true real-time updates
- [ ] SQLite database for persistent storage
- [ ] Historical data analysis and comparison
- [ ] Alert system for unusual traffic patterns
- [ ] Deep packet inspection for payload analysis
- [ ] Dark mode toggle
- [ ] Export to multiple formats (JSON, XML)

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

## 📝 License

MIT License

## 👨‍💻 Author

**Akhilesh K A**
- GitHub: [@Akhileshxyz](https://github.com/Akhileshxyz)
- Project Link: [Network-Monitoring-Analysis-Tool](https://github.com/Akhileshxyz/Network-Monitoring-Analysis-Tool)

## 🙏 Acknowledgments

- Scapy documentation and community
- Flask framework documentation
- Chart.js for beautiful visualizations

---

**Note**: This is an educational project designed for learning purposes. For production network monitoring, consider using established tools like Wireshark, tcpdump, or enterprise solutions like Nagios or PRTG.