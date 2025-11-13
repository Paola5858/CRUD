"""
Context processors para otimização de assets
"""
import os
import hashlib
from pathlib import Path
from django.conf import settings
from django.core.cache import cache

def asset_versions(request):
    """
    Adiciona versões de assets para cache busting
    """
    def get_file_version(file_path):
        """Gera hash do arquivo para versionamento"""
        # Sanitize file path to prevent path traversal
        safe_path = Path(file_path).as_posix()
        if '..' in safe_path or safe_path.startswith('/'):
            return '1.0'
            
        cache_key = f'asset_version_{safe_path.replace("/", "_")}'
        version = cache.get(cache_key)
        
        if version is None:
            try:
                # Use Path for secure path handling
                base_path = Path(settings.BASE_DIR) / 'static'
                full_path = base_path / safe_path
                
                # Ensure the resolved path is within the static directory
                if not str(full_path.resolve()).startswith(str(base_path.resolve())):
                    return '1.0'
                    
                if full_path.exists():
                    with open(full_path, 'rb') as f:
                        content = f.read()
                        # Use SHA-256 instead of MD5 for security
                        version = hashlib.sha256(content).hexdigest()[:8]
                else:
                    version = '1.0'
                
                # Cache por 1 hora em desenvolvimento, 24h em produção
                timeout = 3600 if settings.DEBUG else 86400
                cache.set(cache_key, version, timeout)
            except (OSError, IOError, ValueError) as e:
                # Log the error in production
                if not settings.DEBUG:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f'Asset version error for {safe_path}: {e}')
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