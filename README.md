# Desafio backend IUPI - API de transações financeiras

Este projeto consiste em uma API REST para gerenciamento de transações financeiras (income/expense), incluindo autenticação JWT, filtros, paginação e associação das transações ao usuário autenticado.

## Stack utilizada

* Python 3.x
* Django 5
* Django REST Framework
* SimpleJWT
* SQLite (banco de dados padrão)

## Stack utilizada

1. Certifique-se de ter o Python instalado.

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

* Windows
```bash
venv\Scripts\activate
```

* Linux / Mac
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Preparar o banco de dados

1. Navegue para a pasta onde se encontra o projeto:
```bash
cd project
```

2. Gerar migrações:
```bash
python manage.py makemigrations
```

3. Aplicar migrações:
```bash
python manage.py migrate
```

4. Criar um superusuário
```bash
python manage.py createsuperuser
```

## Rodar o projeto

Para iniciar o servidor de desenvolvimento:
```bash
python manage.py runserver
```

A API ficará disponível em:
```bash
http://localhost:8000/
```