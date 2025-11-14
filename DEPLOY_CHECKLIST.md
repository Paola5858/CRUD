# 🚀 DEPLOY CHECKLIST - MOTOSENSE ENTERPRISE

## ✅ **PRÉ-DEPLOY - CONFIGURAÇÃO**

### **1. Dependências**
```bash
pip install -r requirements.txt
```

### **2. Variáveis de Ambiente (.env)**
```bash
# Django
SECRET_KEY=your-super-secret-key-here-50-chars
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database
DB_NAME=ctrlmotordb
DB_USER=motosense
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=3306

# MQTT CloudAMQP
MQTT_BROKER=your-broker.cloudamqp.com
MQTT_USERNAME=your-mqtt-username
MQTT_PASSWORD=your-mqtt-password

# Redis
REDIS_HOST=redis

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### **3. Migrations**
```bash
python manage.py migrate
python manage.py migrate sensores 0002  # Particionamento
```

## 🐳 **DEPLOY DOCKER**

### **1. Build e Start**
```bash
docker-compose build
docker-compose up -d
```

### **2. Setup Inicial**
```bash
# Migrations
docker-compose exec web python manage.py migrate

# Superuser
docker-compose exec web python manage.py createsuperuser

# Collect static
docker-compose exec web python manage.py collectstatic --noinput

# Create API tokens
docker-compose exec web python manage.py drf_create_token admin
```

### **3. Verificar Serviços**
```bash
docker-compose ps
docker-compose logs -f web
docker-compose logs -f worker
```

## 🧪 **TESTES DE FUNCIONALIDADE**

### **1. WebSocket**
```javascript
// Browser console
ws = new WebSocket('ws://localhost/ws/dashboard/')
ws.onmessage = (e) => console.log(JSON.parse(e.data))
```

### **2. API REST**
```bash
# Get token
TOKEN=$(docker-compose exec web python manage.py drf_create_token admin | grep Token | cut -d' ' -f2)

# Test endpoints
curl -H "Authorization: Token $TOKEN" http://localhost/api/motores/
curl -H "Authorization: Token $TOKEN" http://localhost/api/dados/
```

### **3. MQTT Worker**
```bash
# Check worker logs
docker-compose logs -f worker

# Test with test_publish.py
python test_publish.py
```

### **4. Dashboard**
- Acesse: http://localhost
- Login com superuser
- Verifique KPI cards
- Teste tempo real (publique MQTT)
- Verifique alertas

## 📊 **PERFORMANCE VALIDATION**

### **1. Query Speed**
```python
# Django shell
import time
from sensores.models import DadosSensor

start = time.time()
count = DadosSensor.objects.filter(data_hora__gte='2025-01-01').count()
print(f"Query time: {time.time() - start:.3f}s")
```

### **2. Dashboard Load**
- Chrome DevTools > Network
- Disable cache
- Refresh dashboard
- Total time < 1s

### **3. WebSocket Latency**
- Abrir 2 browsers
- Publicar MQTT
- Verificar update instantâneo

## 🔒 **SECURITY CHECKLIST**

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` forte (50+ chars)
- [ ] `ALLOWED_HOSTS` configurado
- [ ] HTTPS habilitado (produção)
- [ ] Firewall configurado
- [ ] Backup automático
- [ ] Logs monitorados

## 📈 **MONITORAMENTO**

### **1. Health Checks**
```bash
# Web app
curl http://localhost/admin/

# API
curl http://localhost/api/docs/

# Database
docker-compose exec db mysql -u root -p -e "SHOW TABLES;"
```

### **2. Logs**
```bash
# Application logs
docker-compose logs -f web worker

# Database logs
docker-compose logs -f db

# Nginx logs
docker-compose logs -f nginx
```

### **3. Métricas**
- CPU usage < 70%
- Memory usage < 80%
- Disk space > 20%
- Response time < 300ms

## 🚨 **TROUBLESHOOTING**

### **WebSocket não conecta**
```bash
# Verificar Redis
docker-compose exec redis redis-cli ping

# Verificar Channels
docker-compose exec web python -c "from channels.layers import get_channel_layer; print(get_channel_layer())"
```

### **MQTT não recebe**
```bash
# Verificar credenciais
docker-compose exec worker python -c "import os; print(os.getenv('MQTT_USERNAME'))"

# Test connection
docker-compose exec worker python test_publish.py
```

### **API 401 Unauthorized**
```bash
# Create token
docker-compose exec web python manage.py drf_create_token username

# Check token
curl -H "Authorization: Token YOUR_TOKEN" http://localhost/api/motores/
```

## 🎯 **PRÓXIMOS PASSOS**

### **Produção**
1. Configurar domínio próprio
2. SSL com Let's Encrypt
3. Backup automatizado
4. Monitoramento com Grafana
5. CI/CD pipeline

### **Escalabilidade**
1. Load balancer
2. Kubernetes
3. Database clustering
4. CDN para static files
5. Elasticsearch para logs

**Status: ✅ PRONTO PARA PRODUÇÃO**