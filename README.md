# 🏍️ MOTOSENSE - Industrial Motor & Sensor Monitoring System

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2.8-green.svg)](https://www.djangoproject.com/)
[![MQTT](https://img.shields.io/badge/MQTT-CloudAMQP-orange.svg)](https://www.cloudamqp.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)

**Sistema profissional de monitoramento IoT em tempo real para motores industriais**

[Demo](#-demo) • [Instalação](#-instalação-rápida) • [Documentação](#-documentação) • [Contato](#-contato)

</div>

---

## 📊 Sobre o Projeto

MOTOSENSE é uma solução completa de **monitoramento industrial** que integra sensores IoT, comunicação MQTT e dashboard web para **análise em tempo real** de motores e equipamentos.

### 🎯 Principais Funcionalidades

- 📡 **Coleta de Dados IoT**: Recepção automática via MQTT (ESP32/Arduino)
- 📊 **Dashboard Interativo**: Visualização em tempo real com gráficos Chart.js
- 🔧 **CRUD Completo**: Gerenciamento de motores, sensores e dados
- 🔒 **Sistema de Autenticação**: Login/logout seguro com controle de acesso
- ⚡ **Performance Otimizada**: QuerySets otimizados e cache inteligente
- 🛡️ **Segurança Hardened**: Proteção XSS, CSRF, SQL Injection
- 📱 **Responsive Design**: Mobile-first para acesso em qualquer dispositivo

### 🏆 Diferenciais Técnicos

- ✅ Worker MQTT assíncrono com reconexão automática
- ✅ Arquitetura Factory/Strategy para CRUD escalável
- ✅ Logging estruturado para auditoria
- ✅ Compatibilidade com formatos JSON diversos
- ✅ Alertas e notificações em tempo real

---

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.11+
- MySQL 8.0+
- pip
- Git

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/Paola5858/CRUD.git
cd CRUD
```

2. **Crie o ambiente virtual**

```bash
python -m venv .venv
.venv\Scripts\activate # Windows
source .venv/bin/activate # Linux/Mac
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**

```bash
cp .env.example .env
# Edite .env com suas credenciais
```

5. **Execute migrations**

```bash
python manage.py migrate
```

6. **Crie superusuário**

```bash
python manage.py createsuperuser
```

7. **Inicie o servidor**

```bash
python manage.py runserver
```

### Iniciar Worker MQTT (Terminal separado)

```bash
python worker.py
```

**Acesse:** <http://localhost:8000>

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# Django
SECRET_KEY=sua-chave-super-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com

# Database
DB_NAME=ctrlmotordb
DB_USER=root
DB_PASSWORD=sua-senha-mysql
DB_HOST=localhost
DB_PORT=3306

# MQTT CloudAMQP
MQTT_BROKER=leopard.lmq.cloudamqp.com
MQTT_PORT=1883
MQTT_TOPIC=dadosSensor
MQTT_USERNAME=seu-usuario
MQTT_PASSWORD=sua-senha
```

### Formato JSON Esperado do ESP32/Arduino

```json
{
    "motor_id": 1,
    "sensor_id": 1,
    "valor": 85.3,
    "temperatura": 85.3,
    "rpm": 3400,
    "pressao": 2.8
}
```

*Worker aceita tanto `motor_id` quanto `motorid`*

---

## 📁 Estrutura do Projeto

```
CRUD/
├── sensores/           # App principal
│   ├── models.py       # Motor, Sensor, DadosSensor
│   ├── views.py        # Views com Factory/Strategy
│   ├── factories.py    # CrudFactory
│   ├── urls.py         # Rotas do app
│   └── templates/      # Templates HTML
├── dashboard/          # Dashboard IoT
├── usuarios/           # Autenticação
├── static/
│   ├── css/           # Estilos (Core, Dashboard, CRUD)
│   └── js/            # Scripts (Chart.js, interações)
├── logs/              # Logs do worker MQTT
├── worker.py          # Worker MQTT assíncrono
├── test_publish.py    # Script de teste MQTT
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Teste com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report

# Testes de segurança
python manage.py test sensores.tests.SecurityTest

# Teste MQTT manual
python test_publish.py
```

---

## 📊 Tecnologias Utilizadas

| Categoria | Tecnologia |
|-----------|-----------|
| **Backend** | Django 5.2.8, Python 3.11+ |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Gráficos** | Chart.js 4.x |
| **Database** | MySQL 8.0 |
| **IoT/Messaging** | MQTT (Paho), CloudAMQP |
| **Cache** | Django Cache Framework |
| **Security** | CSRF, XSS Protection, HSTS |
| **Static Files** | WhiteNoise |

---

## 🛡️ Segurança

### Proteções Implementadas

- ✅ XSS Protection (auto-escape Django)
- ✅ CSRF Tokens em todos formulários
- ✅ SQL Injection (ORM parametrizado)
- ✅ Secure Headers (HSTS, X-Frame-Options)
- ✅ Path Traversal Prevention
- ✅ HttpOnly/Secure Cookies
- ✅ Input Validation rigorosa

### Boas Práticas

```bash
# Gerar SECRET_KEY segura
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Sempre use .env para credenciais
# Nunca commite .env no Git
```

---

## 🚀 Deploy

### Checklist de Produção

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` forte e única
- [ ] `ALLOWED_HOSTS` configurado
- [ ] HTTPS habilitado
- [ ] Banco com credenciais seguras
- [ ] Logs configurados
- [ ] Backup automatizado
- [ ] Worker rodando com Supervisor/systemd

### Variáveis Obrigatórias

```bash
SECRET_KEY=chave-super-secreta-50-chars
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com
DB_PASSWORD=senha-forte-mysql
MQTT_PASSWORD=senha-cloudamqp
```

---

## 📖 Documentação

### Arquitetura

```
ESP32/Sensor → MQTT Broker → Worker Python → MySQL → Django → Dashboard Web
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes

- Sempre valide entrada do usuário
- Use métodos seguros (evite `innerHTML`)
- Teste contra vulnerabilidades
- Mantenha dependências atualizadas
- Documente código complexo

---

## 📋 Changelog

### v2.0.0 - Security & IoT Hardening (2025-11-14)

- ✅ Integração MQTT completa com ESP32
- ✅ Worker assíncrono com reconexão automática
- ✅ Dashboard em tempo real com Chart.js
- ✅ Correções de segurança XSS/CSRF
- ✅ Sistema de autenticação robusto
- ✅ README profissional

### v1.0.0 - MVP (2025-10-30)

- ✅ CRUD básico de motores e sensores
- ✅ Interface inicial
- ✅ Banco de dados estruturado

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja [LICENSE](LICENSE) para detalhes.

---

## 👩💻 Autora

**Paola Machado**

[![GitHub](https://img.shields.io/badge/GitHub-Paola5858-black?logo=github)](https://github.com/Paola5858)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/paolasoaresmachado)
[![Email](https://img.shields.io/badge/Email-Contact-red?logo=gmail)](mailto:paolasesi351@gmail.com)

---

## 🙏 Agradecimentos

- [Django Project](https://www.djangoproject.com/)
- [Chart.js](https://www.chartjs.org/)
- [CloudAMQP](https://www.cloudamqp.com/)
- [Eclipse Paho MQTT](https://www.eclipse.org/paho/)
- Senai - Excelência em Educação Técnica

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Made with ❤️ by [Paola Machado](https://github.com/Paola5858)

</div>
