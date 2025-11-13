# 🏍️ MOTOSENSE - Sistema de Controle de Motores

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)

Sistema web para gerenciamento e monitoramento de motores com sensores em tempo real.

![Dashboard Preview](docs/screenshots/dashboard.png)

## ✨ Features

- 📊 Dashboard interativo com gráficos em tempo real
- 🏍️ CRUD completo de Motores
- 📡 Gerenciamento de Sensores
- 📈 Histórico de dados com QuerySets otimizados
- 🎨 Interface moderna com tema racing (laranja/preto)
- 📱 Design responsivo

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

## 🧪 Testes

```bash
python manage.py test
```

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### CRUD de Motores
![Motores](docs/screenshots/motores.png)

## 🛠️ Tecnologias

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Chart.js
- **Database**: SQLite (dev) / MySQL (prod)
- **Cache**: Django Cache Framework

## 📝 License

MIT License - veja [LICENSE](LICENSE)

## 👩‍💻 Autor

**Paola Machado** - [@Paola5858](https://github.com/Paola5858)

---

⭐ Se este projeto ajudou você, considere dar uma estrela!