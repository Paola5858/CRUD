@echo off
echo 🏍️ MOTOSENSE - Iniciando Servidor
echo ================================

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Instalar dependências se necessário
pip install python-dotenv

REM Verificar sistema
python manage.py check

REM Executar migrações
python manage.py migrate

REM Iniciar servidor
echo.
echo 🚀 Servidor iniciando em http://localhost:8000
echo 📊 Dashboard: http://localhost:8000/dashboard/
echo 🏍️ Motores CRUD: http://localhost:8000/sensores/motor/
echo.
python manage.py runserver

pause