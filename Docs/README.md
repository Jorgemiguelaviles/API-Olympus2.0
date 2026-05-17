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
- [🧐 Exemplos de Uso](#-exemplos-de-uso)
- [🚧 Melhorias Futuras](#-melhorias-futuras)
- [🔮 Pontos de Observação](#-pontos-de-observação)

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
git clone https://github.com/Jorgemiguelaviles/API-Olympus2.0.git
cd API-Olympus2.0/backend
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
```

---

# 🔄 Fluxo da Aplicação

A API gerencia:

- autenticação de usuários (será adicionado na versão 2.0)
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
- JWT (adicionado na versão 2.0)
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

## JWT (versão 2.0)

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
│   ├── middlewares/ (será adicionado na versão 2.0)
│   ├── models/
│   ├── assets/
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
- JWT (será adicionado na versão 2.0)

---

### `controllers/`

Controla o fluxo das requisições HTTP.

---

### `models/`

Entidades e representação do banco.

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

# 🧐 Exemplos de Uso

### Recupera lista de atividades existentes
![alt text](image.png)

### Recupera lista de atividades execultadas
![alt text](image-2.png)


### Recupera lista de atividades execultadas por funcional
![alt text](image-1.png)


### Cadastra atividades execultadas




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

# 🔮 Pontos de Observação

- a API poderia contar com um sistema de login aonde camuflaria a funcional do usuario por meio de um JWT ou ainda usando um azure para assim a funcional vier camuflada
- poderiam se existir mais tipos de usuarios alem de mais informações sobre o mesmo, podendo essas infromações serem preenchidas de forma manual ou recuperadas por intermedio de uma API de email como a do google, hotmail....
- o usuario sendo do tipo root, semelhante ao que se encontra comentado, poderia ter outras atualizações, como caso o sistema vier ser comeercializado, desabilitando o mesmo atraves de pquenos comandos, ou podendo por exemplo criar outros tipos de esportes como calisthenics, skate....
- ainda nos dias atuais poderiamos fazer um monitoramento de forma mais aprofundada atraves dos comentarios dos usuarios podendo fazer uma analise por meio de IAs trazendo possiveis previsibilidades de resultdos futuros caso a pessoa continue seguindo um determinado ritmo
- na recuperação de lista de todas as atividade execultadas dependendo do caso poderia vim ter sido feita por meio de paginação
- no cadastro da atividade se pensarmos em um contexto geral poderia vir possuir numeros e letras, todavia no caso do case a unica verificação colocada foi garantir que a mesma fosse devidamente preenchida com validação de uma regex sndo composto por intermedio de 9 números

---