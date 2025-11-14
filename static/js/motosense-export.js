// Exportar para CSV
function exportToCSV() {
  const data = getDashboardData();
  const csv = convertToCSV(data);
  downloadFile(csv, 'motosense-dados.csv', 'text/csv');
  showToast('Dados exportados com sucesso!', 'success');
}

// Converter para CSV
function convertToCSV(data) {
  const headers = Object.keys(data[0]).join(',');
  const rows = data.map(obj => Object.values(obj).join(','));
  return headers + '\n' + rows.join('\n');
}

// Download arquivo
function downloadFile(content, filename, type) {
  const blob = new Blob([content], { type: type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

// Exportar gráfico como imagem
function exportChartAsImage() {
  const canvas = document.getElementById('mainChart');
  canvas.toBlob(blob => {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'grafico-motosense.png';
    link.click();
    URL.revokeObjectURL(url);
  });
  showToast('Gráfico exportado!', 'success');
}

// Imprimir relatório
function printDashboard() {
  window.print();
}

// Obter dados do dashboard
function getDashboardData() {
  // Implementar coleta de dados do dashboard
  return [
    { motor: 'Motor 1', temperatura: 85, rpm: 3400, status: 'OK' },
    { motor: 'Motor 2', temperatura: 78, rpm: 3200, status: 'OK' }
  ];
}

// Mostrar toast notification
function showToast(message, type) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('fade-in');
  }, 100);
  
  setTimeout(() => {
    toast.remove();
  }, 3000);
}