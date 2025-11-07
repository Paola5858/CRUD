/**
 * ═══════════════════════════════════════════════════════════════
 * MOTOSENSE CRUD - ULTRA-ADVANCED DATA TABLE
 * Interactive Motor Management with Biker Aesthetic
 * ═══════════════════════════════════════════════════════════════
 */

// ━━━ SAMPLE DATA - RICH MOTOR RECORDS ━━━
const SAMPLE_MOTORS = [
    {
        id: 'M-001',
        name: 'MOTOR TURBO A1',
        serial: 'TRB-2024-A1-X',
        type: 'RACING',
        power: 3000,
        temp: 94,
        rpm: 4850,
        status: 'ONLINE',
        lastSeen: 'Há 30s',
        created: '01/11/2025 08:30',
        description: 'Motor de alta performance para aplicações racing',
        selected: false,
        expanded: false
    },
    {
        id: 'M-002',
        name: 'MOTOR INDUSTRIAL B2',
        serial: 'IND-2024-B2-Y',
        type: 'INDUSTRIAL',
        power: 2200,
        temp: 78,
        rpm: 3200,
        status: 'ONLINE',
        lastSeen: 'Há 1 min',
        created: '02/11/2025 10:15',
        description: 'Motor industrial para uso pesado',
        selected: false,
        expanded: false
    },
    {
        id: 'M-003',
        name: 'MOTOR FLEX C3',
        serial: 'FLX-2024-C3-Z',
        type: 'COMERCIAL',
        power: 1800,
        temp: null,
        rpm: null,
        status: 'OFFLINE',
        lastSeen: 'Há 3h',
        created: '03/11/2025 14:22',
        description: 'Motor comercial flexível',
        selected: false,
        expanded: false
    },
    {
        id: 'M-004',
        name: 'MOTOR ULTRA D4',
        serial: 'ULT-2024-D4-W',
        type: 'INDUSTRIAL',
        power: 2800,
        temp: 98,
        rpm: 4100,
        status: 'ONLINE',
        lastSeen: 'Há 15s',
        created: '04/11/2025 09:45',
        description: 'Motor ultra potente com sistema de resfriamento',
        selected: false,
        expanded: false,
        critical: true
    },
    {
        id: 'M-005',
        name: 'MOTOR ECO E5',
        serial: 'ECO-2024-E5-V',
        type: 'RESIDENCIAL',
        power: 1200,
        temp: 65,
        rpm: 2800,
        status: 'ONLINE',
        lastSeen: 'Há 45s',
        created: '05/11/2025 16:20',
        description: 'Motor econômico para uso residencial',
        selected: false,
        expanded: false
    },
    {
        id: 'M-006',
        name: 'MOTOR POWER F6',
        serial: 'PWR-2024-F6-U',
        type: 'COMERCIAL',
        power: 2500,
        temp: 82,
        rpm: 3600,
        status: 'MANUTENÇÃO',
        lastSeen: 'Há 2h',
        created: '06/11/2025 11:30',
        description: 'Motor de potência para aplicações comerciais',
        selected: false,
        expanded: false
    },
    {
        id: 'M-007',
        name: 'MOTOR SPEED G7',
        serial: 'SPD-2024-G7-T',
        type: 'RACING',
        power: 3500,
        temp: 89,
        rpm: 5200,
        status: 'ONLINE',
        lastSeen: 'Há 10s',
        created: '07/11/2025 13:15',
        description: 'Motor de velocidade extrema',
        selected: false,
        expanded: false
    },
    {
        id: 'M-008',
        name: 'MOTOR BASIC H8',
        serial: 'BSC-2024-H8-S',
        type: 'RESIDENCIAL',
        power: 800,
        temp: 55,
        rpm: 2200,
        status: 'ONLINE',
        lastSeen: 'Há 2 min',
        created: '08/11/2025 15:45',
        description: 'Motor básico para uso doméstico',
        selected: false,
        expanded: false
    },
    {
        id: 'M-009',
        name: 'MOTOR HEAVY I9',
        serial: 'HVY-2024-I9-R',
        type: 'INDUSTRIAL',
        power: 4000,
        temp: 91,
        rpm: 3800,
        status: 'ONLINE',
        lastSeen: 'Há 20s',
        created: '09/11/2025 07:30',
        description: 'Motor pesado para indústria',
        selected: false,
        expanded: false
    },
    {
        id: 'M-010',
        name: 'MOTOR SMART J10',
        serial: 'SMT-2024-J10-Q',
        type: 'COMERCIAL',
        power: 1600,
        temp: 72,
        rpm: 3000,
        status: 'ERRO',
        lastSeen: 'Há 5 min',
        created: '10/11/2025 12:00',
        description: 'Motor inteligente com IoT',
        selected: false,
        expanded: false
    },
    {
        id: 'M-011',
        name: 'MOTOR TURBO K11',
        serial: 'TRB-2024-K11-P',
        type: 'RACING',
        power: 3200,
        temp: 86,
        rpm: 4600,
        status: 'ONLINE',
        lastSeen: 'Há 1 min',
        created: '11/11/2025 14:30',
        description: 'Motor turbo de segunda geração',
        selected: false,
        expanded: false
    },
    {
        id: 'M-012',
        name: 'MOTOR SILENT L12',
        serial: 'SLT-2024-L12-O',
        type: 'RESIDENCIAL',
        power: 1000,
        temp: 60,
        rpm: 2500,
        status: 'STANDBY',
        lastSeen: 'Há 10 min',
        created: '12/11/2025 16:45',
        description: 'Motor silencioso para ambientes residenciais',
        selected: false,
        expanded: false
    }
];

// ━━━ GLOBAL STATE ━━━
let currentMotors = window.MOTORES_BACKEND && window.MOTORES_BACKEND.length > 0 ? [...window.MOTORES_BACKEND] : [...SAMPLE_MOTORS];
let selectedMotors = [];
let sortColumn = 'name';
let sortDirection = 'asc';
let currentPage = 1;
let rowsPerPage = 25;
let searchQuery = '';
let activeFilters = ['INDUSTRIAL', 'ONLINE', '> 2000W', 'ALTA TEMP', 'NOVOS'];

// ━━━ UTILITY FUNCTIONS ━━━
function formatPower(power) {
    if (!power) return '--';
    return `${power.toLocaleString('pt-BR')} W`;
}

function formatTemperature(temp) {
    if (temp === null || temp === undefined) return '--°C';
    return `${temp}°C`;
}

function formatRPM(rpm) {
    if (!rpm) return '--';
    return rpm.toLocaleString('pt-BR');
}

function getTemperatureColor(temp) {
    if (!temp) return '#666666';
    if (temp < 70) return '#00d9ff';
    if (temp < 80) return '#00ff41';
    if (temp < 90) return '#ffaa00';
    if (temp < 95) return '#ff8c00';
    return '#ff3333';
}

function getStatusConfig(status) {
    const configs = {
        'ONLINE': {
            color: '#00ff41',
            bg: 'rgba(0, 255, 65, 0.12)',
            border: 'rgba(0, 255, 65, 0.3)',
            icon: '●',
            pulse: true
        },
        'OFFLINE': {
            color: '#ff3333',
            bg: 'rgba(255, 51, 51, 0.12)',
            border: 'rgba(255, 51, 51, 0.3)',
            icon: '●',
            pulse: false
        },
        'MANUTENÇÃO': {
            color: '#ffaa00',
            bg: 'rgba(255, 170, 0, 0.12)',
            border: 'rgba(255, 170, 0, 0.3)',
            icon: '🔧',
            pulse: false
        },
        'ERRO': {
            color: '#ff3333',
            bg: 'rgba(255, 51, 51, 0.12)',
            border: 'rgba(255, 51, 51, 0.3)',
            icon: '⚠️',
            pulse: true
        },
        'STANDBY': {
            color: '#666666',
            bg: 'rgba(102, 102, 102, 0.12)',
            border: 'rgba(102, 102, 102, 0.3)',
            icon: '⏸️',
            pulse: false
        }
    };
    return configs[status] || configs['OFFLINE'];
}

function getTypeConfig(type) {
    const configs = {
        'INDUSTRIAL': {
            color: '#3b82f6',
            bg: 'rgba(59, 130, 246, 0.15)',
            border: 'rgba(59, 130, 246, 0.4)'
        },
        'RESIDENCIAL': {
            color: '#22c55e',
            bg: 'rgba(34, 197, 94, 0.15)',
            border: 'rgba(34, 197, 94, 0.4)'
        },
        'COMERCIAL': {
            color: '#a855f7',
            bg: 'rgba(168, 85, 247, 0.15)',
            border: 'rgba(168, 85, 247, 0.4)'
        },
        'RACING': {
            color: '#000000',
            bg: 'linear-gradient(135deg, #ff6b00, #ff8c00)',
            border: '#ffaa00',
            special: true
        }
    };
    return configs[type] || configs['INDUSTRIAL'];
}

// ━━━ TABLE RENDERING ━━━
function renderTableRow(motor, index) {
    const statusConfig = getStatusConfig(motor.status);
    const typeConfig = getTypeConfig(motor.type);
    const tempColor = getTemperatureColor(motor.temp);
    
    const isSelected = selectedMotors.includes(motor.id);
    const rowClass = `table-row ${isSelected ? 'selected' : ''} ${motor.status === 'OFFLINE' ? 'dimmed' : ''}`;
    
    return `
        <div class="${rowClass}" data-motor-id="${motor.id}" onclick="toggleRowSelection('${motor.id}')">
            <!-- Checkbox -->
            <div class="row-cell checkbox-col">
                <input type="checkbox" class="row-checkbox" ${isSelected ? 'checked' : ''} 
                       onchange="handleRowCheckbox('${motor.id}', this.checked)">
            </div>
            
            <!-- ID + Drag Handle -->
            <div class="row-cell id-col">
                <span class="drag-handle" draggable="true">⠿</span>
                <span class="motor-id">${motor.id}</span>
            </div>
            
            <!-- Motor Info -->
            <div class="row-cell motor-col">
                <div class="motor-avatar">
                    <span class="motor-icon">🏍️</span>
                </div>
                <div class="motor-info">
                    <div class="motor-name">${motor.name}</div>
                    <div class="motor-serial">SN: ${motor.serial}</div>
                    ${motor.type === 'RACING' ? '<div class="motor-tag">PREMIUM</div>' : ''}
                </div>
            </div>
            
            <!-- Type Badge -->
            <div class="row-cell type-col">
                <div class="type-badge ${motor.type.toLowerCase()}" 
                     style="background: ${typeConfig.bg}; border-color: ${typeConfig.border}; color: ${typeConfig.color};">
                    <span class="type-dot"></span>
                    <span class="type-text">${motor.type}</span>
                </div>
            </div>
            
            <!-- Power -->
            <div class="row-cell power-col">
                <div class="power-display">
                    <span class="power-value">${motor.power || '--'}</span>
                    <span class="power-unit">W</span>
                </div>
                <div class="power-bar">
                    <div class="power-fill" style="width: ${motor.power ? (motor.power / 4000) * 100 : 0}%"></div>
                </div>
            </div>
            
            <!-- Temperature -->
            <div class="row-cell temp-col">
                <span class="temp-icon" style="color: ${tempColor}">🌡️</span>
                <span class="temp-value" style="color: ${tempColor}">${formatTemperature(motor.temp)}</span>
                ${motor.critical ? '<span class="temp-warning">⚠️</span>' : ''}
            </div>
            
            <!-- RPM -->
            <div class="row-cell rpm-col">
                <div class="rpm-display">
                    <span class="rpm-value">${formatRPM(motor.rpm)}</span>
                    <span class="rpm-unit">RPM</span>
                </div>
                ${motor.status === 'ONLINE' ? '<div class="rpm-indicator pulsing"></div>' : ''}
                <div class="mini-sparkline"></div>
            </div>
            
            <!-- Status -->
            <div class="row-cell status-col">
                <div class="status-badge ${motor.status.toLowerCase()}" 
                     style="background: ${statusConfig.bg}; border-color: ${statusConfig.border};">
                    <span class="status-icon ${statusConfig.pulse ? 'pulsing' : ''}" 
                          style="color: ${statusConfig.color}">${statusConfig.icon}</span>
                    <div class="status-info">
                        <div class="status-text" style="color: ${statusConfig.color}">${motor.status}</div>
                        <div class="status-time">${motor.lastSeen}</div>
                    </div>
                </div>
            </div>
            
            <!-- Created Date -->
            <div class="row-cell date-col">
                <span class="date-icon">📅</span>
                <div class="date-info">
                    <div class="date-value">${motor.created.split(' ')[0]}</div>
                    <div class="time-value">${motor.created.split(' ')[1]}</div>
                </div>
            </div>
            
            <!-- Actions -->
            <div class="row-cell actions-col">
                <div class="action-buttons">
                    <button class="action-btn view" onclick="viewMotor('${motor.id}')" title="Ver detalhes">
                        <span class="btn-icon">👁️</span>
                    </button>
                    <button class="action-btn edit" onclick="editMotor('${motor.id}')" title="Editar motor">
                        <span class="btn-icon">✏️</span>
                    </button>
                    <button class="action-btn chart" onclick="showCharts('${motor.id}')" title="Ver métricas">
                        <span class="btn-icon">📊</span>
                    </button>
                    <button class="action-btn link" onclick="linkSensor('${motor.id}')" title="Vincular sensor">
                        <span class="btn-icon">🔗</span>
                    </button>
                    <button class="action-btn delete" onclick="deleteMotor('${motor.id}')" title="Deletar motor">
                        <span class="btn-icon">🗑️</span>
                    </button>
                </div>
            </div>
        </div>
        
        ${motor.expanded ? renderExpandedRow(motor) : ''}
    `;
}

function renderExpandedRow(motor) {
    return `
        <div class="expanded-row" data-motor-id="${motor.id}">
            <div class="expanded-content">
                <div class="expanded-col sensors">
                    <h4 class="expanded-title">SENSORES VINCULADOS</h4>
                    <div class="sensor-list">
                        <div class="sensor-item">
                            <span class="sensor-icon">🌡️</span>
                            <span class="sensor-type">Temperatura:</span>
                            <span class="sensor-value">${formatTemperature(motor.temp)}</span>
                        </div>
                        <div class="sensor-item">
                            <span class="sensor-icon">⚡</span>
                            <span class="sensor-type">Potência:</span>
                            <span class="sensor-value">${formatPower(motor.power)}</span>
                        </div>
                        <div class="sensor-item">
                            <span class="sensor-icon">🔄</span>
                            <span class="sensor-type">RPM:</span>
                            <span class="sensor-value">${formatRPM(motor.rpm)}</span>
                        </div>
                    </div>
                </div>
                
                <div class="expanded-col charts">
                    <h4 class="expanded-title">MINI GRÁFICOS</h4>
                    <div class="mini-chart rpm-chart">
                        <div class="chart-title">RPM (Última Hora)</div>
                        <div class="chart-placeholder">📈</div>
                    </div>
                    <div class="mini-chart power-chart">
                        <div class="chart-title">Consumo de Energia</div>
                        <div class="chart-placeholder">📊</div>
                    </div>
                </div>
                
                <div class="expanded-col actions">
                    <h4 class="expanded-title">AÇÕES RÁPIDAS</h4>
                    <div class="quick-actions">
                        <button class="quick-action-btn">
                            <span class="btn-icon">⚙️</span>
                            <span class="btn-text">Configurar</span>
                        </button>
                        <button class="quick-action-btn">
                            <span class="btn-icon">📊</span>
                            <span class="btn-text">Relatório</span>
                        </button>
                        <button class="quick-action-btn">
                            <span class="btn-icon">🔧</span>
                            <span class="btn-text">Manutenção</span>
                        </button>
                        <button class="quick-action-btn">
                            <span class="btn-icon">📜</span>
                            <span class="btn-text">Histórico</span>
                        </button>
                    </div>
                </div>
            </div>
            
            <button class="collapse-btn" onclick="collapseRow('${motor.id}')">
                <span class="btn-icon">△</span>
                <span class="btn-text">FECHAR</span>
            </button>
        </div>
    `;
}

function renderTable() {
    const tableBody = document.getElementById('tableBody');
    if (!tableBody) return;
    
    // Apply filters and search
    let filteredMotors = currentMotors.filter(motor => {
        // Search filter
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            const searchableText = `${motor.name} ${motor.serial} ${motor.type} ${motor.power} ${motor.status}`.toLowerCase();
            if (!searchableText.includes(query)) return false;
        }
        
        // Additional filters can be applied here
        return true;
    });
    
    // Sort motors
    filteredMotors.sort((a, b) => {
        let aVal = a[sortColumn];
        let bVal = b[sortColumn];
        
        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
        }
        
        if (sortDirection === 'asc') {
            return aVal > bVal ? 1 : -1;
        } else {
            return aVal < bVal ? 1 : -1;
        }
    });
    
    // Pagination
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const paginatedMotors = filteredMotors.slice(startIndex, endIndex);
    
    // Render rows
    tableBody.innerHTML = paginatedMotors.map((motor, index) => renderTableRow(motor, index)).join('');
    
    // Update pagination info
    updatePaginationInfo(filteredMotors.length);
    
    // Update bulk actions visibility
    updateBulkActionsVisibility();
}

// ━━━ EVENT HANDLERS ━━━
function handleRowCheckbox(motorId, checked) {
    if (checked) {
        if (!selectedMotors.includes(motorId)) {
            selectedMotors.push(motorId);
        }
    } else {
        selectedMotors = selectedMotors.filter(id => id !== motorId);
    }
    
    updateBulkActionsVisibility();
    updateHeaderCheckbox();
}

function toggleRowSelection(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (!motor) return;
    
    motor.selected = !motor.selected;
    
    if (motor.selected) {
        if (!selectedMotors.includes(motorId)) {
            selectedMotors.push(motorId);
        }
    } else {
        selectedMotors = selectedMotors.filter(id => id !== motorId);
    }
    
    renderTable();
}

function updateBulkActionsVisibility() {
    const bulkActionsBar = document.getElementById('bulkActionsBar');
    const bulkActions = document.getElementById('bulkActions');
    
    if (selectedMotors.length > 0) {
        if (bulkActionsBar) {
            bulkActionsBar.style.display = 'flex';
            const countElement = bulkActionsBar.querySelector('.bulk-count');
            if (countElement) {
                countElement.textContent = `${selectedMotors.length} MOTORES SELECIONADOS`;
            }
        }
        if (bulkActions) {
            bulkActions.style.display = 'flex';
        }
    } else {
        if (bulkActionsBar) bulkActionsBar.style.display = 'none';
        if (bulkActions) bulkActions.style.display = 'none';
    }
}

function updateHeaderCheckbox() {
    const headerCheckbox = document.getElementById('headerCheckbox');
    if (!headerCheckbox) return;
    
    const visibleMotors = currentMotors.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage);
    const visibleSelected = visibleMotors.filter(motor => selectedMotors.includes(motor.id));
    
    if (visibleSelected.length === 0) {
        headerCheckbox.checked = false;
        headerCheckbox.indeterminate = false;
    } else if (visibleSelected.length === visibleMotors.length) {
        headerCheckbox.checked = true;
        headerCheckbox.indeterminate = false;
    } else {
        headerCheckbox.checked = false;
        headerCheckbox.indeterminate = true;
    }
}

function updatePaginationInfo(totalItems) {
    const totalPages = Math.ceil(totalItems / rowsPerPage);
    const startItem = (currentPage - 1) * rowsPerPage + 1;
    const endItem = Math.min(currentPage * rowsPerPage, totalItems);
    
    // Update footer info
    const totalInfo = document.querySelector('.total-text');
    if (totalInfo) {
        totalInfo.textContent = `Mostrando ${startItem}-${endItem} de ${totalItems} motores`;
    }
    
    const pageInfo = document.querySelector('.page-text');
    if (pageInfo) {
        pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
    }
    
    // Update pagination buttons
    updatePaginationButtons(totalPages);
}

function updatePaginationButtons(totalPages) {
    const pageNumbers = document.querySelector('.page-numbers');
    if (!pageNumbers) return;
    
    let paginationHTML = '';
    
    // Always show first page
    paginationHTML += `<button class="page-number ${currentPage === 1 ? 'active' : ''}" onclick="goToPage(1)">1</button>`;
    
    if (totalPages > 1) {
        if (currentPage > 3) {
            paginationHTML += '<span class="page-ellipsis">...</span>';
        }
        
        // Show pages around current page
        for (let i = Math.max(2, currentPage - 1); i <= Math.min(totalPages - 1, currentPage + 1); i++) {
            paginationHTML += `<button class="page-number ${currentPage === i ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
        }
        
        if (currentPage < totalPages - 2) {
            paginationHTML += '<span class="page-ellipsis">...</span>';
        }
        
        // Always show last page
        if (totalPages > 1) {
            paginationHTML += `<button class="page-number ${currentPage === totalPages ? 'active' : ''}" onclick="goToPage(${totalPages})">${totalPages}</button>`;
        }
    }
    
    pageNumbers.innerHTML = paginationHTML;
}

// ━━━ ACTION FUNCTIONS ━━━
function viewMotor(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (!motor) return;
    
    console.log('Viewing motor:', motor);
    // Implement view modal or navigation
}

function editMotor(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (!motor) return;
    
    console.log('Editing motor:', motor);
    // Implement edit functionality
}

function showCharts(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (!motor) return;
    
    console.log('Showing charts for motor:', motor);
    // Implement charts modal
}

function linkSensor(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (!motor) return;
    
    console.log('Linking sensor to motor:', motor);
    // Implement sensor linking
}

function deleteMotor(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (!motor) return;
    
    if (confirm(`Tem certeza que deseja deletar o motor ${motor.name}?`)) {
        currentMotors = currentMotors.filter(m => m.id !== motorId);
        selectedMotors = selectedMotors.filter(id => id !== motorId);
        renderTable();
        console.log('Motor deleted:', motorId);
    }
}

function expandRow(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (motor) {
        motor.expanded = true;
        renderTable();
    }
}

function collapseRow(motorId) {
    const motor = currentMotors.find(m => m.id === motorId);
    if (motor) {
        motor.expanded = false;
        renderTable();
    }
}

function goToPage(page) {
    currentPage = page;
    renderTable();
}

// ━━━ MODAL FUNCTIONS ━━━
function showNewMotorModal() {
    const modal = document.getElementById('modalOverlay');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function hideNewMotorModal() {
    const modal = document.getElementById('modalOverlay');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function handleNewMotorSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const newMotor = {
        id: `M-${String(currentMotors.length + 1).padStart(3, '0')}`,
        name: formData.get('nome'),
        serial: `${formData.get('tipo').substring(0, 3).toUpperCase()}-2025-${String(currentMotors.length + 1).padStart(2, '0')}-A`,
        type: formData.get('tipo'),
        power: parseInt(formData.get('potencia')),
        temp: Math.floor(Math.random() * 40 + 60), // Random temp 60-100
        rpm: Math.floor(Math.random() * 2000 + 2000), // Random RPM 2000-4000
        status: 'ONLINE',
        lastSeen: 'Há poucos segundos',
        created: new Date().toLocaleDateString('pt-BR') + ' ' + new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
        description: formData.get('descricao') || 'Motor criado via interface',
        selected: false,
        expanded: false
    };
    
    currentMotors.unshift(newMotor); // Add to beginning
    renderTable();
    hideNewMotorModal();
    
    // Reset form
    event.target.reset();
    
    console.log('New motor created:', newMotor);
}

// ━━━ SEARCH AND FILTER FUNCTIONS ━━━
function handleSearch(query) {
    searchQuery = query;
    currentPage = 1; // Reset to first page
    renderTable();
}

function removeFilter(filterText) {
    activeFilters = activeFilters.filter(f => f !== filterText);
    renderFilters();
    renderTable();
}

function renderFilters() {
    const filtersContainer = document.querySelector('.quick-filters');
    if (!filtersContainer) return;
    
    filtersContainer.innerHTML = activeFilters.map(filter => `
        <div class="filter-tag active">
            <span>${filter}</span>
            <button class="remove-filter" onclick="removeFilter('${filter}')">✕</button>
        </div>
    `).join('');
}

// ━━━ INITIALIZATION ━━━
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏍️ MOTOSENSE CRUD Initializing...');
    
    // Initial render
    renderTable();
    renderFilters();
    
    // Event listeners
    const btnNovoMotor = document.getElementById('btnNovoMotor');
    if (btnNovoMotor) {
        btnNovoMotor.addEventListener('click', showNewMotorModal);
    }
    
    const modalClose = document.getElementById('modalClose');
    if (modalClose) {
        modalClose.addEventListener('click', hideNewMotorModal);
    }
    
    const btnCancel = document.getElementById('btnCancel');
    if (btnCancel) {
        btnCancel.addEventListener('click', hideNewMotorModal);
    }
    
    const motorForm = document.getElementById('motorForm');
    if (motorForm) {
        motorForm.addEventListener('submit', handleNewMotorSubmit);
    }
    
    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            handleSearch(e.target.value);
        });
    }
    
    // Header checkbox
    const headerCheckbox = document.getElementById('headerCheckbox');
    if (headerCheckbox) {
        headerCheckbox.addEventListener('change', (e) => {
            const visibleMotors = currentMotors.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage);
            
            if (e.target.checked) {
                visibleMotors.forEach(motor => {
                    if (!selectedMotors.includes(motor.id)) {
                        selectedMotors.push(motor.id);
                    }
                });
            } else {
                visibleMotors.forEach(motor => {
                    selectedMotors = selectedMotors.filter(id => id !== motor.id);
                });
            }
            
            renderTable();
        });
    }
    
    // View toggle buttons
    const viewBtns = document.querySelectorAll('.view-btn');
    viewBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            viewBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
    
    // Density toggle buttons
    const densityBtns = document.querySelectorAll('.density-btn');
    densityBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            densityBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
    
    // Close modal on overlay click
    const modalOverlay = document.getElementById('modalOverlay');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                hideNewMotorModal();
            }
        });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            hideNewMotorModal();
        }
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            showNewMotorModal();
        }
    });
    
    // Sidebar toggle functionality
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            
            // Save state to localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
        });
        
        // Restore sidebar state from localStorage
        const savedState = localStorage.getItem('sidebarCollapsed');
        if (savedState === 'true') {
            sidebar.classList.add('collapsed');
        }
    }
    
    console.log('🔥 MOTOSENSE CRUD Ready!');
});

// ━━━ EXPORT FOR GLOBAL ACCESS ━━━
window.MOTOSENSE_CRUD = {
    currentMotors,
    selectedMotors,
    renderTable,
    showNewMotorModal,
    hideNewMotorModal,
    viewMotor,
    editMotor,
    deleteMotor,
    expandRow,
    collapseRow
};

/**
 * ═══════════════════════════════════════════════════════════════
 * END OF MOTOSENSE CRUD JAVASCRIPT
 * ═══════════════════════════════════════════════════════════════
 */