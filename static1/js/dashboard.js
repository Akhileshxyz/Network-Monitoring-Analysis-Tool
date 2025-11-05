// Global state
let isCapturing = false;
let updateInterval = null;
let protocolChart = null;
let talkersChart = null;

// Initialize charts
function initCharts() {
    // Protocol Distribution Chart
    const protocolCtx = document.getElementById('protocolChart').getContext('2d');
    protocolChart = new Chart(protocolCtx, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b',
                    '#ef4444',
                    '#8b5cf6',
                    '#ec4899',
                    '#14b8a6'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Top Talkers Chart
    const talkersCtx = document.getElementById('talkersChart').getContext('2d');
    talkersChart = new Chart(talkersCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Packet Count',
                data: [],
                backgroundColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Update statistics
async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();

        document.getElementById('totalPackets').textContent = 
            stats.total_packets.toLocaleString();
        
        const dataMB = (stats.total_bytes / (1024 * 1024)).toFixed(2);
        document.getElementById('totalData').textContent = `${dataMB} MB`;
        
        document.getElementById('activeIPs').textContent = stats.active_ips;
        
        const hours = Math.floor(stats.duration_seconds / 3600);
        const minutes = Math.floor((stats.duration_seconds % 3600) / 60);
        const seconds = stats.duration_seconds % 60;
        document.getElementById('duration').textContent = 
            `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        
        document.getElementById('status').textContent = 
            stats.is_capturing ? 'Capturing' : 'Idle';
        document.getElementById('status').style.color = 
            stats.is_capturing ? '#10b981' : '#f59e0b';
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Update protocol distribution chart
async function updateProtocolChart() {
    try {
        const response = await fetch('/api/protocol-dist');
        const data = await response.json();

        const labels = Object.keys(data);
        const values = Object.values(data);

        protocolChart.data.labels = labels;
        protocolChart.data.datasets[0].data = values;
        protocolChart.update();
    } catch (error) {
        console.error('Error updating protocol chart:', error);
    }
}

// Update top talkers chart
async function updateTalkersChart() {
    try {
        const response = await fetch('/api/top-talkers');
        const data = await response.json();

        const labels = data.map(item => item.ip);
        const values = data.map(item => item.count);

        talkersChart.data.labels = labels;
        talkersChart.data.datasets[0].data = values;
        talkersChart.update();
    } catch (error) {
        console.error('Error updating talkers chart:', error);
    }
}

// Update packets table
async function updatePacketsTable() {
    try {
        const response = await fetch('/api/packets');
        const packets = await response.json();

        const tbody = document.getElementById('packetsBody');

        if (packets.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No packets captured yet</td></tr>';
            return;
        }

        tbody.innerHTML = packets.map(packet => `
            <tr>
                <td>${packet.timestamp}</td>
                <td>${packet.source_ip}</td>
                <td>${packet.source_port}</td>
                <td>${packet.dest_ip}</td>
                <td>${packet.dest_port}</td>
                <td><span style="background: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.85em;">${packet.protocol}</span></td>
                <td>${packet.size} B</td>
            </tr>
        `).reverse().join('');
    } catch (error) {
        console.error('Error updating packets table:', error);
    }
}

// Update devices table
async function updateDevicesTable() {
    try {
        const response = await fetch('/api/devices');
        const data = await response.json();
        const devices = data.devices;

        const tbody = document.getElementById('devicesBody');

        if (devices.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="empty-state">Click "Scan Network" to discover devices</td></tr>';
            return;
        }

        tbody.innerHTML = devices.map(device => `
            <tr>
                <td><strong>${device.ip}</strong></td>
                <td><code>${device.mac}</code></td>
                <td>${device.hostname}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error updating devices table:', error);
    }
}

// Start capture
async function startCapture() {
    try {
        const response = await fetch('/api/start', { method: 'POST' });
        const result = await response.json();

        if (result.status === 'started') {
            isCapturing = true;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            
            // Start periodic updates
            updateInterval = setInterval(() => {
                updateStats();
                updateProtocolChart();
                updateTalkersChart();
                updatePacketsTable();
            }, 2000); // Update every 2 seconds

            showNotification('Packet capture started!', 'success');
        }
    } catch (error) {
        console.error('Error starting capture:', error);
        showNotification('Failed to start capture', 'error');
    }
}

// Stop capture
async function stopCapture() {
    try {
        const response = await fetch('/api/stop', { method: 'POST' });
        const result = await response.json();

        if (result.status === 'stopped') {
            isCapturing = false;
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            
            // Stop periodic updates
            if (updateInterval) {
                clearInterval(updateInterval);
                updateInterval = null;
            }

            // Final update
            updateStats();
            updateProtocolChart();
            updateTalkersChart();
            updatePacketsTable();

            showNotification('Packet capture stopped!', 'info');
        }
    } catch (error) {
        console.error('Error stopping capture:', error);
        showNotification('Failed to stop capture', 'error');
    }
}

// Scan network
async function scanNetwork() {
    try {
        document.getElementById('scanBtn').disabled = true;
        document.getElementById('devicesLoading').style.display = 'block';
        
        showNotification('Scanning network...', 'info');

        const response = await fetch('/api/scan', { method: 'POST' });
        const result = await response.json();

        document.getElementById('devicesLoading').style.display = 'none';
        document.getElementById('scanBtn').disabled = false;

        await updateDevicesTable();
        showNotification(`Found ${result.count} devices!`, 'success');
    } catch (error) {
        console.error('Error scanning network:', error);
        document.getElementById('devicesLoading').style.display = 'none';
        document.getElementById('scanBtn').disabled = false;
        showNotification('Failed to scan network', 'error');
    }
}

// Export data
async function exportData() {
    try {
        showNotification('Exporting data...', 'info');
        window.location.href = '/api/export';
        setTimeout(() => {
            showNotification('Data exported successfully!', 'success');
        }, 1000);
    } catch (error) {
        console.error('Error exporting data:', error);
        showNotification('Failed to export data', 'error');
    }
}

// Reset data
async function resetData() {
    if (!confirm('Are you sure you want to reset all data? This cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        const result = await response.json();

        if (result.status === 'reset') {
            // Reset UI
            updateStats();
            updateProtocolChart();
            updateTalkersChart();
            updatePacketsTable();
            
            showNotification('Data reset successfully!', 'success');
        }
    } catch (error) {
        console.error('Error resetting data:', error);
        showNotification('Failed to reset data', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };

    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    updateStats();
    updateDevicesTable();

    document.getElementById('startBtn').addEventListener('click', startCapture);
    document.getElementById('stopBtn').addEventListener('click', stopCapture);
    document.getElementById('scanBtn').addEventListener('click', scanNetwork);
    document.getElementById('exportBtn').addEventListener('click', exportData);
    document.getElementById('resetBtn').addEventListener('click', resetData);
});
