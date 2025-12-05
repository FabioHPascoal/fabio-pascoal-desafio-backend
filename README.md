# Desafio backend IUPI - API de transações financeiras

Uma API REST completa para gerenciamento de transações financeiras (receitas e despesas), desenvolvida com Django e Django REST Framework.

## Sumário

- [Stack](#-stack-utilizada)
- [Instalação](#-instalação-das-dependências)
- [Configuração do Banco de Dados](#️-preparar-o-banco-de-dados)
- [Rodando o Projeto](#️-rodar-o-projeto)
- [Autenticação](#-autenticação)
- [Endpoints](#-endpoints)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)

## 🛠 Stack utilizada

* **Python** 3.x
* **Django** 5
* **Django REST Framework** - Framework REST para Django
* **SimpleJWT** - Autenticação JWT (JSON Web Token)
* **SQLite** - Banco de dados padrão

## Instalação das dependências

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd fabio-pascoal-desafio-backend
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

## Preparar o banco de dados

### 1. Navegue para a pasta do projeto
```bash
cd project
```

### 2. Gere as migrações
```bash
python manage.py makemigrations
```

### 3. Aplique as migrações
```bash
python manage.py migrate
```

### 4. Crie um superusuário
```bash
python manage.py createsuperuser
```

Você será solicitado a fornecer um nome de usuário, email e senha.

## Rodar o projeto

Para iniciar o servidor de desenvolvimento:
```bash
python manage.py runserver
```

A API ficará disponível em:
```
http://localhost:8000/
```

O painel de administração Django estará em:
```
http://localhost:8000/admin/
```

## Autenticação

A API utiliza **JWT (JSON Web Token)** para autenticação. Todos os endpoints (exceto o de login) requerem um token válido.

### Obter um Token

**Endpoint:** `POST /login/`

**Body:**
```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta (sucesso):**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar o Token

Inclua o token `access` no header `Authorization` de todas as requisições autenticadas:

```bash
Authorization: Bearer <seu_access_token>
```

### Renovar o Token

Se o token `access` expirar (padrão: 60 minutos), use o `refresh` para obter um novo:

**Endpoint:** `POST /token/refresh/`

**Body:**
```json
{
    "refresh": "seu_refresh_token"
}
```

## Endpoints

### Transações

#### 1. Listar todas as transações
```
GET /transactions/
```

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters (opcionais):**
- `description` - Filtrar por descrição (busca parcial)
- `type` - Filtrar por tipo (`income` ou `expense`)
- `size` - Número de itens por página (padrão: 10, máximo: 50)
- `page` - Número da página (padrão: 1)

**Resposta (sucesso - 200):**
```json
{
    "count": 15,
    "next": "http://localhost:8000/transactions/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": "username",
            "description": "Salário",
            "amount": "5000.00",
            "type": "income",
            "date": "2024-01-15"
        }
    ]
}
```

#### 2. Criar uma nova transação
```
POST /transactions/
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body:**
```json
{
    "description": "Compra de supermercado",
    "amount": "150.50",
    "type": "expense",
    "date": "2024-01-20"
}
```

**Resposta (sucesso - 201):**
```json
{
    "id": 2,
    "user": "username",
    "description": "Compra de supermercado",
    "amount": "150.50",
    "type": "expense",
    "date": "2024-01-20"
}
```

#### 3. Obter detalhes de uma transação
```
GET /transactions/<id>/
```

**Resposta (sucesso - 200):**
```json
{
    "id": 1,
    "user": "username",
    "description": "Salário",
    "amount": "5000.00",
    "type": "income",
    "date": "2024-01-15"
}
```

#### 4. Atualizar uma transação (completo)
```
PUT /transactions/<id>/
```

**Body:**
```json
{
    "description": "Salário Atualizado",
    "amount": "5500.00",
    "type": "income",
    "date": "2024-01-15"
}
```

#### 5. Atualizar parcialmente uma transação
```
PATCH /transactions/<id>/
```

**Body (apenas os campos a atualizar):**
```json
{
    "amount": "5500.00"
}
```

#### 6. Deletar uma transação
```
DELETE /transactions/<id>/
```

**Resposta (sucesso - 204):** Sem conteúdo

#### 7. Obter resumo das transações
```
GET /summary/
```

**Resposta (sucesso - 200):**
```json
{
    "total_income": 10000.00,
    "total_expense": 2500.00,
    "net_balance": 7500.00
}
```

## Exemplos de Uso

### Exemplo 1: Autenticar e listar transações

```bash
# 1. Obter token
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Salve o access token retornado

# 2. Listar transações
curl -X GET http://localhost:8000/transactions/ \
  -H "Authorization: Bearer <seu_access_token>"
```

### Exemplo 2: Criar uma transação

```bash
curl -X POST http://localhost:8000/transactions/ \
  -H "Authorization: Bearer <seu_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Venda de produto",
    "amount": "250.00",
    "type": "income",
    "date": "2024-01-22"
  }'
```

### Exemplo 3: Filtrar transações por tipo

```bash
curl -X GET "http://localhost:8000/transactions/?type=expense&size=20" \
  -H "Authorization: Bearer <seu_access_token>"
```

### Exemplo 4: Obter resumo

```bash
curl -X GET http://localhost:8000/summary/ \
  -H "Authorization: Bearer <seu_access_token>"
```

## Estrutura do Projeto

```
project/
├── application/              # App principal da API
│   ├── migrations/          # Migrações do banco de dados
│   ├── models.py            # Modelos (Transaction)
│   ├── views.py             # Views/endpoints
│   ├── serializers.py       # Serializadores
│   ├── pagination.py        # Configuração de paginação
│   ├── urls.py              # Rotas
│   ├── tests.py             # Testes
│   └── admin.py             # Admin do Django
│
├── project/                 # Configurações do Django
│   ├── settings.py          # Configurações gerais
│   ├── urls.py              # URLs principais
│   ├── asgi.py              # ASGI
│   └── wsgi.py              # WSGI
│
├── manage.py                # Script de gerenciamento
└── db.sqlite3               # Banco de dados
```

## Validações

A API realiza as seguintes validações:

- **Amount**: Deve ser maior que zero
- **Type**: Deve ser `income` ou `expense`
- **Date**: Deve ser uma data válida
- **Description**: Campo obrigatório, máximo 255 caracteres
- **Autenticação**: Token JWT válido e não expirado

## Configurações Importantes

- **Timeout do Token**: 60 minutos
- **Paginação padrão**: 10 itens por página
- **Máximo por página**: 50 itens
- **Autenticação**: JWT obrigatória em todos os endpoints

## Notas Adicionais

- Todas as transações são filtradas automaticamente por usuário autenticado
- As transações são ordenadas por data (mais recentes primeiro) na listagem
- O banco de dados SQLite é adequado para desenvolvimento; em produção, considere usar PostgreSQL