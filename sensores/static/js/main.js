// MOTOSENSE - JavaScript Global

document.addEventListener('DOMContentLoaded', function() {
    // Animação de hover nas linhas da tabela
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Confirmação de delete
    const deleteButtons = document.querySelectorAll('a[href*="deletar"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.href;
            
            if (confirm('Tem certeza que deseja deletar este item?')) {
                window.location.href = href;
            }
        });
    });

    // Loading state para formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processando...';
            }
        });
    });

    // Validação em tempo real
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    function validateField(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');
        
        field.classList.remove('is-invalid', 'is-valid');
        
        if (isRequired && !value) {
            field.classList.add('is-invalid');
            return false;
        }
        
        if (field.type === 'number' && value && isNaN(value)) {
            field.classList.add('is-invalid');
            return false;
        }
        
        if (value) {
            field.classList.add('is-valid');
        }
        
        return true;
    }

    // Busca em tempo real
    const searchInput = document.querySelector('#searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Navegação inteligente
    function setupSmartNavigation() {
        // Destacar item ativo no menu
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href.split('/')[1])) {
                link.classList.add('active');
            }
        });
        
        // Confirmação antes de sair de formulários modificados
        const forms = document.querySelectorAll('form');
        let formModified = false;
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('change', () => {
                    formModified = true;
                });
            });
            
            form.addEventListener('submit', () => {
                formModified = false;
            });
        });
        
        window.addEventListener('beforeunload', (e) => {
            if (formModified) {
                e.preventDefault();
                e.returnValue = 'Você tem alterações não salvas. Deseja realmente sair?';
            }
        });
    }
    
    // Atalhos de teclado
    function setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + S para salvar formulários
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                const submitBtn = document.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                }
            }
            
            // Esc para voltar
            if (e.key === 'Escape') {
                const backBtn = document.querySelector('a[href*="listar"]');
                if (backBtn) {
                    backBtn.click();
                }
            }
        });
    }
    
    setupSmartNavigation();
    setupKeyboardShortcuts();

    window.MOTOSENSE = {
        validateField: validateField
    };
});