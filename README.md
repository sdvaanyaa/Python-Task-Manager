# Task Manager

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   
2. Запустите PostgreSQL:
   ```bash
    brew services start postgresql

3. Примените миграции:   
    ```bash
    psql -U postgres -d task-manager -f migrations/ddl.sql
    psql -U postgres -d task-manager -f migrations/dml.sql

4. Запустите приложение:
   ```bash
   streamlit run main.py