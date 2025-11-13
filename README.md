# 🏍️ MOTOSENSE - Sistema de Controle de Motores

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2.8-green.svg)](https://www.djangoproject.com/)
[![Security](https://img.shields.io/badge/security-hardened-brightgreen.svg)](#-segurança)

Sistema web para gerenciamento e monitoramento de motores com sensores em tempo real.

![Dashboard Preview](docs/screenshots/dashboard.png)

## ✨ Features

- 📊 Dashboard interativo com gráficos em tempo real
- 🏍️ CRUD completo de Motores
- 📡 Gerenciamento de Sensores
- 📈 Histórico de dados com QuerySets otimizados
- 🎨 Interface moderna com tema racing (laranja/preto)
- 📱 Design responsivo
- 🔒 Sistema de autenticação seguro
- 🛡️ Proteção contra XSS, CSRF e outras vulnerabilidades
- ⚡ Cache otimizado para performance
- 📝 Logging estruturado

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- pip

### Instalação

1. Clone o repositório
```bash
git clone https://github.com/Paola5858/CRUD.git
cd CRUD
```

2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
```

3. Instale dependências
```bash
pip install -r requirements.txt
```

4. Configure variáveis de ambiente
```bash
cp .env.example .env
```
Edite .env com suas configurações

5. Execute migrações
```bash
python manage.py migrate
```

6. Crie superusuário
```bash
python manage.py createsuperuser
```

7. Rode o servidor
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## 📁 Estrutura do Projeto

```
CRUD/
├── sensores/ # App principal
│ ├── models.py # Motor, Sensor, DadosSensor
│ ├── views.py # Views com Factory/Strategy
│ ├── factories.py # CrudFactory
│ └── templates/
├── dashboard/ # Dashboard app
├── static/
│ ├── css/ # Estilos personalizados
│ └── js/ # Chart.js e scripts
└── setup/ # Configurações Django
```

## 🔒 Segurança

O MOTOSENSE implementa várias camadas de segurança:

### Proteções Implementadas
- ✅ **XSS Protection**: Sanitização de entrada e uso seguro do DOM
- ✅ **CSRF Protection**: Tokens CSRF em todos os formulários
- ✅ **SQL Injection**: Uso de ORM Django e queries parametrizadas
- ✅ **Secure Headers**: HSTS, X-Frame-Options, Content-Type-Nosniff
- ✅ **Path Traversal**: Validação de caminhos de arquivo
- ✅ **Secure Cookies**: Flags HttpOnly e Secure em produção
- ✅ **Input Validation**: Validação rigorosa de dados de entrada

### Configuração Segura
```bash
# Configure variáveis de ambiente seguras
cp .env.example .env

# Gere uma SECRET_KEY segura
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Configure no .env:
# SECRET_KEY=sua-chave-gerada-aqui
# DEBUG=False  # Para produção
# ALLOWED_HOSTS=seu-dominio.com
```

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Executar testes com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report

# Testes de segurança específicos
python manage.py test sensores.tests.SecurityTest
```

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### CRUD de Motores
![Motores](docs/screenshots/motores.png)

## 🛠️ Tecnologias

- **Backend**: Django 5.2.8 (versão segura)
- **Frontend**: HTML5, CSS3, JavaScript (XSS-safe)
- **Gráficos**: Chart.js
- **Database**: SQLite (dev) / MySQL (prod)
- **Cache**: Django Cache Framework
- **Security**: CSRF, XSS, SQL Injection protection
- **Performance**: WhiteNoise, asset compression
- **Monitoring**: Structured logging

## 🚀 Deploy em Produção

### Checklist de Segurança
- [ ] SECRET_KEY configurada e segura
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado
- [ ] HTTPS habilitado
- [ ] Banco de dados com credenciais seguras
- [ ] Logs configurados
- [ ] Backup automatizado

### Variáveis de Ambiente Obrigatórias
```bash
SECRET_KEY=sua-chave-super-secreta
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DB_PASSWORD=senha-segura-do-banco
```

## 📝 License

MIT License - veja [LICENSE](LICENSE)

## 👩‍💻 Autor

**Paola Machado** - [@Paola5858](https://github.com/Paola5858)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Segurança
- Sempre valide entrada do usuário
- Use métodos seguros do DOM (evite innerHTML)
- Teste contra vulnerabilidades comuns
- Mantenha dependências atualizadas

## 📞 Suporte

Se encontrar problemas de segurança, por favor reporte de forma responsável.

---

⭐ Se este projeto ajudou você, considere dar uma estrela!

## 📋 Changelog

### v2.0.0 - Security Hardening
- ✅ Corrigidas vulnerabilidades XSS críticas
- ✅ Implementada proteção contra Path Traversal
- ✅ Removidas credenciais hardcoded
- ✅ Atualizado Django para versão segura
- ✅ Adicionados testes de segurança
- ✅ Melhorada configuração de produção