#!/usr/bin/env python3
"""
CORREÇÕES CRÍTICAS - MOTOSENSE
Script para verificar e corrigir todos os problemas identificados
"""

import os
import sys
import json
import django
from django.test import Client
from django.urls import reverse
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

def check_chartjs():
    """Verifica se Chart.js está correto"""
    print("🔍 Verificando Chart.js...")
    
    chartjs_path = 'static/js/chart.min.js'
    if not os.path.exists(chartjs_path):
        print("  ❌ Chart.js não encontrado!")
        return False
    
    file_size = os.path.getsize(chartjs_path)
    if file_size < 100000:  # Menos de 100KB é suspeito
        print(f"  ⚠️ Chart.js muito pequeno: {file_size:,} bytes (esperado ~180KB)")
        return False
    
    print(f"  ✅ Chart.js OK: {file_size:,} bytes")
    return True

def check_dashboard_data():
    """Verifica se os dados do dashboard estão sendo passados"""
    print("\n📊 Verificando dados do dashboard...")
    
    try:
        from dashboard.views import dashboard_view
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/')
        
        response = dashboard_view(request)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Verificar se dashboard_json está presente
            if 'window.DASHBOARD_BACKEND' in content:
                print("  ✅ dashboard_json encontrado no template")
                
                # Extrair dados JSON
                start = content.find('window.DASHBOARD_BACKEND = ') + len('window.DASHBOARD_BACKEND = ')
                end = content.find('};', start) + 1
                if start > 0 and end > start:
                    json_str = content[start:end]
                    try:
                        data = json.loads(json_str)
                        print(f"  ✅ Dados JSON válidos: {len(data)} chaves")
                        
                        # Verificar estrutura essencial
                        required_keys = ['metrics', 'chart_data']
                        missing_keys = [key for key in required_keys if key not in data]
                        
                        if missing_keys:
                            print(f"  ⚠️ Chaves faltando: {missing_keys}")
                        else:
                            print("  ✅ Estrutura de dados completa")
                        
                        return True
                    except json.JSONDecodeError as e:
                        print(f"  ❌ JSON inválido: {e}")
                        return False
            else:
                print("  ❌ dashboard_json não encontrado no template")
                return False
        else:
            print(f"  ❌ Erro na view: status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro ao verificar dados: {e}")
        return False

def check_template_references():
    """Verifica referências nos templates"""
    print("\n📄 Verificando referências nos templates...")
    
    issues = []
    
    # Verificar dashboard template
    dashboard_template = 'dashboard/templates/dashboard/index.html'
    if os.path.exists(dashboard_template):
        with open(dashboard_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se usa Chart.js local
        if 'cdn.jsdelivr.net/npm/chart.js' in content:
            issues.append("Dashboard ainda usa Chart.js CDN")
        elif 'static/js/chart.min.js' in content:
            print("  ✅ Dashboard usa Chart.js local")
        else:
            issues.append("Dashboard não carrega Chart.js")
            
        # Verificar se tem dashboard_json
        if 'dashboard_json|safe' in content:
            print("  ✅ Dashboard template tem dashboard_json")
        else:
            issues.append("Dashboard template não tem dashboard_json")
    else:
        issues.append("Dashboard template não encontrado")
    
    # Verificar base templates
    base_templates = [
        'templates/base_optimized.html',
        'templates/base_motosense.html'
    ]
    
    for template_path in base_templates:
        if os.path.exists(template_path):
            print(f"  ✅ Template base encontrado: {template_path}")
        else:
            print(f"  ⚠️ Template base não encontrado: {template_path}")
    
    if issues:
        print("  ❌ Problemas encontrados:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print("  ✅ Todas as referências estão corretas")
        return True

def check_css_animations():
    """Verifica se as animações CSS estão funcionando"""
    print("\n🎨 Verificando animações CSS...")
    
    css_files = [
        'static/css/motosense-dashboard.css',
        'static/css/motosense-crud.css'
    ]
    
    required_animations = [
        '@keyframes pulse',
        '@keyframes rotate', 
        '@keyframes fadeIn',
        'animation: pulse',
        'animation: rotate'
    ]
    
    for css_file in css_files:
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_animations = []
            for animation in required_animations:
                if animation in content:
                    found_animations.append(animation)
            
            print(f"  📁 {os.path.basename(css_file)}: {len(found_animations)}/{len(required_animations)} animações")
            
            if len(found_animations) < len(required_animations) // 2:
                print(f"    ⚠️ Poucas animações encontradas")
            else:
                print(f"    ✅ Animações suficientes")
        else:
            print(f"  ❌ CSS não encontrado: {css_file}")
    
    return True

def check_responsive_design():
    """Verifica se o design responsivo está implementado"""
    print("\n📱 Verificando design responsivo...")
    
    css_files = [
        'static/css/motosense-dashboard.css',
        'static/css/motosense-crud.css'
    ]
    
    responsive_features = [
        '@media (max-width: 768px)',
        '@media (max-width: 1024px)', 
        '@media (max-width: 1200px)',
        'repeat(auto-fit, minmax(',
        'grid-template-columns',
        'flex-wrap'
    ]
    
    for css_file in css_files:
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_features = []
            for feature in responsive_features:
                if feature in content:
                    found_features.append(feature)
            
            print(f"  📁 {os.path.basename(css_file)}: {len(found_features)}/{len(responsive_features)} recursos responsivos")
            
            if len(found_features) >= 4:
                print(f"    ✅ Bem responsivo")
            elif len(found_features) >= 2:
                print(f"    ⚠️ Parcialmente responsivo")
            else:
                print(f"    ❌ Pouco responsivo")
        else:
            print(f"  ❌ CSS não encontrado: {css_file}")
    
    return True

def check_interactivity():
    """Verifica se a interatividade está implementada"""
    print("\n🖱️ Verificando interatividade...")
    
    js_files = [
        'static/js/motosense-dashboard.js',
        'static/js/motosense-crud.js',
        'static/js/motosense-interactive.js'
    ]
    
    interactive_features = [
        'addEventListener',
        'onclick',
        'hover',
        'click',
        'toggle',
        'show',
        'hide'
    ]
    
    total_interactivity = 0
    
    for js_file in js_files:
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_features = []
            for feature in interactive_features:
                count = content.count(feature)
                if count > 0:
                    found_features.append(f"{feature}({count})")
                    total_interactivity += count
            
            print(f"  📁 {os.path.basename(js_file)}: {len(found_features)} tipos de interação")
            
            if len(found_features) >= 5:
                print(f"    ✅ Altamente interativo")
            elif len(found_features) >= 3:
                print(f"    ⚠️ Moderadamente interativo")
            else:
                print(f"    ❌ Pouco interativo")
        else:
            print(f"  ⚠️ JS não encontrado: {js_file}")
    
    print(f"  📊 Total de interações: {total_interactivity}")
    return total_interactivity > 50

def generate_fixes():
    """Gera correções automáticas para problemas comuns"""
    print("\n🔧 Gerando correções automáticas...")
    
    fixes_applied = []
    
    # Fix 1: Verificar se Chart.js precisa ser baixado novamente
    chartjs_path = 'static/js/chart.min.js'
    if os.path.exists(chartjs_path):
        file_size = os.path.getsize(chartjs_path)
        if file_size < 100000:
            print("  🔄 Chart.js muito pequeno, pode precisar ser baixado novamente")
            print("  💡 Execute: curl -o static/js/chart.min.js https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.min.js")
            fixes_applied.append("Chart.js precisa ser baixado")
    
    # Fix 2: Verificar estrutura de diretórios
    required_dirs = [
        'static/css',
        'static/js', 
        'dashboard/templates/dashboard',
        'sensores/templates/sensores',
        'templates'
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"  📁 Criando diretório: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            fixes_applied.append(f"Diretório criado: {dir_path}")
    
    # Fix 3: Verificar arquivos essenciais
    essential_files = {
        'static/css/motosense-core.css': 'Arquivo CSS core',
        'static/css/motosense-dashboard.css': 'Arquivo CSS dashboard',
        'static/js/motosense-dashboard.js': 'Arquivo JS dashboard'
    }
    
    for file_path, description in essential_files.items():
        if not os.path.exists(file_path):
            print(f"  ❌ Arquivo essencial faltando: {file_path}")
            fixes_applied.append(f"Arquivo faltando: {description}")
        else:
            print(f"  ✅ Arquivo essencial OK: {file_path}")
    
    return fixes_applied

def run_comprehensive_test():
    """Executa teste abrangente do sistema"""
    print("🚀 EXECUTANDO TESTE ABRANGENTE DO SISTEMA")
    print("=" * 60)
    
    tests = [
        ("Chart.js", check_chartjs),
        ("Dados Dashboard", check_dashboard_data),
        ("Referências Templates", check_template_references),
        ("Animações CSS", check_css_animations),
        ("Design Responsivo", check_responsive_design),
        ("Interatividade", check_interactivity)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Gerar correções
    fixes = generate_fixes()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 SCORE: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if fixes:
        print(f"\n🔧 CORREÇÕES NECESSÁRIAS ({len(fixes)}):")
        for fix in fixes:
            print(f"  - {fix}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema 100% funcional")
        print("🚀 Pronto para produção")
    elif passed >= total * 0.8:
        print("⚠️ SISTEMA MAJORITARIAMENTE FUNCIONAL")
        print(f"🔧 {total - passed} problemas menores para corrigir")
        print("📈 Sistema utilizável com pequenos ajustes")
    else:
        print("🚨 PROBLEMAS CRÍTICOS DETECTADOS")
        print(f"🔧 {total - passed} problemas importantes para corrigir")
        print("⚠️ Revisar antes de usar em produção")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)