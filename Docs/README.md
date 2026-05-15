![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)

# 📚 Sumário

- [📌 Sobre o Projeto](#-sobre-o-projeto)
- [🚀 Getting Started](#-getting-started)
  - [⚙️ Pré-requisitos](#️-pré-requisitos)
  - [📥 Clonando o Repositório](#-clonando-o-repositório)
  - [🔧 Configuração do Backend](#-configuração-do-backend)
  - [🔐 Variáveis de Ambiente](#-variáveis-de-ambiente)
- [🔄 Fluxo da Aplicação](#-fluxo-da-aplicação)
- [🏗 Arquitetura da Aplicação](#-arquitetura-da-aplicação)
- [🛠 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🧪 Estratégia de Testes](#-estratégia-de-testes)
- [⚙️ Decisões Técnicas](#️-decisões-técnicas)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🚧 Melhorias Futuras](#-melhorias-futuras)

---

# 📌 Sobre o Projeto

O **Olympus API** é uma API REST desenvolvida para servir como base backend de futuras aplicações voltadas ao gerenciamento e acompanhamento de exercícios físicos.

A plataforma permite:

- cadastro e autenticação de usuários
- gerenciamento de atividades físicas
- categorização por tipos de exercício
- histórico de atividades realizadas

A proposta é construir uma arquitetura escalável, segura e preparada para evolução futura.

---

# 🚀 Getting Started

## ⚙️ Pré-requisitos

- Git
- Python (≥ 3.10)
- pip
- MySQL

---

## 📥 Clonando o Repositório

```bash
git clone https://github.com/Jorgemiguelaviles/API-Olympus.git
cd API-Olympus
```

---

## 🔧 Configuração do Backend

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar ambiente

**Linux/Mac**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Rodar servidor

```bash
uvicorn main:app --reload
```

### Endpoints locais

API:

```bash
http://localhost:8000
```

Swagger:

```bash
http://localhost:8000/docs
```

---

## 🔐 Variáveis de Ambiente

Crie um `.env` com base no `.env.example`

```env
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
SECRET_KEY=
JWT_ALGORITHM=
JWT_EXPIRE_MINUTES=
```

---

# 🔄 Fluxo da Aplicação

A API gerencia:

- autenticação de usuários
- cadastro de atividades físicas
- associação de atividades por categoria/tag
- registro de atividades executadas
- consulta de histórico

---

# 🏗 Arquitetura da Aplicação

O projeto utiliza **Layered Architecture**.

## Camadas

1. Presentation
2. Application
3. Domain
4. Infrastructure
5. Testing

Essa separação permite:

- baixo acoplamento
- alta manutenibilidade
- facilidade para testes
- escalabilidade

---

# 🛠 Tecnologias Utilizadas

## Backend

- FastAPI
- Python
- Pydantic
- SQLAlchemy
- JWT
- MySQL
- Pytest

---

# 🧪 Estratégia de Testes

## Objetivos

- evitar regressões
- validar regras de negócio
- garantir integridade da API

## Cobertura esperada

- ≥ 90%

## Tipos de testes

- testes unitários
- testes de integração
- validação de endpoints

---

# ⚙️ Decisões Técnicas

## FastAPI

Escolhido por:

- alta performance
- documentação automática
- tipagem forte
- excelente integração com Pydantic

## MySQL

Escolhido por:

- confiabilidade
- consistência transacional
- ampla adoção no mercado

## JWT

Escolhido para:

- autenticação stateless
- segurança
- escalabilidade

---

# 📁 Estrutura do Projeto

```bash
API-Olympus/
├── backend/
└── docs/
```

---

## Backend

```bash
backend/
├── .venv/
├── .env
├── main.py
├── src/
│   ├── config/
│   ├── controllers/
│   ├── interfaces/
│   ├── middlewares/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   └── validators/
└── tests/
```

---

## Responsabilidades

### `config/`

Configurações globais:

- banco de dados
- JWT
- ambiente

---

### `controllers/`

Controla o fluxo das requisições HTTP.

---

### `models/`

Entidades e representação do banco.

---

### `repositories/`

Responsável pelo acesso aos dados.

---

### `services/`

Contém a lógica de negócio.

---

### `middlewares/`

Interceptação e segurança.

---

### `routes/`

Definição dos endpoints.

---

### `validators/`

Validações e regras de entrada.

---

### `tests/`

Testes automatizados da aplicação.

---

# 🚧 Melhorias Futuras

- refresh token
- OAuth2
- rate limiting
- cache com Redis
- containerização com Docker
- CI/CD com GitHub Actions
- deploy na AWS

---