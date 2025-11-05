# Network Monitoring & Analysis Tool

A Python-based network monitoring application that captures and analyzes network traffic in real-time.

## Features

- 🔍 Network device scanner
- 📦 Real-time packet capture
- 📊 Protocol distribution visualization
- 🔝 Top talkers analysis
- 📥 CSV export functionality
- 🎨 Beautiful web dashboard

## Requirements

- Python 3.8+
- Root/Administrator privileges (for packet capture)
- Network interface access

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd network-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Linux/Mac:
```bash
sudo python app.py
```

### Windows (Run as Administrator):
```bash
python app.py
```

Access the dashboard at: `http://localhost:5000`

## Dashboard Features

### Network Scanner
- Discovers all devices on your local network
- Shows IP addresses, MAC addresses, and hostnames

### Packet Capture
- Real-time packet analysis
- Protocol identification (TCP, UDP, HTTP, HTTPS, DNS, etc.)
- Traffic statistics

### Visualizations
- Protocol distribution pie chart
- Top talkers bar chart
- Recent packets table

### Data Export
- Export captured packets to CSV
- Includes timestamp, IPs, ports, protocol, and size

## Technical Stack

- **Backend**: Python, Flask, Scapy
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js
- **Data Processing**: Pandas

## Screenshots

[Add screenshots of your dashboard here]

## Author

Akhilesh K A
