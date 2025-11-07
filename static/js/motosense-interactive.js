/**
 * MOTOSENSE - Sistema Interativo Completo
 * Feedback visual, animações e funcionalidades reais
 */

// ━━━ ESTADO GLOBAL ━━━
const MOTOSENSE = {
    data: {
        motors: [],
        selectedIds: [],
        currentView: 'table',
        searchQuery: '',
        sortColumn: 'name',
        sortDirection: 'asc'
    },
    
    // ━━━ INICIALIZAÇÃO ━━━
    init() {
        console.log('🏍️ MOTOSENSE Interactive Loading...');
        
        // Carregar dados do backend ou fallback
        this.loadData();
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Renderizar interface inicial
        this.render();
        
        console.log('✅ MOTOSENSE Interactive Ready!');
    },
    
    // ━━━ CARREGAMENTO DE DADOS ━━━
    loadData() {
        // Usar dados do backend se disponíveis
        if (window.MOTORES_BACKEND && window.MOTORES_BACKEND.length > 0) {
            this.data.motors = [...window.MOTORES_BACKEND];
        } else {
            // Fallback com dados simulados
            this.data.motors = this.generateFallbackData();
        }
    },
    
    generateFallbackData() {
        const types = ['INDUSTRIAL', 'COMERCIAL', 'RESIDENCIAL', 'RACING'];
        const statuses = ['ONLINE', 'OFFLINE', 'MANUTENÇÃO', 'ERRO'];
        
        return Array.from({length: 12}, (_, i) => ({
            id: `M-${String(i + 1).padStart(3, '0')}`,
            name: `Motor ${String.fromCharCode(65 + i)}${i + 1}`,
            type: types[i % types.length],
            power: Math.floor(Math.random() * 3000) + 1000,
            temp: Math.floor(Math.random() * 40) + 60,
            rpm: Math.floor(Math.random() * 2000) + 2000,
            status: statuses[i % statuses.length],
            created: new Date(2025, 0, i + 1).toLocaleDateString('pt-BR'),
            selected: false,
            expanded: false
        }));
    },
    
    // ━━━ EVENT LISTENERS ━━━
    setupEventListeners() {
        // Botões principais
        this.bindClick('btnNovoMotor', () => this.showModal('motorModal'));
        this.bindClick('btnImportar', () => this.showNotification('Função de importação em desenvolvimento', 'info'));
        this.bindClick('btnExportar', () => this.exportData());
        
        // Modal
        this.bindClick('modalClose', () => this.hideModal());
        this.bindClick('btnCancel', () => this.hideModal());
        
        // Busca
        this.bindInput('searchInput', (value) => this.handleSearch(value));
        
        // View toggles
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchView(e.target.dataset.view));
        });
        
        // Density toggles
        document.querySelectorAll('.density-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchDensity(e.target.textContent.toLowerCase()));
        });
        
        // Filter tags
        document.querySelectorAll('.filter-tag .remove-filter').forEach(btn => {
            btn.addEventListener('click', (e) => this.removeFilter(e.target.closest('.filter-tag')));
        });
        
        // Sidebar toggle
        this.bindClick('sidebarToggle', () => this.toggleSidebar());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // Modal overlay click
        this.bindClick('modalOverlay', (e) => {
            if (e.target.id === 'modalOverlay') this.hideModal();
        });
    },
    
    // ━━━ UTILITÁRIOS DE BINDING ━━━
    bindClick(id, handler) {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('click', handler);
        }
    },
    
    bindInput(id, handler) {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', (e) => handler(e.target.value));
        }
    },
    
    // ━━━ RENDERIZAÇÃO ━━━
    render() {
        this.renderTable();
        this.updateStats();
        this.updateBulkActions();
    },
    
    renderTable() {
        const tableBody = document.getElementById('tableBody');
        if (!tableBody) return;
        
        const filteredMotors = this.getFilteredMotors();
        
        if (filteredMotors.length === 0) {
            tableBody.innerHTML = this.renderEmptyState();
            return;
        }
        
        tableBody.innerHTML = filteredMotors.map(motor => this.renderMotorRow(motor)).join('');
        
        // Aplicar animações de entrada
        this.animateTableRows();
    },
    
    renderMotorRow(motor) {
        const statusConfig = this.getStatusConfig(motor.status);
        const isSelected = this.data.selectedIds.includes(motor.id);
        
        return `
            <div class=\"table-row ${isSelected ? 'selected' : ''} ${motor.status === 'OFFLINE' ? 'dimmed' : ''}\" 
                 data-motor-id=\"${motor.id}\">
                
                <div class=\"row-cell checkbox-col\">
                    <input type=\"checkbox\" class=\"row-checkbox\" ${isSelected ? 'checked' : ''} 
                           onchange=\"MOTOSENSE.toggleSelection('${motor.id}', this.checked)\">
                </div>
                
                <div class=\"row-cell id-col\">
                    <span class=\"drag-handle\">⠿</span>
                    <span class=\"motor-id\">${motor.id}</span>
                </div>
                
                <div class=\"row-cell motor-col\">
                    <div class=\"motor-info\">
                        <div class=\"motor-name\">${motor.name}</div>
                        <div class=\"motor-type\">${motor.type}</div>
                    </div>
                </div>
                
                <div class=\"row-cell type-col\">
                    <span class=\"type-badge ${motor.type.toLowerCase()}\">${motor.type}</span>
                </div>
                
                <div class=\"row-cell power-col\">
                    <span class=\"power-value\">${motor.power}W</span>
                    <div class=\"power-bar\">
                        <div class=\"power-fill\" style=\"width: ${(motor.power / 4000) * 100}%\"></div>
                    </div>
                </div>
                
                <div class=\"row-cell temp-col\">
                    <span class=\"temp-value\" style=\"color: ${this.getTempColor(motor.temp)}\">${motor.temp}°C</span>
                </div>
                
                <div class=\"row-cell rpm-col\">
                    <span class=\"rpm-value\">${motor.rpm.toLocaleString()}</span>
                </div>
                
                <div class=\"row-cell status-col\">
                    <div class=\"status-badge ${motor.status.toLowerCase()}\" 
                         style=\"background: ${statusConfig.bg}; border-color: ${statusConfig.border};\">
                        <span class=\"status-icon ${statusConfig.pulse ? 'pulsing' : ''}\" 
                              style=\"color: ${statusConfig.color}\">${statusConfig.icon}</span>
                        <span class=\"status-text\">${motor.status}</span>
                    </div>
                </div>
                
                <div class=\"row-cell date-col\">
                    <span class=\"date-value\">${motor.created}</span>
                </div>
                
                <div class=\"row-cell actions-col\">
                    <div class=\"action-buttons\">
                        <button class=\"action-btn view\" onclick=\"MOTOSENSE.viewMotor('${motor.id}')\" title=\"Ver detalhes\">
                            👁️
                        </button>
                        <button class=\"action-btn edit\" onclick=\"MOTOSENSE.editMotor('${motor.id}')\" title=\"Editar\">
                            ✏️
                        </button>
                        <button class=\"action-btn delete\" onclick=\"MOTOSENSE.deleteMotor('${motor.id}')\" title=\"Deletar\">
                            🗑️
                        </button>
                    </div>
                </div>
            </div>
        `;
    },
    
    renderEmptyState() {
        return `
            <div class=\"empty-state\">
                <div class=\"empty-icon\">🏍️</div>
                <div class=\"empty-title\">Nenhum motor encontrado</div>
                <div class=\"empty-subtitle\">Tente ajustar os filtros ou adicionar um novo motor</div>
                <button class=\"btn-primary\" onclick=\"MOTOSENSE.showModal('motorModal')\">
                    ➕ Adicionar Motor
                </button>
            </div>
        `;
    },
    
    // ━━━ INTERAÇÕES ━━━
    toggleSelection(motorId, checked) {
        if (checked) {
            if (!this.data.selectedIds.includes(motorId)) {
                this.data.selectedIds.push(motorId);
            }
        } else {
            this.data.selectedIds = this.data.selectedIds.filter(id => id !== motorId);
        }
        
        this.updateBulkActions();
        this.animateSelection(motorId);
    },
    
    switchView(view) {
        if (!view) return;
        
        this.data.currentView = view;
        
        // Atualizar botões
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === view);
        });
        
        // Aplicar feedback visual
        this.showNotification(`Visualização alterada para ${view.toUpperCase()}`, 'info', 2000);
        
        // Re-renderizar se necessário
        if (view === 'table') {
            this.render();
        }
    },
    
    switchDensity(density) {
        document.querySelectorAll('.density-btn').forEach(btn => {
            btn.classList.toggle('active', btn.textContent.toLowerCase() === density);
        });
        
        // Aplicar classe de densidade
        const tableCard = document.querySelector('.table-card');
        if (tableCard) {
            tableCard.className = `table-card density-${density}`;
        }
        
        this.showNotification(`Densidade alterada para ${density}`, 'info', 2000);
    },
    
    removeFilter(filterElement) {
        // Animação de remoção
        filterElement.style.transform = 'scale(0.8)';
        filterElement.style.opacity = '0.5';
        
        setTimeout(() => {
            filterElement.remove();
            this.render();
            this.showNotification('Filtro removido', 'info', 2000);
        }, 200);
    },
    
    handleSearch(query) {
        this.data.searchQuery = query.toLowerCase();
        this.render();
        
        // Feedback visual na busca
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.style.borderColor = query ? '#ff6b00' : '';
        }
    },
    
    // ━━━ AÇÕES DOS MOTORES ━━━
    viewMotor(motorId) {
        const motor = this.data.motors.find(m => m.id === motorId);
        if (!motor) return;
        
        this.showNotification(`Visualizando motor ${motor.name}`, 'info');
        console.log('Viewing motor:', motor);
    },
    
    editMotor(motorId) {
        const motor = this.data.motors.find(m => m.id === motorId);
        if (!motor) return;
        
        this.showNotification(`Editando motor ${motor.name}`, 'info');
        console.log('Editing motor:', motor);
    },
    
    deleteMotor(motorId) {
        const motor = this.data.motors.find(m => m.id === motorId);
        if (!motor) return;
        
        if (confirm(`Tem certeza que deseja deletar o motor ${motor.name}?`)) {\n            // Animação de remoção\n            const row = document.querySelector(`[data-motor-id=\"${motorId}\"]`);\n            if (row) {\n                row.style.transform = 'translateX(-100%)';\n                row.style.opacity = '0';\n                \n                setTimeout(() => {\n                    this.data.motors = this.data.motors.filter(m => m.id !== motorId);\n                    this.data.selectedIds = this.data.selectedIds.filter(id => id !== motorId);\n                    this.render();\n                    this.showNotification(`Motor ${motor.name} deletado`, 'success');\n                }, 300);\n            }\n        }\n    },\n    \n    exportData() {\n        const data = this.getFilteredMotors();\n        const csv = this.convertToCSV(data);\n        this.downloadCSV(csv, 'motores-motosense.csv');\n        this.showNotification(`${data.length} motores exportados`, 'success');\n    },\n    \n    // ━━━ MODAL ━━━\n    showModal(modalId) {\n        const modal = document.getElementById('modalOverlay');\n        if (modal) {\n            modal.style.display = 'flex';\n            modal.style.opacity = '0';\n            \n            // Animação de entrada\n            requestAnimationFrame(() => {\n                modal.style.opacity = '1';\n                const container = modal.querySelector('.modal-container');\n                if (container) {\n                    container.style.transform = 'scale(1)';\n                }\n            });\n            \n            document.body.style.overflow = 'hidden';\n        }\n    },\n    \n    hideModal() {\n        const modal = document.getElementById('modalOverlay');\n        if (modal) {\n            modal.style.opacity = '0';\n            \n            setTimeout(() => {\n                modal.style.display = 'none';\n                document.body.style.overflow = 'auto';\n            }, 300);\n        }\n    },\n    \n    // ━━━ SIDEBAR ━━━\n    toggleSidebar() {\n        const sidebar = document.querySelector('.sidebar');\n        if (sidebar) {\n            sidebar.classList.toggle('collapsed');\n            \n            // Salvar estado\n            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));\n            \n            // Feedback visual\n            const isCollapsed = sidebar.classList.contains('collapsed');\n            this.showNotification(isCollapsed ? 'Sidebar recolhida' : 'Sidebar expandida', 'info', 2000);\n        }\n    },\n    \n    // ━━━ ANIMAÇÕES ━━━\n    animateTableRows() {\n        const rows = document.querySelectorAll('.table-row');\n        rows.forEach((row, index) => {\n            row.style.opacity = '0';\n            row.style.transform = 'translateY(20px)';\n            \n            setTimeout(() => {\n                row.style.transition = 'all 0.3s ease';\n                row.style.opacity = '1';\n                row.style.transform = 'translateY(0)';\n            }, index * 50);\n        });\n    },\n    \n    animateSelection(motorId) {\n        const row = document.querySelector(`[data-motor-id=\"${motorId}\"]`);\n        if (row) {\n            row.style.transform = 'scale(1.02)';\n            setTimeout(() => {\n                row.style.transform = 'scale(1)';\n            }, 200);\n        }\n    },\n    \n    // ━━━ NOTIFICAÇÕES ━━━\n    showNotification(message, type = 'info', duration = 5000) {\n        if (typeof showNotification === 'function') {\n            showNotification(message, type, duration);\n        } else {\n            console.log(`[${type.toUpperCase()}] ${message}`);\n        }\n    },\n    \n    // ━━━ UTILITÁRIOS ━━━\n    getFilteredMotors() {\n        return this.data.motors.filter(motor => {\n            if (this.data.searchQuery) {\n                const searchText = `${motor.name} ${motor.type} ${motor.status}`.toLowerCase();\n                return searchText.includes(this.data.searchQuery);\n            }\n            return true;\n        });\n    },\n    \n    updateStats() {\n        const total = this.data.motors.length;\n        const online = this.data.motors.filter(m => m.status === 'ONLINE').length;\n        const totalPower = this.data.motors.reduce((sum, m) => sum + m.power, 0);\n        \n        // Atualizar elementos da interface\n        this.updateElement('.stat-value', `${online}/${total}`);\n        this.updateElement('.power-total', `${(totalPower / 1000).toFixed(1)} kW`);\n    },\n    \n    updateBulkActions() {\n        const bulkBar = document.getElementById('bulkActionsBar');\n        const selected = this.data.selectedIds.length;\n        \n        if (bulkBar) {\n            if (selected > 0) {\n                bulkBar.style.display = 'flex';\n                const countElement = bulkBar.querySelector('.bulk-count');\n                if (countElement) {\n                    countElement.textContent = `${selected} MOTORES SELECIONADOS`;\n                }\n            } else {\n                bulkBar.style.display = 'none';\n            }\n        }\n    },\n    \n    updateElement(selector, value) {\n        const element = document.querySelector(selector);\n        if (element) element.textContent = value;\n    },\n    \n    getStatusConfig(status) {\n        const configs = {\n            'ONLINE': { color: '#00ff41', bg: 'rgba(0, 255, 65, 0.12)', border: 'rgba(0, 255, 65, 0.3)', icon: '●', pulse: true },\n            'OFFLINE': { color: '#ff3333', bg: 'rgba(255, 51, 51, 0.12)', border: 'rgba(255, 51, 51, 0.3)', icon: '●', pulse: false },\n            'MANUTENÇÃO': { color: '#ffaa00', bg: 'rgba(255, 170, 0, 0.12)', border: 'rgba(255, 170, 0, 0.3)', icon: '🔧', pulse: false },\n            'ERRO': { color: '#ff3333', bg: 'rgba(255, 51, 51, 0.12)', border: 'rgba(255, 51, 51, 0.3)', icon: '⚠️', pulse: true }\n        };\n        return configs[status] || configs['OFFLINE'];\n    },\n    \n    getTempColor(temp) {\n        if (temp < 70) return '#00d9ff';\n        if (temp < 80) return '#00ff41';\n        if (temp < 90) return '#ffaa00';\n        return '#ff3333';\n    },\n    \n    handleKeyboard(e) {\n        if (e.key === 'Escape') this.hideModal();\n        if (e.ctrlKey && e.key === 'n') {\n            e.preventDefault();\n            this.showModal('motorModal');\n        }\n        if (e.key === 'Delete' && this.data.selectedIds.length > 0) {\n            if (confirm(`Deletar ${this.data.selectedIds.length} motores selecionados?`)) {\n                this.data.selectedIds.forEach(id => this.deleteMotor(id));\n            }\n        }\n    },\n    \n    convertToCSV(data) {\n        const headers = ['ID', 'Nome', 'Tipo', 'Potência', 'Temperatura', 'RPM', 'Status', 'Criado'];\n        const rows = data.map(motor => [\n            motor.id, motor.name, motor.type, motor.power, motor.temp, motor.rpm, motor.status, motor.created\n        ]);\n        \n        return [headers, ...rows].map(row => row.join(',')).join('\\n');\n    },\n    \n    downloadCSV(csv, filename) {\n        const blob = new Blob([csv], { type: 'text/csv' });\n        const url = window.URL.createObjectURL(blob);\n        const a = document.createElement('a');\n        a.href = url;\n        a.download = filename;\n        a.click();\n        window.URL.revokeObjectURL(url);\n    }\n};\n\n// ━━━ INICIALIZAÇÃO AUTOMÁTICA ━━━\ndocument.addEventListener('DOMContentLoaded', () => {\n    MOTOSENSE.init();\n});\n\n// ━━━ EXPORTAR PARA ACESSO GLOBAL ━━━\nwindow.MOTOSENSE = MOTOSENSE;