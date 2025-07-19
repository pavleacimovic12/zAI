// Training dashboard functionality

let progressChart = null;
let metricsChart = null;
let trainingInterval = null;

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    updateStats();
    setInterval(updateStats, 10000); // Update every 10 seconds
});

// Initialize Chart.js charts
function initCharts() {
    // Progress Chart
    const progressCtx = document.getElementById('progressChart').getContext('2d');
    progressChart = new Chart(progressCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Cumulative Reward',
                data: [],
                borderColor: 'rgba(13, 110, 253, 1)',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Average Loss',
                data: [],
                borderColor: 'rgba(220, 53, 69, 1)',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                tension: 0.4,
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#ffffff' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    ticks: { color: '#ffffff' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    ticks: { color: '#ffffff' },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });

    // Metrics Chart
    const metricsCtx = document.getElementById('metricsChart').getContext('2d');
    metricsChart = new Chart(metricsCtx, {
        type: 'doughnut',
        data: {
            labels: ['Exploration', 'Exploitation'],
            datasets: [{
                data: [100, 0], // Will be updated based on epsilon
                backgroundColor: [
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(25, 135, 84, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 193, 7, 1)',
                    'rgba(25, 135, 84, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                }
            }
        }
    });
}

// Start training
async function startTraining() {
    const episodesInput = document.getElementById('episodes');
    const episodes = parseInt(episodesInput.value) || 100;
    const trainBtn = document.getElementById('train-btn');
    const statusDiv = document.getElementById('training-status');
    
    // Disable training button
    trainBtn.disabled = true;
    trainBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Training...';
    
    // Show progress modal
    const trainingModal = new bootstrap.Modal(document.getElementById('trainingModal'));
    trainingModal.show();
    
    // Update status
    statusDiv.className = 'alert alert-warning mb-0';
    statusDiv.innerHTML = '<i class="fas fa-cogs me-2"></i> Training in progress...';
    
    // Add log entry
    addLogEntry('INFO', `Starting training with ${episodes} episodes`);
    
    try {
        const response = await fetch('/api/train', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ episodes: episodes })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Training completed successfully
            statusDiv.className = 'alert alert-success mb-0';
            statusDiv.innerHTML = '<i class="fas fa-check me-2"></i> Training completed successfully!';
            
            addLogEntry('SUCCESS', `Training completed. Total reward: ${data.stats.total_reward.toFixed(2)}`);
            
            // Update statistics display
            updateTrainingStats(data.stats);
            
        } else {
            // Training failed
            statusDiv.className = 'alert alert-danger mb-0';
            statusDiv.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i> Training failed!';
            
            addLogEntry('ERROR', `Training failed: ${data.error}`);
        }
        
    } catch (error) {
        console.error('Training error:', error);
        statusDiv.className = 'alert alert-danger mb-0';
        statusDiv.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i> Training failed due to network error!';
        
        addLogEntry('ERROR', `Network error during training: ${error.message}`);
    } finally {
        // Re-enable training button
        trainBtn.disabled = false;
        trainBtn.innerHTML = '<i class="fas fa-play me-1"></i> Start Training';
        
        // Hide progress modal
        trainingModal.hide();
        
        // Update stats
        updateStats();
    }
}

// Update statistics from server
async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (response.ok && data.training_stats) {
            updateStatsDisplay(data);
        }
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Update statistics display
function updateStatsDisplay(data) {
    const stats = data.training_stats;
    
    // Update stat cards
    document.getElementById('total-episodes').textContent = stats.episodes || 0;
    document.getElementById('total-reward').textContent = (stats.total_reward || 0).toFixed(2);
    document.getElementById('epsilon-value').textContent = (data.epsilon || 1.0).toFixed(3);
    document.getElementById('memory-size').textContent = data.memory_size || 0;
    
    // Update exploration/exploitation chart
    if (metricsChart && data.epsilon !== undefined) {
        const epsilon = data.epsilon;
        const exploration = epsilon * 100;
        const exploitation = (1 - epsilon) * 100;
        
        metricsChart.data.datasets[0].data = [exploration, exploitation];
        metricsChart.update('none');
    }
}

// Update training statistics after training
function updateTrainingStats(stats) {
    // Add data point to progress chart
    if (progressChart) {
        const timestamp = new Date().toLocaleTimeString();
        progressChart.data.labels.push(timestamp);
        progressChart.data.datasets[0].data.push(stats.total_reward || 0);
        progressChart.data.datasets[1].data.push(stats.avg_loss || 0);
        
        // Keep only last 20 data points
        if (progressChart.data.labels.length > 20) {
            progressChart.data.labels.shift();
            progressChart.data.datasets[0].data.shift();
            progressChart.data.datasets[1].data.shift();
        }
        
        progressChart.update('none');
    }
}

// Add entry to training log
function addLogEntry(level, message) {
    const logContainer = document.getElementById('training-log');
    const timestamp = new Date().toLocaleTimeString();
    
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    
    let levelClass = '';
    switch (level.toLowerCase()) {
        case 'error':
            levelClass = 'log-level-error';
            break;
        case 'warning':
            levelClass = 'log-level-warning';
            break;
        case 'success':
            levelClass = 'log-level-info';
            break;
        default:
            levelClass = 'log-level-info';
    }
    
    logEntry.innerHTML = `
        <span class="log-timestamp">[${timestamp}]</span>
        <span class="${levelClass}">[${level}]</span>
        <span class="log-message">${message}</span>
    `;
    
    logContainer.appendChild(logEntry);
    
    // Auto-scroll to bottom
    logContainer.scrollTop = logContainer.scrollHeight;
    
    // Keep only last 100 entries
    const entries = logContainer.querySelectorAll('.log-entry');
    if (entries.length > 100) {
        entries[0].remove();
    }
}

// Clear training log
function clearLog() {
    const logContainer = document.getElementById('training-log');
    logContainer.innerHTML = '<div class="text-muted">Training log cleared...</div>';
}

// Export training data
function exportTrainingData() {
    // This would export training statistics and logs
    const data = {
        timestamp: new Date().toISOString(),
        charts: {
            progress: progressChart ? progressChart.data : null,
            metrics: metricsChart ? metricsChart.data : null
        },
        logs: Array.from(document.querySelectorAll('.log-entry')).map(entry => entry.textContent)
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `training-data-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

// Handle window resize for charts
window.addEventListener('resize', function() {
    if (progressChart) progressChart.resize();
    if (metricsChart) metricsChart.resize();
});

// Initialize with some sample log entries
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        addLogEntry('INFO', 'Training dashboard initialized');
        addLogEntry('INFO', 'Q-learning agent ready for training');
    }, 1000);
});
