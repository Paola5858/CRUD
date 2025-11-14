/**
 * MOTOSENSE - Real-time WebSocket Dashboard
 * Conexão WebSocket para atualizações em tempo real
 */

class MotosenseRealtime {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.isConnected = false;
        
        this.init();
    }
    
    init() {
        this.connect();
        this.setupEventListeners();
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/dashboard/`;
        
        try {
            this.socket = new WebSocket(wsUrl);
            
            this.socket.onopen = (event) => {
                console.log('🔗 WebSocket conectado');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.updateConnectionStatus(true);
                
                // Solicitar KPIs iniciais
                this.send({
                    type: 'get_kpis'
                });
            };
            
            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            };
            
            this.socket.onclose = (event) => {
                console.log('❌ WebSocket desconectado');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                this.attemptReconnect();
            };
            
            this.socket.onerror = (error) => {
                console.error('🚨 Erro WebSocket:', error);
                this.updateConnectionStatus(false);
            };
            
        } catch (error) {
            console.error('Erro ao conectar WebSocket:', error);
            this.attemptReconnect();
        }
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'sensor_data':
                this.updateSensorData(data.data);
                break;
            case 'kpis_update':
                this.updateKPIs(data.data);
                break;
            case 'alert':
                this.showAlert(data.data);
                break;
            default:
                console.log('Mensagem desconhecida:', data);
        }
    }
    
    updateSensorData(sensorData) {
        // Atualizar gráficos em tempo real
        if (window.mainChart) {
            const now = new Date().toLocaleTimeString();
            updateChartData(window.mainChart, sensorData.valor, now);
        }
        
        // Atualizar tabela de dados
        this.updateDataTable(sensorData);
        
        // Animação visual
        this.animateNewData();
    }
    
    updateKPIs(kpis) {
        // Atualizar cards KPI
        const elements = {
            'total-motores': kpis.total_motores,
            'total-sensores': kpis.total_sensores,
            'dados-hoje': kpis.dados_hoje
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                this.animateValue(element, parseInt(element.textContent) || 0, value);
            }
        });
        
        // Atualizar últimos dados
        if (kpis.ultimos_dados) {
            this.updateRecentData(kpis.ultimos_dados);
        }
    }
    
    updateDataTable(newData) {
        const tableBody = document.querySelector('#data-table tbody');
        if (!tableBody) return;
        
        // Criar nova linha
        const row = document.createElement('tr');
        row.className = 'new-data-row';
        row.innerHTML = `
            <td>${newData.motor_nome}</td>
            <td>${newData.sensor_tipo}</td>
            <td class="valor-cell">${newData.valor}</td>
            <td>${newData.temperatura || '--'}°C</td>
            <td>${newData.rpm || '--'}</td>
            <td>${new Date().toLocaleTimeString()}</td>
        `;
        
        // Inserir no topo
        tableBody.insertBefore(row, tableBody.firstChild);
        
        // Remover linhas antigas (manter apenas 10)
        while (tableBody.children.length > 10) {
            tableBody.removeChild(tableBody.lastChild);
        }
        
        // Animação de entrada
        setTimeout(() => {
            row.classList.remove('new-data-row');
        }, 1000);
    }
    
    showAlert(alertData) {
        // Criar toast de alerta
        const toast = document.createElement('div');
        toast.className = `alert-toast ${alertData.tipo.toLowerCase()}`;
        toast.innerHTML = `
            <div class="alert-icon">${this.getAlertIcon(alertData.tipo)}</div>
            <div class="alert-content">
                <div class="alert-title">${alertData.titulo}</div>
                <div class="alert-message">${alertData.mensagem}</div>
            </div>
            <button class="alert-close" onclick="this.parentElement.remove()">×</button>
        `;
        
        // Adicionar ao container
        const container = document.getElementById('alerts-container') || document.body;
        container.appendChild(toast);
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
        
        // Efeito sonoro (opcional)
        if (alertData.tipo === 'CRITICO') {
            this.playAlertSound();
        }
    }
    
    animateValue(element, start, end) {
        const duration = 1000;
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }
    
    animateNewData() {
        // Pulso visual no indicador de conexão
        const indicator = document.getElementById('realtime-indicator');
        if (indicator) {
            indicator.classList.add('pulse');
            setTimeout(() => {
                indicator.classList.remove('pulse');
            }, 500);
        }
    }
    
    updateConnectionStatus(connected) {
        const indicator = document.getElementById('connection-status');
        if (indicator) {
            indicator.className = connected ? 'connected' : 'disconnected';
            indicator.textContent = connected ? 'ONLINE' : 'OFFLINE';
        }
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            
            console.log(`🔄 Tentativa de reconexão ${this.reconnectAttempts}/${this.maxReconnectAttempts} em ${delay}ms`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            console.error('❌ Máximo de tentativas de reconexão atingido');
            this.updateConnectionStatus(false);
        }
    }
    
    send(data) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(data));
        }
    }
    
    setupEventListeners() {
        // Reconectar quando a página voltar ao foco
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && !this.isConnected) {
                this.connect();
            }
        });
        
        // Reconectar quando a conexão de rede voltar
        window.addEventListener('online', () => {
            if (!this.isConnected) {
                this.connect();
            }
        });
    }
    
    getAlertIcon(tipo) {
        const icons = {
            'TEMP_ALTA': '🌡️',
            'RPM_ALTA': '⚡',
            'VALOR_FORA': '⚠️',
            'DESCONECTADO': '📡',
            'CRITICO': '🚨'
        };
        return icons[tipo] || '⚠️';
    }
    
    playAlertSound() {
        // Som de alerta opcional
        try {
            const audio = new Audio('/static/sounds/alert.mp3');
            audio.volume = 0.3;
            audio.play().catch(() => {
                // Ignorar erro se som não puder ser reproduzido
            });
        } catch (error) {
            // Ignorar erro de áudio
        }
    }
    
    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.motosenseRealtime = new MotosenseRealtime();
});

// Limpar conexão ao sair da página
window.addEventListener('beforeunload', () => {
    if (window.motosenseRealtime) {
        window.motosenseRealtime.disconnect();
    }
});