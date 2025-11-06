// Dashboard Analytics JavaScript
class Dashboard {
    constructor() {
        this.charts = {};
        this.init();
    }

    async init() {
        await this.loadData();
        this.initCharts();
        this.loadMotorStatus();
        this.setupEventListeners();
    }

    async loadData() {
        try {
            const response = await fetch('/dashboard/api/metrics/');
            this.data = await response.json();
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            this.data = this.getMockData();
        }
    }

    getMockData() {
        return {
            chart_main: {
                labels: ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'],
                data: [120, 190, 300, 500, 200, 300, 450, 280, 350, 400, 480, 520]
            },
            metrics: {
                total_motores: 12,
                total_sensores: 24,
                leituras_hoje: 1547,
                crescimento: 47.8
            },
            sensor_distribution: [
                { tipo: 'Temperatura', count: 8 },
                { tipo: 'Pressão', count: 6 },
                { tipo: 'Velocidade', count: 10 }
            ]
        };
    }

    initCharts() {
        this.createMainChart();
        this.createDonutChart();
        this.updateMetrics();
    }

    createMainChart() {
        const ctx = document.getElementById('chart-main').getContext('2d');
        
        this.charts.main = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.data.chart_main.labels,
                datasets: [{
                    label: 'Dados Coletados',
                    data: this.data.chart_main.data,
                    borderColor: '#ff1493',
                    backgroundColor: 'rgba(255, 20, 147, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#ff1493',
                    pointBorderColor: '#ff1493',
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        grid: { 
                            color: '#333',
                            drawBorder: false
                        },
                        ticks: { 
                            color: '#ccc',
                            font: { size: 12 }
                        }
                    },
                    x: {
                        grid: { 
                            color: '#333',
                            drawBorder: false
                        },
                        ticks: { 
                            color: '#ccc',
                            font: { size: 12 }
                        }
                    }
                },
                elements: {
                    point: {
                        hoverBackgroundColor: '#ff69b4'
                    }
                }
            }
        });
    }

    createDonutChart() {
        const ctx = document.getElementById('chart-donut').getContext('2d');
        
        const colors = ['#ff1493', '#ff69b4', '#ff8fa3'];
        const labels = this.data.sensor_distribution.map(item => item.tipo);
        const data = this.data.sensor_distribution.map(item => item.count);
        
        this.charts.donut = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderColor: '#1a1a1a',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#ccc',
                            font: { size: 12 },
                            padding: 20
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }

    updateMetrics() {
        const metrics = this.data.metrics;
        
        document.getElementById('growth-percentage').textContent = `+${metrics.crescimento}%`;
        document.getElementById('total-readings').textContent = `${metrics.leituras_hoje.toLocaleString()} leituras`;
    }

    async loadMotorStatus() {
        try {
            const response = await fetch('/dashboard/api/motor-status/');
            const data = await response.json();
            this.renderMotorStatus(data.motores);
        } catch (error) {
            console.error('Erro ao carregar status dos motores:', error);
            this.renderMotorStatus(this.getMockMotorStatus());
        }
    }

    getMockMotorStatus() {
        return [
            { nome: 'Motor A1', potencia: 1500, online: true, ultima_atualizacao: new Date().toISOString() },
            { nome: 'Motor B2', potencia: 2200, online: true, ultima_atualizacao: new Date().toISOString() },
            { nome: 'Motor C3', potencia: 1800, online: false, ultima_atualizacao: null },
            { nome: 'Motor D4', potencia: 3000, online: true, ultima_atualizacao: new Date().toISOString() },
            { nome: 'Motor E5', potencia: 1200, online: true, ultima_atualizacao: new Date().toISOString() }
        ];
    }

    renderMotorStatus(motores) {
        const container = document.getElementById('motor-status-list');
        const onlineCount = motores.filter(m => m.online).length;
        
        document.getElementById('online-count').textContent = `${onlineCount} online`;
        
        container.innerHTML = motores.map(motor => `
            <div class="status-item ${motor.online ? 'online' : 'offline'}">
                <div class="motor-info">
                    <h4>${motor.nome}</h4>
                    <p>${motor.potencia}W - ${motor.online ? 'Online' : 'Offline'}</p>
                </div>
                <div class="status-indicator ${motor.online ? 'online' : 'offline'}"></div>
            </div>
        `).join('');
    }

    setupEventListeners() {
        // Filtros
        document.getElementById('filter-period').addEventListener('change', () => {
            this.updateCharts();
        });
        
        document.getElementById('filter-year').addEventListener('change', () => {
            this.updateCharts();
        });
        
        // Auto-refresh a cada 30 segundos
        setInterval(() => {
            this.loadMotorStatus();
        }, 30000);
    }

    async updateCharts() {
        await this.loadData();
        
        // Atualizar gráfico principal
        this.charts.main.data.labels = this.data.chart_main.labels;
        this.charts.main.data.datasets[0].data = this.data.chart_main.data;
        this.charts.main.update();
        
        // Atualizar métricas
        this.updateMetrics();
    }
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});