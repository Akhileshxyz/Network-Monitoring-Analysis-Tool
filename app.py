from flask import Flask, render_template, jsonify, send_file
from flask_cors import CORS
from packet_capture import PacketCapture
from network_scanner import NetworkScanner
import csv
from io import StringIO, BytesIO
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize components
packet_capture = PacketCapture()
network_scanner = NetworkScanner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_capture():
    """Start packet capture"""
    packet_capture.start_capture()
    return jsonify({'status': 'started', 'message': 'Packet capture started'})

@app.route('/api/stop', methods=['POST'])
def stop_capture():
    """Stop packet capture"""
    packet_capture.stop_capture()
    return jsonify({'status': 'stopped', 'message': 'Packet capture stopped'})

@app.route('/api/stats')
def get_stats():
    """Get current statistics"""
    return jsonify(packet_capture.get_stats())

@app.route('/api/protocol-dist')
def get_protocol_dist():
    """Get protocol distribution"""
    return jsonify(packet_capture.get_protocol_distribution())

@app.route('/api/top-talkers')
def get_top_talkers():
    """Get top talkers"""
    return jsonify(packet_capture.get_top_talkers())

@app.route('/api/packets')
def get_packets():
    """Get recent packets"""
    return jsonify(packet_capture.get_recent_packets())

@app.route('/api/scan', methods=['POST'])
def scan_network():
    """Scan network for devices"""
    devices = network_scanner.scan_network()
    return jsonify({'devices': devices, 'count': len(devices)})

@app.route('/api/devices')
def get_devices():
    """Get scanned devices"""
    return jsonify({'devices': network_scanner.devices})

@app.route('/api/export')
def export_data():
    """Export captured packets as CSV"""
    packets = packet_capture.packets
    
    if not packets:
        return jsonify({'error': 'No data to export'}), 400
    
    # Create CSV in memory
    output = StringIO()
    
    # Write CSV
    if packets:
        headers = packets[0].keys()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(packets)
    
    # Convert to bytes for send_file
    csv_bytes = BytesIO()
    csv_bytes.write(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'network_capture_{timestamp}.csv'
    
    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/reset', methods=['POST'])
def reset_data():
    """Reset all captured data"""
    packet_capture.reset()
    return jsonify({'status': 'reset', 'message': 'Data reset successfully'})

if __name__ == '__main__':
    print("="*50)
    print("Network Monitor Server Starting...")
    print("="*50)
    print("\nIMPORTANT: Run with sudo on Linux/Mac:")
    print("  sudo python app.py")
    print("\nAccess dashboard at: http://localhost:5000")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)