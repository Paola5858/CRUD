/**
 * ═══════════════════════════════════════════════════════════════
 * MOTOSENSE - BIKER DASHBOARD JAVASCRIPT
 * Ultra-Interactive Racing/Motorcycle Analytics
 * ═══════════════════════════════════════════════════════════════
 */

// ━━━ GLOBAL CONFIGURATION ━━━
const MOTOSENSE_CONFIG = {
    colors: {
        orange: '#ff6b00',
        neonOrange: '#ff8c00',
        amber: '#ffaa00',
        cyan: '#00d9ff',
        neonBlue: '#0099ff',
        activeGreen: '#00ff41',
        errorRed: '#ff3333',
        warningYellow: '#ffcc00',
        offlineGray: '#666666'
    },
    gradients: {
        fire: ['#ff6b00', '#ff8c00', '#ffaa00'],
        hotMetal: ['#ff6b00', '#e85d00'],
        cyan: ['#00d9ff', '#0099ff'],
        green: ['#00ff41', '#00cc35']
    },
    animations: {
        duration: 300,
        easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
    }
};

// ━━━ CHART CONFIGURATIONS ━━━
Chart.defaults.font.family = "'Barlow', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#cccccc';

// ━━━ MAIN CHART - EVOLUTION OVER TIME ━━━
function initMainChart() {
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;

    const gradient1 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
    gradient1.addColorStop(0, 'rgba(255, 107, 0, 0.3)');
    gradient1.addColorStop(1, 'rgba(255, 107, 0, 0)');

    const gradient2 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
    gradient2.addColorStop(0, 'rgba(0, 217, 255, 0.2)');
    gradient2.addColorStop(1, 'rgba(0, 217, 255, 0)');

    const gradient3 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
    gradient3.addColorStop(0, 'rgba(255, 170, 0, 0.2)');
    gradient3.addColorStop(1, 'rgba(255, 170, 0, 0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'],
            datasets: [{
                label: 'Temperatura',
                data: [15, 18, 22, 28, 24, 30, 38, 32, 35, 40, 42, 45],
                borderColor: MOTOSENSE_CONFIG.colors.orange,
                backgroundColor: gradient1,
                borderWidth: 4,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: MOTOSENSE_CONFIG.colors.orange,
                pointBorderColor: '#000000',
                pointBorderWidth: 3,
                pointRadius: 6,
                pointHoverRadius: 10,
                pointHoverBackgroundColor: MOTOSENSE_CONFIG.colors.orange,
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 2
            }, {
                label: 'Pressão',
                data: [12, 15, 18, 24, 20, 25, 32, 28, 30, 35, 38, 40],
                borderColor: MOTOSENSE_CONFIG.colors.cyan,
                backgroundColor: gradient2,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: MOTOSENSE_CONFIG.colors.cyan,
                pointBorderColor: '#000000',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }, {
                label: 'Velocidade',
                data: [10, 13, 16, 22, 18, 23, 30, 26, 28, 33, 36, 38],
                borderColor: MOTOSENSE_CONFIG.colors.amber,
                backgroundColor: gradient3,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: MOTOSENSE_CONFIG.colors.amber,
                pointBorderColor: '#000000',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    titleColor: MOTOSENSE_CONFIG.colors.orange,
                    bodyColor: '#ffffff',
                    borderColor: MOTOSENSE_CONFIG.colors.orange,
                    borderWidth: 2,
                    cornerRadius: 12,
                    displayColors: true,
                    titleFont: {
                        family: "'Teko', sans-serif",
                        size: 16,
                        weight: 700
                    },
                    bodyFont: {
                        family: "'Barlow', sans-serif",
                        size: 13,
                        weight: 600
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#666666',
                        font: {
                            family: "'Barlow', sans-serif",
                            size: 12,
                            weight: 600
                        }
                    }
                },
                y: {
                    grid: {
                        color: '#1a1a1a',
                        lineWidth: 1
                    },
                    ticks: {
                        color: '#666666',
                        font: {
                            family: "'Teko', sans-serif",
                            size: 14,
                            weight: 600
                        }
                    },
                    position: 'right'
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// ━━━ DONUT CHART - SENSOR DISTRIBUTION ━━━
function initDonutChart() {
    const ctx = document.getElementById('donutChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Temperatura', 'Pressão', 'Velocidade'],
            datasets: [{
                data: [35, 25, 40],
                backgroundColor: [
                    MOTOSENSE_CONFIG.colors.orange,
                    MOTOSENSE_CONFIG.colors.cyan,
                    MOTOSENSE_CONFIG.colors.amber
                ],
                borderWidth: 4,
                borderColor: '#000000',
                hoverBorderWidth: 6,
                hoverBorderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    titleColor: MOTOSENSE_CONFIG.colors.orange,
                    bodyColor: '#ffffff',
                    borderColor: MOTOSENSE_CONFIG.colors.orange,
                    borderWidth: 2,
                    cornerRadius: 12,
                    titleFont: {
                        family: "'Teko', sans-serif",
                        size: 16,
                        weight: 700
                    },
                    bodyFont: {
                        family: "'Barlow', sans-serif",
                        size: 13,
                        weight: 600
                    },
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            return `${label}: ${value}%`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 2000,
                easing: 'easeOutBounce'
            },
            onHover: (event, elements) => {
                event.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
            }
        }
    });
}

// ━━━ BAR CHART - WEEKLY PERFORMANCE ━━━
function initBarChart() {
    const ctx = document.getElementById('barChart');
    if (!ctx) return;

    const gradient1 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient1.addColorStop(0, MOTOSENSE_CONFIG.colors.orange);
    gradient1.addColorStop(1, 'rgba(255, 107, 0, 0.3)');

    const gradient2 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient2.addColorStop(0, MOTOSENSE_CONFIG.colors.cyan);
    gradient2.addColorStop(1, 'rgba(0, 217, 255, 0.3)');

    const gradient3 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient3.addColorStop(0, MOTOSENSE_CONFIG.colors.amber);
    gradient3.addColorStop(1, 'rgba(255, 170, 0, 0.3)');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB', 'DOM'],
            datasets: [{
                label: 'Temperatura',
                data: [12000, 15000, 18000, 22000, 35000, 28000, 16000],
                backgroundColor: gradient1,
                borderColor: MOTOSENSE_CONFIG.colors.orange,
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }, {
                label: 'Pressão',
                data: [8000, 12000, 14000, 18000, 28000, 22000, 12000],
                backgroundColor: gradient2,
                borderColor: MOTOSENSE_CONFIG.colors.cyan,
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }, {
                label: 'Velocidade',
                data: [10000, 13000, 16000, 20000, 32000, 25000, 14000],
                backgroundColor: gradient3,
                borderColor: MOTOSENSE_CONFIG.colors.amber,
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    titleColor: MOTOSENSE_CONFIG.colors.orange,
                    bodyColor: '#ffffff',
                    borderColor: MOTOSENSE_CONFIG.colors.orange,
                    borderWidth: 2,
                    cornerRadius: 12,
                    titleFont: {
                        family: "'Teko', sans-serif",
                        size: 16,
                        weight: 700
                    },
                    bodyFont: {
                        family: "'Barlow', sans-serif",
                        size: 13,
                        weight: 600
                    },
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = context.parsed.y;
                            return `${label}: ${value.toLocaleString('pt-BR')}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#666666',
                        font: {
                            family: "'Barlow', sans-serif",
                            size: 12,
                            weight: 600
                        }
                    }
                },
                y: {
                    grid: {
                        color: '#1a1a1a',
                        lineWidth: 1
                    },
                    ticks: {
                        color: '#666666',
                        font: {
                            family: "'Teko', sans-serif",
                            size: 12,
                            weight: 600
                        },
                        callback: function(value) {
                            return (value / 1000) + 'K';
                        }
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeOutBounce'
            },
            onHover: (event, elements) => {
                if (elements.length > 0) {
                    const element = elements[0];
                    const chart = element.chart;
                    const dataset = chart.data.datasets[element.datasetIndex];
                    
                    // Scale effect on hover
                    chart.update('none');
                }
            }
        }
    });
}

// ━━━ GAUGE CHART - SYSTEM HEALTH ━━━
function initGaugeChart() {
    const ctx = document.getElementById('gaugeChart');
    if (!ctx) return;

    const gaugeValue = 92;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [gaugeValue, 100 - gaugeValue],
                backgroundColor: [
                    MOTOSENSE_CONFIG.colors.activeGreen,
                    'rgba(102, 102, 102, 0.2)'
                ],
                borderWidth: 0,
                cutout: '85%',
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            animation: {
                animateRotate: true,
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// ━━━ REAL-TIME DATA UPDATES ━━━
function updateRealTimeData() {
    // Simulate real-time data updates
    const elements = {
        motorCount: document.querySelector('.online-badge'),
        alertCount: document.querySelector('.alert-count'),
        currentTime: document.querySelector('.current-time'),
        currentDate: document.querySelector('.current-date')
    };

    // Update time
    if (elements.currentTime && elements.currentDate) {
        const now = new Date();
        elements.currentTime.textContent = now.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        elements.currentDate.textContent = now.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        }).toUpperCase();
    }

    // Simulate motor status changes
    const motorItems = document.querySelectorAll('.motor-item');
    motorItems.forEach((item, index) => {
        if (Math.random() > 0.95) { // 5% chance of status change
            const isOnline = item.classList.contains('online');
            const powerElement = item.querySelector('.motor-power');
            const tempElement = item.querySelector('.motor-temp');
            const statusIndicator = item.querySelector('.status-indicator');
            
            if (isOnline && Math.random() > 0.7) {
                // Simulate going offline
                item.classList.remove('online');
                item.classList.add('offline');
                powerElement.textContent = '0W';
                tempElement.textContent = '--°C';
                statusIndicator.classList.remove('online');
                statusIndicator.classList.add('offline');
            } else if (!isOnline && Math.random() > 0.8) {
                // Simulate coming online
                item.classList.remove('offline');
                item.classList.add('online');
                powerElement.textContent = `${Math.floor(Math.random() * 1000 + 1000)}W`;
                tempElement.textContent = `${Math.floor(Math.random() * 30 + 70)}°C`;
                statusIndicator.classList.remove('offline');
                statusIndicator.classList.add('online');
            }
        }
    });

    // Update online count
    if (elements.motorCount) {
        const onlineMotors = document.querySelectorAll('.motor-item.online').length;
        elements.motorCount.textContent = `${onlineMotors} ONLINE`;
    }
}

// ━━━ INTERACTIVE ANIMATIONS ━━━
function initInteractiveAnimations() {
    // Hover effects for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-4px) scale(1.02)';
            card.style.boxShadow = `
                0 16px 64px rgba(0, 0, 0, 0.9),
                0 0 100px rgba(255, 107, 0, 0.2),
                inset 0 1px 0 rgba(255, 107, 0, 0.3)
            `;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.boxShadow = '';
        });
    });

    // Navigation item hover effects
    const navItems = document.querySelectorAll('.nav-item:not(.active)');
    navItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            const speedLines = item.querySelector('.speed-lines');
            if (speedLines) {
                speedLines.style.opacity = '1';
            }
        });

        item.addEventListener('mouseleave', () => {
            const speedLines = item.querySelector('.speed-lines');
            if (speedLines) {
                speedLines.style.opacity = '0';
            }
        });
    });

    // Period toggle functionality
    const periodBtns = document.querySelectorAll('.period-btn');
    periodBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            periodBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Add click animation
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                btn.style.transform = '';
            }, 150);
        });
    });

    // Header button animations
    const headerBtns = document.querySelectorAll('.header-btn');
    headerBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const icon = btn.querySelector('.btn-icon');
            if (icon) {
                icon.style.animation = 'shake 0.5s ease-in-out';
                setTimeout(() => {
                    icon.style.animation = '';
                }, 500);
            }
        });
    });
}

// ━━━ NUMBER COUNTER ANIMATION ━━━
function animateCounters() {
    const counters = document.querySelectorAll('.metric-value-large, .donut-total, .gauge-value');
    
    counters.forEach(counter => {
        const target = parseFloat(counter.textContent.replace(/[^\d.]/g, ''));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format the number based on original format
            const originalText = counter.textContent;
            if (originalText.includes('%')) {
                counter.textContent = `${Math.floor(current)}%`;
            } else if (originalText.includes('W')) {
                counter.textContent = `${Math.floor(current)} W`;
            } else if (originalText.includes('.')) {
                counter.textContent = Math.floor(current).toLocaleString('pt-BR');
            } else {
                counter.textContent = Math.floor(current).toLocaleString('pt-BR');
            }
        }, 16);
    });
}

// ━━━ PROGRESS BAR ANIMATIONS ━━━
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach((bar, index) => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, index * 200);
    });
}

// ━━━ SPARKLINE GENERATION ━━━
function generateSparklines() {
    const sparklines = document.querySelectorAll('.mini-sparkline');
    
    sparklines.forEach(sparkline => {
        // Create mini SVG sparkline
        const data = Array.from({length: 20}, () => Math.random() * 100);
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '100');
        svg.setAttribute('height', '20');
        svg.style.position = 'absolute';
        svg.style.top = '0';
        svg.style.left = '0';
        
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const pathData = data.map((value, index) => {
            const x = (index / (data.length - 1)) * 100;
            const y = 20 - (value / 100) * 20;
            return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
        }).join(' ');
        
        path.setAttribute('d', pathData);
        path.setAttribute('stroke', MOTOSENSE_CONFIG.colors.activeGreen);
        path.setAttribute('stroke-width', '2');
        path.setAttribute('fill', 'none');
        path.style.filter = 'drop-shadow(0 0 4px rgba(0, 255, 65, 0.5))';
        
        svg.appendChild(path);
        sparkline.style.position = 'relative';
        sparkline.appendChild(svg);
    });
}

// ━━━ ALERT SYSTEM ━━━
function initAlertSystem() {
    const alertItems = document.querySelectorAll('.alert-item');
    
    alertItems.forEach(item => {
        const actionBtn = item.querySelector('.alert-action');
        if (actionBtn) {
            actionBtn.addEventListener('click', () => {
                // Simulate alert action
                item.style.opacity = '0.5';
                item.style.transform = 'translateX(20px)';
                
                setTimeout(() => {
                    item.style.opacity = '';
                    item.style.transform = '';
                }, 1000);
            });
        }
    });
}

// ━━━ PERFORMANCE MONITORING ━━━
function monitorPerformance() {
    // Monitor FPS and performance
    let lastTime = performance.now();
    let frameCount = 0;
    
    function checkFPS() {
        const currentTime = performance.now();
        frameCount++;
        
        if (currentTime - lastTime >= 1000) {
            const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
            
            // Log performance if needed
            if (fps < 30) {
                console.warn('MOTOSENSE: Low FPS detected:', fps);
            }
            
            frameCount = 0;
            lastTime = currentTime;
        }
        
        requestAnimationFrame(checkFPS);
    }
    
    requestAnimationFrame(checkFPS);
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
    
    // Initialize animations and interactions
    setTimeout(() => {
        initInteractiveAnimations();
        animateCounters();
        animateProgressBars();
        generateSparklines();
        initAlertSystem();
    }, 500);
    
    // Start real-time updates
    setTimeout(() => {
        updateRealTimeData();
        setInterval(updateRealTimeData, 5000); // Update every 5 seconds
    }, 1000);
    
    // Start performance monitoring
    monitorPerformance();
    
    console.log('🔥 MOTOSENSE Dashboard Ready!');
});

// ━━━ WINDOW RESIZE HANDLER ━━━
window.addEventListener('resize', function() {
    // Reinitialize charts on resize if needed
    setTimeout(() => {
        Chart.helpers.each(Chart.instances, function(instance) {
            instance.resize();
        });
    }, 100);
});

// ━━━ ERROR HANDLING ━━━
window.addEventListener('error', function(e) {
    console.error('MOTOSENSE Error:', e.error);
});

// ━━━ EXPORT FOR GLOBAL ACCESS ━━━
window.MOTOSENSE = {
    config: MOTOSENSE_CONFIG,
    updateRealTimeData,
    animateCounters,
    initMainChart,
    initDonutChart,
    initBarChart,
    initGaugeChart
};

/**
 * ═══════════════════════════════════════════════════════════════
 * END OF MOTOSENSE JAVASCRIPT
 * ═══════════════════════════════════════════════════════════════
 */