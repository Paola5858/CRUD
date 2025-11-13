/**
 * ═══════════════════════════════════════════════════════════════
 * MOTOSENSE DASHBOARD - JAVASCRIPT
 * Chart.js integration using backend-provided data.
 * ═══════════════════════════════════════════════════════════════
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🏍️ MOTOSENSE Dashboard Initializing...');

    if (!window.DASHBOARD_BACKEND || typeof Chart === 'undefined') {
        console.error('❌ Backend data or Chart.js is not available. Dashboard cannot be initialized.');
        return;
    }

    const backendData = window.DASHBOARD_BACKEND;
    console.log('✅ Backend data loaded:', backendData);

    // Initialize all charts with a single delay
    setTimeout(() => {
        console.log('Initializing charts...');
        initMainChart(backendData.chart_main);
        initBarChart(backendData.weekly_performance);
        initGaugeChart(backendData.gauge_value);
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
function initMainChart(chartData) {
    const ctx = document.getElementById('mainChart');
    if (!ctx || !chartData) {
        console.warn('MainChart canvas or data not found');
        return;
    }

    const data = {
        labels: chartData.labels,
        datasets: [
            { label: 'Temperatura', data: chartData.temperatura, borderColor: chartColors.orange, backgroundColor: chartColors.orange + '20', borderWidth: 3, fill: true, tension: 0.4 },
            { label: 'Pressão', data: chartData.pressao, borderColor: chartColors.cyan, backgroundColor: chartColors.cyan + '20', borderWidth: 3, fill: true, tension: 0.4 },
            { label: 'Velocidade', data: chartData.velocidade, borderColor: chartColors.amber, backgroundColor: chartColors.amber + '20', borderWidth: 3, fill: true, tension: 0.4 }
        ]
    };

    const config = createChartConfig(data);
    new Chart(ctx, config);
    console.log('Main chart initialized successfully');
}

// ━━━ BAR CHART ━━━
function initBarChart(chartData) {
    const ctx = document.getElementById('barChart');
    if (!ctx || !chartData) {
        console.warn('BarChart canvas or data not found');
        return;
    }

    const data = {
        labels: chartData.labels,
        datasets: [
            { label: 'Temperatura', data: chartData.temperatura, backgroundColor: chartColors.orange + '80', borderColor: chartColors.orange, borderWidth: 2 },
            { label: 'Pressão', data: chartData.pressao, backgroundColor: chartColors.cyan + '80', borderColor: chartColors.cyan, borderWidth: 2 },
            { label: 'Velocidade', data: chartData.velocidade, backgroundColor: chartColors.amber + '80', borderColor: chartColors.amber, borderWidth: 2 }
        ]
    };

    const config = createChartConfig(data, 'bar');
    config.options.scales.y.ticks.callback = value => (value / 1000) + 'K';
    new Chart(ctx, config);
    console.log('Bar chart initialized successfully');
}

// ━━━ GAUGE CHART ━━━
function initGaugeChart(value) {
    const ctx = document.getElementById('gaugeChart');
    if (!ctx) {
        console.warn('GaugeChart canvas not found');
        return;
    }

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