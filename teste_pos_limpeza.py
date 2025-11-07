#!/usr/bin/env python3
"""
TESTE PÓS-LIMPEZA - MOTOSENSE
Script para verificar se todas as funcionalidades estão operacionais após a limpeza de arquivos
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

def test_static_files():
    """Testa se todos os arquivos estáticos necessários existem"""
    print("🔍 Testando arquivos estáticos...")
    
    required_files = [
        'static/css/motosense-core.css',
        'static/css/motosense-crud.css', 
        'static/css/motosense-dashboard.css',
        'static/js/chart.min.js',
        'static/js/motosense-crud.js',
        'static/js/motosense-dashboard.js',
        'static/js/motosense-interactive.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            file_size = os.path.getsize(file_path)
            print(f"  ✅ {file_path} ({file_size:,} bytes)")
    
    if missing_files:
        print(f"  ❌ Arquivos faltando: {missing_files}")
        return False
    
    # Verificar se arquivos removidos não existem mais
    removed_files = [
        'static/css/style.css',
        'static/css/motosense-table-rows.css'
    ]
    
    for file_path in removed_files:
        if os.path.exists(file_path):
            print(f"  ⚠️ Arquivo deveria ter sido removido: {file_path}")
        else:
            print(f"  ✅ Confirmado removido: {file_path}")
    
    return True

def test_pages():
    """Testa se as páginas principais carregam sem erro"""
    print("\n🌐 Testando páginas principais...")
    
    client = Client()
    
    test_urls = [
        ('Dashboard', '/'),
        ('Motores', '/sensores/motor/'),
        ('Sensores', '/sensores/sensor/'),
        ('Dados', '/sensores/dados/'),
    ]
    
    results = []
    for name, url in test_urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {name} ({url}) - Status: {response.status_code}")
                results.append(True)
            else:
                print(f"  ❌ {name} ({url}) - Status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"  ❌ {name} ({url}) - Erro: {str(e)}")
            results.append(False)
    
    return all(results)

def test_css_content():
    """Verifica se o conteúdo CSS consolidado está correto"""
    print("\n🎨 Testando conteúdo CSS...")
    
    # Verificar se motosense-crud.css contém os estilos de table rows
    crud_css_path = 'static/css/motosense-crud.css'
    if os.path.exists(crud_css_path):
        with open(crud_css_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se contém estilos essenciais
        essential_classes = [
            '.table-row',
            '.motor-avatar', 
            '.power-display',
            '.status-badge',
            '.action-btn',
            '.expanded-row'
        ]
        
        missing_classes = []
        for css_class in essential_classes:
            if css_class not in content:
                missing_classes.append(css_class)
            else:
                print(f"  ✅ Classe encontrada: {css_class}")
        
        if missing_classes:
            print(f"  ❌ Classes faltando: {missing_classes}")
            return False
        
        print(f"  ✅ motosense-crud.css consolidado corretamente ({len(content):,} caracteres)")
        return True
    else:
        print(f"  ❌ Arquivo não encontrado: {crud_css_path}")
        return False

def test_template_references():
    """Verifica se os templates não referenciam arquivos removidos"""
    print("\n📄 Testando referências em templates...")
    
    template_dirs = [
        'dashboard/templates/',
        'sensores/templates/',
        'templates/'
    ]
    
    removed_references = ['style.css', 'motosense-table-rows.css']
    issues_found = []
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            for ref in removed_references:
                                if ref in content:
                                    issues_found.append(f"{file_path} ainda referencia {ref}")
                                    
                        except Exception as e:
                            print(f"  ⚠️ Erro ao ler {file_path}: {e}")
    
    if issues_found:
        print("  ❌ Referências problemáticas encontradas:")
        for issue in issues_found:
            print(f"    - {issue}")
        return False
    else:
        print("  ✅ Nenhuma referência a arquivos removidos encontrada")
        return True

def calculate_savings():
    """Calcula a economia de espaço obtida"""
    print("\n📊 Calculando economia de espaço...")
    
    # Tamanhos estimados dos arquivos removidos
    removed_sizes = {
        'style.css': 5200,  # 5.2KB
        'motosense-table-rows.css': 12000  # 12KB
    }
    
    total_removed = sum(removed_sizes.values())
    
    # Tamanho atual dos arquivos CSS
    current_sizes = {}
    css_files = [
        'static/css/motosense-core.css',
        'static/css/motosense-crud.css',
        'static/css/motosense-dashboard.css'
    ]
    
    total_current = 0
    for css_file in css_files:
        if os.path.exists(css_file):
            size = os.path.getsize(css_file)
            current_sizes[css_file] = size
            total_current += size
            print(f"  📁 {os.path.basename(css_file)}: {size:,} bytes")
    
    print(f"\n  📉 Arquivos removidos: {total_removed:,} bytes")
    print(f"  📊 Total atual: {total_current:,} bytes")
    
    # Estimativa do tamanho anterior (considerando que table-rows foi consolidado)
    estimated_previous = total_current + removed_sizes['style.css']  # style.css era redundante
    savings_percentage = (removed_sizes['style.css'] / estimated_previous) * 100
    
    print(f"  💾 Economia líquida: ~{removed_sizes['style.css']:,} bytes ({savings_percentage:.1f}%)")
    print(f"  🎯 Redução de arquivos: 2 arquivos removidos")
    
    return True

def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES PÓS-LIMPEZA - MOTOSENSE")
    print("=" * 60)
    
    tests = [
        ("Arquivos Estáticos", test_static_files),
        ("Páginas Principais", test_pages),
        ("Conteúdo CSS", test_css_content),
        ("Referências Templates", test_template_references),
        ("Economia de Espaço", calculate_savings)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status}: {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para uso após limpeza")
        print("🚀 Recomendação: Deploy para produção liberado")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM!")
        print("🔧 Revisar problemas antes do deploy")
        print("📞 Contatar equipe de desenvolvimento")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)