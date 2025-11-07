/**
 * ═══════════════════════════════════════════════════════════════
 * MOTOSENSE - API INTEGRATION
 * Real-time data integration with Django backend
 * ═══════════════════════════════════════════════════════════════
 */

// ━━━ API ENDPOINTS ━━━
const API_ENDPOINTS = {
    metrics: '/dashboard/api/metrics/',
    motorStatus: '/dashboard/api/motor-status/',
    alerts: '/dashboard/api/alerts/'
};

// ━━━ API CLIENT ━━━
class MotosenseAPI {
    constructor() {
        this.baseURL = window.location.origin;
        this.cache = new Map();
        this.cacheTimeout = 30000; // 30 seconds
    }

    async fetchWithCache(endpoint, options = {}) {
        const cacheKey = endpoint + JSON.stringify(options);
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        try {
            const response = await fetch(this.baseURL + endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Cache the response
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });

            return data;
        } catch (error) {
            console.error('API Error:', error);
            
            // Retornar dados simulados como fallback
            return this.getFallbackData(endpoint);
        }
    }

    getFallbackData(endpoint) {
        const fallbackData = {
            '/dashboard/api/metrics/': {
                chart_main: {
                    labels: ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'],
                    temperatura: [15, 18, 22, 28, 24, 30, 38, 32, 35, 40, 42, 45],
                    pressao: [12, 15, 18, 24, 20, 25, 32, 28, 30, 35, 38, 40],
                    velocidade: [10, 13, 16, 22, 18, 23, 30, 26, 28, 33, 36, 38]
                },
                metrics: {
                    total_motores: 12,
                    total_sensores: 24,
                    crescimento: 47.8,
                    temperatura_media: 78,
                    rpm_medio: 3450,
                    alertas_criticos: 3
                },
                status: 'fallback'
            },
            '/dashboard/api/motor-status/': {
                motores: [
                    {nome: 'Motor A1', potencia: 1500, temperatura: 85, online: true},
                    {nome: 'Motor B2', potencia: 1200, temperatura: 78, online: true},
                    {nome: 'Motor C3', potencia: 1800, temperatura: 92, online: false}
                ],
                online_count: 2,
                status: 'fallback'
            },
            '/dashboard/api/alerts/': {
                alerts: [
                    {tipo: 'critical', icon: '🔥', titulo: 'TEMPERATURA CRÍTICA', detalhes: 'Motor D4 • 98°C', timestamp: 'Há 2 min'}
                ],
                count: 1,
                status: 'fallback'
            }
        };
        
        return fallbackData[endpoint] || {status: 'error', message: 'Dados não disponíveis'};
    }

    async getMetrics() {
        return this.fetchWithCache(API_ENDPOINTS.metrics);
    }

    async getMotorStatus() {
        return this.fetchWithCache(API_ENDPOINTS.motorStatus);
    }

    async getAlerts() {
        return this.fetchWithCache(API_ENDPOINTS.alerts);
    }
}

// ━━━ GLOBAL API INSTANCE ━━━
const motosenseAPI = new MotosenseAPI();

// ━━━ DATA UPDATERS ━━━
async function updateDashboardMetrics() {
    try {
        const data = await motosenseAPI.getMetrics();
        
        if (data.status === 'success' || data.status === 'fallback') {
            // Update header metrics
            if (data.metrics) updateHeaderMetrics(data.metrics);
            
            // Update main chart if it exists
            if (data.chart_main) updateMainChart(data.chart_main);
            
            // Update donut chart
            if (data.sensor_distribution) updateDonutChart(data.sensor_distribution);
            
            // Update weekly performance
            if (data.weekly_performance) updateWeeklyChart(data.weekly_performance);
            
            // Update gauge
            if (data.gauge_value !== undefined) updateGaugeChart(data.gauge_value);
            
            // Show fallback warning if using fallback data
            if (data.status === 'fallback') {
                console.warn('⚠️ Usando dados simulados - API indisponível');
            }
        }
    } catch (error) {
        console.error('Failed to update dashboard metrics:', error);
        showErrorNotification('Erro ao carregar métricas do dashboard');
    }
}

async function updateMotorStatus() {
    try {
        const data = await motosenseAPI.getMotorStatus();
        
        if (data.status === 'success') {
            updateMotorList(data.motores);
            updateOnlineCount(data.online_count);
        }
    } catch (error) {
        console.error('Failed to update motor status:', error);
        showErrorNotification('Erro ao carregar status dos motores');
    }
}

async function updateAlerts() {
    try {
        const data = await motosenseAPI.getAlerts();
        
        if (data.status === 'success') {
            updateAlertsList(data.alerts);
            updateAlertCount(data.count);
        }
    } catch (error) {
        console.error('Failed to update alerts:', error);
        showErrorNotification('Erro ao carregar alertas');
    }
}

// ━━━ UI UPDATERS ━━━
function updateHeaderMetrics(metrics) {
    const elements = {
        temperature: document.querySelector('.metric-card .metric-value'),
        rpm: document.querySelectorAll('.metric-card .metric-value')[1],
        alerts: document.querySelectorAll('.metric-card .metric-value')[2]
    };

    if (elements.temperature) {
        elements.temperature.textContent = `${metrics.temperatura_media}°C`;
    }
    
    if (elements.rpm) {
        elements.rpm.textContent = metrics.rpm_medio.toLocaleString('pt-BR');
    }
    
    if (elements.alerts) {
        elements.alerts.textContent = String(metrics.alertas_criticos).padStart(2, '0');
    }

    // Update large metric cards
    const metricValues = document.querySelectorAll('.metric-value-large');
    if (metricValues[0]) {
        metricValues[0].textContent = metrics.total_leituras.toLocaleString('pt-BR');
    }
    if (metricValues[1]) {
        metricValues[1].textContent = `${metrics.potencia_media} W`;
    }
    if (metricValues[2]) {
        metricValues[2].textContent = `${metrics.uptime}%`;
    }
}

function updateMainChart(chartData) {
    if (window.mainChartInstance && chartData) {
        window.mainChartInstance.data.labels = chartData.labels;
        window.mainChartInstance.data.datasets[0].data = chartData.temperatura;
        window.mainChartInstance.data.datasets[1].data = chartData.pressao;
        window.mainChartInstance.data.datasets[2].data = chartData.velocidade;
        window.mainChartInstance.update('none');
    }
}

function updateDonutChart(sensorData) {
    if (window.donutChartInstance && sensorData) {
        const values = sensorData.map(item => item.percentage);
        window.donutChartInstance.data.datasets[0].data = values;
        window.donutChartInstance.update('none');
        
        // Update legend
        updateDonutLegend(sensorData);
    }
}

function updateDonutLegend(sensorData) {
    const legendItems = document.querySelectorAll('.legend-item-detailed');
    
    sensorData.forEach((item, index) => {
        if (legendItems[index]) {
            const countElement = legendItems[index].querySelector('.legend-count');
            const percentElement = legendItems[index].querySelector('.legend-percent');
            const progressFill = legendItems[index].querySelector('.progress-fill');
            
            if (countElement) countElement.textContent = item.count;
            if (percentElement) percentElement.textContent = `(${item.percentage}%)`;
            if (progressFill) progressFill.style.width = `${item.percentage}%`;
        }
    });
}

function updateWeeklyChart(weeklyData) {
    if (window.barChartInstance && weeklyData) {
        window.barChartInstance.data.datasets[0].data = weeklyData.temperatura;
        window.barChartInstance.data.datasets[1].data = weeklyData.pressao;
        window.barChartInstance.data.datasets[2].data = weeklyData.velocidade;
        window.barChartInstance.update('none');
    }
}

function updateGaugeChart(gaugeValue) {
    if (window.gaugeChartInstance && gaugeValue !== undefined) {
        window.gaugeChartInstance.data.datasets[0].data = [gaugeValue, 100 - gaugeValue];
        window.gaugeChartInstance.update('none');
        
        // Update gauge center value
        const gaugeValueElement = document.querySelector('.gauge-value');
        if (gaugeValueElement) {
            gaugeValueElement.textContent = `${gaugeValue}%`;
        }
    }
}

function updateMotorList(motores) {
    const motorList = document.querySelector('.motor-list');
    if (!motorList || !motores) return;

    motorList.innerHTML = '';
    
    motores.forEach(motor => {
        const motorItem = document.createElement('div');
        motorItem.className = `motor-item ${motor.online ? 'online' : 'offline'}`;
        
        motorItem.innerHTML = `
            <div class="motor-icon">🏍️</div>
            <div class="motor-info">
                <div class="motor-name">${motor.nome}</div>
                <div class="motor-power">${motor.potencia}W</div>
                <div class="motor-temp">${motor.online ? motor.temperatura + '°C' : '--°C'}</div>
            </div>
            <div class="status-indicator ${motor.online ? 'online' : 'offline'}"></div>
        `;
        
        motorList.appendChild(motorItem);
    });
}

function updateOnlineCount(count) {
    const onlineBadge = document.querySelector('.online-badge');
    if (onlineBadge) {
        onlineBadge.textContent = `${count} ONLINE`;
    }
}

function updateAlertsList(alerts) {
    const alertsList = document.querySelector('.alerts-list');
    if (!alertsList || !alerts) return;

    alertsList.innerHTML = '';
    
    alerts.forEach(alert => {
        const alertItem = document.createElement('div');
        alertItem.className = `alert-item ${alert.tipo}`;
        
        alertItem.innerHTML = `
            <div class="alert-icon ${alert.tipo === 'critical' ? 'pulsing' : ''}">${alert.icon}</div>
            <div class="alert-content">
                <div class="alert-title">${alert.titulo}</div>
                <div class="alert-details">${alert.detalhes}</div>
                <div class="alert-timestamp">${alert.timestamp}</div>
                <button class="alert-action">VER DETALHES ›</button>
            </div>
        `;
        
        alertsList.appendChild(alertItem);
    });
}

function updateAlertCount(count) {
    const alertCount = document.querySelector('.alert-count');
    if (alertCount) {
        alertCount.textContent = String(count).padStart(2, '0');
    }
}

// ━━━ ERROR HANDLING ━━━
function showErrorNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'error-notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ff3333, #cc0000);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(255, 51, 51, 0.5);
        z-index: 9999;
        font-family: 'Barlow', sans-serif;
        font-weight: 600;
        font-size: 14px;
        max-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// ━━━ REAL-TIME UPDATE MANAGER ━━━
class RealTimeManager {
    constructor() {
        this.intervals = new Map();
        this.isActive = true;
    }

    start() {
        if (!this.isActive) return;

        // Update metrics every 30 seconds
        this.intervals.set('metrics', setInterval(() => {
            updateDashboardMetrics();
        }, 30000));

        // Update motor status every 10 seconds
        this.intervals.set('motors', setInterval(() => {
            updateMotorStatus();
        }, 10000));

        // Update alerts every 15 seconds
        this.intervals.set('alerts', setInterval(() => {
            updateAlerts();
        }, 15000));

        console.log('🔄 Real-time updates started');
    }

    stop() {
        this.intervals.forEach((interval, key) => {
            clearInterval(interval);
            this.intervals.delete(key);
        });
        
        this.isActive = false;
        console.log('⏹️ Real-time updates stopped');
    }

    pause() {
        this.stop();
        this.isActive = false;
    }

    resume() {
        this.isActive = true;
        this.start();
    }
}

// ━━━ GLOBAL REAL-TIME MANAGER ━━━
const realTimeManager = new RealTimeManager();

// ━━━ PAGE VISIBILITY API ━━━
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        realTimeManager.pause();
    } else {
        realTimeManager.resume();
    }
});

// ━━━ INITIALIZATION ━━━
document.addEventListener('DOMContentLoaded', () => {
    // Initial data load
    setTimeout(() => {
        updateDashboardMetrics();
        updateMotorStatus();
        updateAlerts();
    }, 1000);

    // Start real-time updates
    setTimeout(() => {
        realTimeManager.start();
    }, 2000);
});

// ━━━ CLEANUP ON PAGE UNLOAD ━━━
window.addEventListener('beforeunload', () => {
    realTimeManager.stop();
});

// ━━━ EXPORT FOR GLOBAL ACCESS ━━━
window.MotosenseAPI = {
    api: motosenseAPI,
    realTimeManager: realTimeManager,
    updateDashboardMetrics,
    updateMotorStatus,
    updateAlerts
};

/**
 * ═══════════════════════════════════════════════════════════════
 * END OF API INTEGRATION
 * ═══════════════════════════════════════════════════════════════
 */