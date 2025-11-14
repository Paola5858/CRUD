/**
 * MOTOSENSE - Dashboard Interativo
 * @fileoverview Scripts para gráficos e interações do dashboard
 * @author Paola Machado
 * @version 2.0.0
 */

/**
 * Configuração global dos gráficos Chart.js
 * @constant {Object}
 */
const CHART_DEFAULTS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#ff6b00',
            bodyColor: '#fff',
            borderColor: '#ff6b00',
            borderWidth: 1
        }
    }
};

/**
 * Inicializa o gráfico principal de linhas
 * @param {string} canvasId - ID do elemento canvas
 * @param {Array} data - Array de dados para plotar
 * @param {Array} labels - Labels para o eixo X
 * @returns {Chart} Instância do Chart.js
 * 
 * @example
 * const chart = initLineChart('mainChart', [10, 20, 30], ['Jan', 'Feb', 'Mar']);
 */
function initLineChart(canvasId, data, labels) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Valor do Sensor',
                data: data,
                borderColor: '#ff6b00',
                backgroundColor: 'rgba(255, 107, 0, 0.2)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: '#ff6b00',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            ...CHART_DEFAULTS,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#808080',
                        callback: function(value) {
                            return value.toFixed(1);
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#808080',
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Atualiza dados do gráfico em tempo real
 * @param {Chart} chart - Instância do Chart.js
 * @param {number} newValue - Novo valor a adicionar
 * @param {string} newLabel - Novo label (timestamp)
 * @param {number} maxDataPoints - Máximo de pontos a exibir
 * 
 * @example
 * updateChartData(myChart, 42.5, '14:30:00', 10);
 */
function updateChartData(chart, newValue, newLabel, maxDataPoints = 10) {
    // Adicionar novo dado
    chart.data.labels.push(newLabel);
    chart.data.datasets[0].data.push(newValue);
    
    // Remover dados antigos se exceder limite
    if (chart.data.labels.length > maxDataPoints) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    
    // Animar atualização
    chart.update('active');
}

/**
 * Classe para gerenciar conexão WebSocket com worker MQTT
 * @class
 */
class MqttDashboardConnector {
    /**
     * Cria uma nova instância do connector
     * @param {string} wsUrl - URL do WebSocket
     * @param {Function} onMessageCallback - Callback para mensagens recebidas
     */
    constructor(wsUrl, onMessageCallback) {
        this.wsUrl = wsUrl;
        this.onMessageCallback = onMessageCallback;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }
    
    /**
     * Estabelece conexão WebSocket
     * @returns {Promise<void>}
     */
    async connect() {
        try {
            this.ws = new WebSocket(this.wsUrl);
            
            this.ws.onopen = () => {
                console.log('✅ Conectado ao MQTT Worker');
                this.reconnectAttempts = 0;
            };
            
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.onMessageCallback(data);
            };
            
            this.ws.onerror = (error) => {
                console.error('❌ Erro WebSocket:', error);
            };
            
            this.ws.onclose = () => {
                console.warn('⚠️ Conexão fechada. Tentando reconectar...');
                this.reconnect();
            };
        } catch (error) {
            console.error('Erro ao conectar:', error);
            this.reconnect();
        }
    }
    
    /**
     * Tenta reconectar ao WebSocket
     * @private
     */
    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
            
            console.log(`🔄 Reconectando em ${delay/1000}s (tentativa ${this.reconnectAttempts})`);
            
            setTimeout(() => this.connect(), delay);
        } else {
            console.error('❌ Máximo de tentativas de reconexão atingido');
        }
    }
}