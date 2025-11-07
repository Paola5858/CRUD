"""
Context processors para otimização de assets
"""
import os
import hashlib
from django.conf import settings
from django.core.cache import cache

def asset_versions(request):
    """
    Adiciona versões de assets para cache busting
    """
    def get_file_version(file_path):
        """Gera hash do arquivo para versionamento"""
        cache_key = f'asset_version_{file_path}'
        version = cache.get(cache_key)
        
        if version is None:
            try:
                full_path = os.path.join(settings.BASE_DIR, 'static', file_path)
                if os.path.exists(full_path):
                    with open(full_path, 'rb') as f:
                        content = f.read()
                        version = hashlib.md5(content).hexdigest()[:8]
                else:
                    version = '1.0'
                
                # Cache por 1 hora em desenvolvimento, 24h em produção
                timeout = 3600 if settings.DEBUG else 86400
                cache.set(cache_key, version, timeout)
            except:
                version = '1.0'
        
        return version
    
    return {
        'css_version': get_file_version('css/motosense-core.css'),
        'js_version': get_file_version('js/motosense-interactive.js'),
        'debug': settings.DEBUG
    }

def performance_config(request):
    """
    Configurações de performance
    """
    return {
        'enable_cache': not settings.DEBUG,
        'cache_timeout': 86400 if not settings.DEBUG else 0,
        'compress_assets': not settings.DEBUG
    }