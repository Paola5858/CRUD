/**
 * ═══════════════════════════════════════════════════════════════
 * MOTOSENSE DASHBOARD - JAVASCRIPT
 * Chart.js integration and real-time updates
 * ═══════════════════════════════════════════════════════════════
 */

// ━━━ GLOBAL VARIABLES ━━━
let mainChartInstance = null;
let donutChartInstance = null;
let barChartInstance = null;
let gaugeChartInstance = null;

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
    if (!ctx) return;

    // Usar dados do backend se disponíveis
    const backendData = window.DASHBOARD_BACKEND?.chart_data || {
        labels: ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'],
        temperatura: [15, 18, 22, 28, 24, 30, 38, 32, 35, 40, 42, 45],
        pressao: [12, 15, 18, 24, 20, 25, 32, 28, 30, 35, 38, 40],
        velocidade: [10, 13, 16, 22, 18, 23, 30, 26, 28, 33, 36, 38]
    };

    const data = {
        labels: backendData.labels,
        datasets: [
            {
                label: 'Temperatura',
                data: backendData.temperatura,
                borderColor: chartColors.orange,
                backgroundColor: chartColors.orange + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            },
            {
                label: 'Pressão',
                data: backendData.pressao,
                borderColor: chartColors.cyan,
                backgroundColor: chartColors.cyan + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            },
            {
                label: 'Velocidade',
                data: backendData.velocidade,
                borderColor: chartColors.amber,
                backgroundColor: chartColors.amber + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        color: '#333333',
                        borderColor: '#666666'
                    },
                    ticks: {
                        color: '#808080',
                        font: {
                            family: 'Barlow',
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                y: {
                    grid: {
                        color: '#333333',
                        borderColor: '#666666'
                    },
                    ticks: {
                        color: '#808080',
                        font: {
                            family: 'Barlow',
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            },
            elements: {
                point: {
                    radius: 6,
                    hoverRadius: 8,
                    borderWidth: 2,
                    backgroundColor: '#000000'
                }
            }
        }
    };

    mainChartInstance = new Chart(ctx, config);
}

// ━━━ DONUT CHART ━━━
function initDonutChart() {
    const ctx = document.getElementById('donutChart');
    if (!ctx) return;

    const data = {
        labels: ['Temperatura', 'Pressão', 'Velocidade'],
        datasets: [{
            data: [35, 25, 40],
            backgroundColor: [
                chartColors.orange,
                chartColors.cyan,
                chartColors.amber
            ],
            borderColor: '#000000',
            borderWidth: 3,
            cutout: '70%'
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    };

    donutChartInstance = new Chart(ctx, config);
}

// ━━━ BAR CHART ━━━
function initBarChart() {
    const ctx = document.getElementById('barChart');
    if (!ctx) return;

    const data = {
        labels: ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB', 'DOM'],
        datasets: [
            {
                label: 'Temperatura',
                data: [12000, 15000, 18000, 22000, 35000, 28000, 16000],
                backgroundColor: chartColors.orange + '80',
                borderColor: chartColors.orange,
                borderWidth: 2
            },
            {
                label: 'Pressão',
                data: [8000, 12000, 14000, 18000, 28000, 22000, 12000],
                backgroundColor: chartColors.cyan + '80',
                borderColor: chartColors.cyan,
                borderWidth: 2
            },
            {
                label: 'Velocidade',
                data: [10000, 13000, 16000, 20000, 32000, 25000, 14000],
                backgroundColor: chartColors.amber + '80',
                borderColor: chartColors.amber,
                borderWidth: 2
            }
        ]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#808080',
                        font: {
                            family: 'Barlow',
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                y: {
                    grid: {
                        color: '#333333'
                    },
                    ticks: {
                        color: '#808080',
                        font: {
                            family: 'Barlow',
                            size: 12,
                            weight: '600'
                        },
                        callback: function(value) {
                            return (value / 1000) + 'K';
                        }
                    }
                }
            }
        }
    };

    barChartInstance = new Chart(ctx, config);
}

// ━━━ GAUGE CHART ━━━
function initGaugeChart() {
    const ctx = document.getElementById('gaugeChart');
    if (!ctx) return;

    const data = {
        datasets: [{
            data: [92, 8], // 92% filled, 8% empty
            backgroundColor: [
                chartColors.green,
                '#333333'
            ],
            borderWidth: 0,
            cutout: '80%',
            circumference: 180,
            rotation: 270
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    };

    gaugeChartInstance = new Chart(ctx, config);
}

// ━━━ REAL-TIME UPDATES ━━━
function updateTime() {
    const now = new Date();
    const timeElement = document.querySelector('.current-time');
    const dateElement = document.querySelector('.current-date');
    
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        }).toUpperCase();
    }
}

// ━━━ API INTEGRATION ━━━
async function fetchDashboardData() {
    try {
        const response = await fetch('/dashboard/api/metrics/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        // Return fallback data
        return {
            chart_main: {
                labels: ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'],
                temperatura: [15, 18, 22, 28, 24, 30, 38, 32, 35, 40, 42, 45],
                pressao: [12, 15, 18, 24, 20, 25, 32, 28, 30, 35, 38, 40],
                velocidade: [10, 13, 16, 22, 18, 23, 30, 26, 28, 33, 36, 38]
            },
            metrics: {
                total_motores: 12,
                total_sensores: 24,
                crescimento: 47.8
            },
            status: 'fallback'
        };
    }
}

function updateChartData(data) {
    if (mainChartInstance && data.chart_main) {
        mainChartInstance.data.datasets[0].data = data.chart_main.temperatura;
        mainChartInstance.data.datasets[1].data = data.chart_main.pressao;
        mainChartInstance.data.datasets[2].data = data.chart_main.velocidade;
        mainChartInstance.update('none');
    }
}

function updateMetrics() {
    const metrics = window.DASHBOARD_BACKEND?.metrics;
    if (!metrics) return;
    
    // Atualizar métricas na interface
    const elements = {
        totalMotores: document.querySelector('.stat-value:contains("MOTORES")')?.parentElement?.querySelector('.stat-value'),
        totalSensores: document.querySelector('.stat-value:contains("SENSORES")')?.parentElement?.querySelector('.stat-value'),
        temperatura: document.querySelector('.metric-value'),
        rpm: document.querySelectorAll('.metric-value')[1]
    };
    
    // Atualizar valores se elementos existirem
    Object.keys(elements).forEach(key => {
        const element = elements[key];
        if (element && metrics[key]) {
            element.textContent = metrics[key];
        }
    });
}

// ━━━ INITIALIZATION ━━━
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏍️ MOTOSENSE Dashboard Initializing...');
    
    // Initialize charts
    setTimeout(() => {
        initMainChart();
        initDonutChart();
        initBarChart();
        initGaugeChart();
    }, 100);
    
    // Update time immediately and then every second
    updateTime();
    setInterval(updateTime, 1000);
    
    // Load initial data
    setTimeout(async () => {
        // Primeiro usar dados do backend se disponíveis
        if (window.DASHBOARD_BACKEND) {
            updateMetrics();
        }
        
        // Depois tentar buscar dados da API
        const data = await fetchDashboardData();
        if (data.status === 'success' || data.status === 'fallback') {
            updateChartData(data);
        }
    }, 1000);
    
    // Set up real-time updates every 30 seconds
    setInterval(async () => {
        const data = await fetchDashboardData();
        if (data.status === 'success' || data.status === 'fallback') {
            updateChartData(data);
        }
    }, 30000);
    
    console.log('🔥 MOTOSENSE Dashboard Ready!');
});

// ━━━ EXPORT FOR GLOBAL ACCESS ━━━
window.MOTOSENSE_DASHBOARD = {
    mainChartInstance,
    donutChartInstance,
    barChartInstance,
    gaugeChartInstance,
    updateChartData,
    fetchDashboardData
};

/**
 * ═══════════════════════════════════════════════════════════════
 * END OF MOTOSENSE DASHBOARD JAVASCRIPT
 * ═══════════════════════════════════════════════════════════════
 */