/**
 * ═══════════════════════════════════════════════════════════════
 * MOTOSENSE DASHBOARD - JAVASCRIPT
 * Chart.js integration using backend-provided data.
 * ═══════════════════════════════════════════════════════════════
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🏍️ MOTOSENSE Dashboard Initializing...');

    if (typeof Chart === 'undefined') {
        console.error('❌ Chart.js is not available. Dashboard cannot be initialized.');
        return;
    }

    // Initialize all charts with a single delay
    setTimeout(() => {
        console.log('Initializing charts...');
        initMainChart();
        initBarChart();
        initGaugeChart();
    }, 300);

    // Update time immediately and then every second
    updateTime();
    setInterval(updateTime, 1000);

    console.log('🔥 MOTOSENSE Dashboard Ready!');
});

// ━━━ CHART CONFIGURATIONS ━━━
const chartColors = {
    orange: '#ff6b00',
    cyan: '#00d9ff',
    amber: '#ffaa00',
    green: '#00ff41',
    red: '#ff3333',
    white: '#ffffff',
    gray: '#808080'
};

// ━━━ MAIN CHART (LINE) ━━━
function initMainChart() {
    const ctx = document.getElementById('mainChart');
    if (!ctx) {
        console.warn('MainChart canvas not found');
        return;
    }

    // Sample data for demonstration
    const data = {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        datasets: [
            { label: 'Temperatura', data: [65, 70, 75, 80, 78, 72], borderColor: chartColors.orange, backgroundColor: chartColors.orange + '20', borderWidth: 3, fill: true, tension: 0.4 },
            { label: 'Pressão', data: [2.1, 2.3, 2.5, 2.4, 2.2, 2.0], borderColor: chartColors.cyan, backgroundColor: chartColors.cyan + '20', borderWidth: 3, fill: true, tension: 0.4 },
            { label: 'Velocidade', data: [1800, 2200, 2800, 3200, 2900, 2400], borderColor: chartColors.amber, backgroundColor: chartColors.amber + '20', borderWidth: 3, fill: true, tension: 0.4 }
        ]
    };

    const config = createChartConfig(data);
    new Chart(ctx, config);
    console.log('Main chart initialized successfully');
}

// ━━━ BAR CHART ━━━
function initBarChart() {
    const ctx = document.getElementById('barChart');
    if (!ctx) {
        console.warn('BarChart canvas not found');
        return;
    }

    // Sample data for demonstration
    const data = {
        labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        datasets: [
            { label: 'Temperatura', data: [68, 72, 75, 78, 76, 70, 69], backgroundColor: chartColors.orange + '80', borderColor: chartColors.orange, borderWidth: 2 },
            { label: 'Pressão', data: [2.2, 2.4, 2.3, 2.5, 2.1, 2.0, 2.3], backgroundColor: chartColors.cyan + '80', borderColor: chartColors.cyan, borderWidth: 2 },
            { label: 'Velocidade', data: [2000, 2400, 2800, 3200, 2900, 2200, 2100], backgroundColor: chartColors.amber + '80', borderColor: chartColors.amber, borderWidth: 2 }
        ]
    };

    const config = createChartConfig(data, 'bar');
    config.options.scales.y.ticks.callback = value => (value / 1000) + 'K';
    new Chart(ctx, config);
    console.log('Bar chart initialized successfully');
}

// ━━━ GAUGE CHART ━━━
function initGaugeChart() {
    const ctx = document.getElementById('gaugeChart');
    if (!ctx) {
        console.warn('GaugeChart canvas not found');
        return;
    }

    // Sample value for demonstration
    const value = 75;

    const data = {
        datasets: [{
            data: [value, 100 - value],
            backgroundColor: [chartColors.green, '#333333'],
            borderWidth: 0,
            cutout: '80%',
            circumference: 180,
            rotation: 270
        }]
    };

    const config = { type: 'doughnut', data: data, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } } };
    new Chart(ctx, config);
    console.log('Gauge chart initialized successfully');
}

// ━━━ UTILITY FUNCTIONS ━━━
function createChartConfig(data, type = 'line') {
    return {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: '#333', borderColor: '#666' }, ticks: { color: '#808080', font: { family: 'Barlow', size: 12, weight: '600' } } },
                y: { grid: { color: '#333', borderColor: '#666' }, ticks: { color: '#808080', font: { family: 'Barlow', size: 12, weight: '600' } } }
            },
            elements: { point: { radius: 6, hoverRadius: 8, borderWidth: 2, backgroundColor: '#000' } }
        }
    };
}

function updateTime() {
    const now = new Date();
    const timeElement = document.querySelector('.current-time');
    const dateElement = document.querySelector('.current-date');
    
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    }
    
    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();
    }
}