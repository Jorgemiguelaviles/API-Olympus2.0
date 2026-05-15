![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)

# 📚 Sumário

- [📌 Sobre o Projeto](#-sobre-o-projeto)
- [🚀 Getting Started](#-getting-started)
  - [⚙️ Pré-requisitos](#️-pré-requisitos)
  - [📥 Clonando o Repositório](#-clonando-o-repositório)
  - [🔧 Configuração do Backend](#-configuração-do-backend)
  - [🎨 Configuração do Frontend](#-configuração-do-frontend)
  - [🔐 Variáveis de Ambiente](#-variáveis-de-ambiente)

- [🔄 Fluxo da Aplicação](#-fluxo-da-aplicação)
- [🏗 Arquitetura da Aplicação](#-arquitetura-da-aplicação)
- [🛠 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🎨 Estilização da Interface](#-estilização-da-interface)
- [🧪 Estratégia de Testes](#-estratégia-de-testes)
- [⚙️ Decisões Técnicas](#️-decisões-técnicas)
- [📁 Estrutura do Projeto](#-estrutura-geral-do-projeto)
- [🚧 Melhorias Futuras](#-melhorias-futuras)

---

# 📌 Sobre o Projeto

Este projeto simula o jogo **Mastermind (Senha)** como parte de um case técnico para o Itaú Unibanco.

A proposta é transformar a resolução do puzzle em uma experiência gamificada com estética **hacker/cyberpunk**, inspirada na era PlayStation 2.

O frontend segue princípios modernos:

- Componentização
- Tipagem forte
- Organização modular

> 💡 Sugestão: adicionar GIFs ou prints

```md
![Demo](caminho/para/demo.gif)
```

---

# 🚀 Getting Started

## ⚙️ Pré-requisitos

- Git
- Node.js (≥ 18)
- npm
- Python (≥ 3.10)
- pip
- MySQL

---

## 📥 Clonando o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
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

📍 API:

```
http://localhost:8000
```

📍 Docs:

```
http://localhost:8000/docs
```

---

## 🎨 Configuração do Frontend

```bash
cd frontend
npm install
ng serve
```

📍 App:

```
http://localhost:4200
```

---

## 🔐 Variáveis de Ambiente

Crie um `.env` baseado no `.env.example`

### Backend

```env
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
SECRET_KEY=
```

### Frontend

```ts
apiUrl: 'http://localhost:8000';
```

---

# 🔄 Fluxo da Aplicação

- Frontend → `localhost:4200`
- Backend → `localhost:8000`

A API gerencia:

- autenticação
- partidas
- ranking
- dashboards

---

# 🏗 Arquitetura da Aplicação

Arquitetura baseada em **Layered Architecture**:

### Camadas

1. Presentation
2. Application
3. Domain
4. Data
5. Testing

### Tecnologias

- Frontend: Angular
- Backend: FastAPI
- DB: MySQL
- Estilo: Tailwind
- Charts: Chart.js
- Testes: Jest + Pytest

---

# 🛠 Tecnologias Utilizadas

## Backend

- FastAPI
- JWT
- Pydantic
- Pytest
- MySQL

📌 Para visualizar todas as dependências utilizadas no backend, consulte o arquivo:

```bash
requirements.txt
```

---

## Frontend

- Angular
- TypeScript
- Tailwind CSS
- Jest

📌 Todas as dependências do frontend podem ser encontradas em:

```bash
node_modules/
```

> ⚠️ Observação: o diretório `node_modules` é gerado automaticamente após a execução do `npm install`.
> Para visualizar as dependências declaradas do projeto, consulte também o arquivo:

```bash
package.json
```

---

# 🎨 Estilização da Interface

Estilo **retro-hacker** com:

- fundo escuro
- alto contraste
- design minimalista

---

# 🧪 Estratégia de Testes

### Objetivos

- evitar regressões
- validar lógica
- garantir confiabilidade

### Cobertura

- ≥ 90%

### Tipos

- testes de componentes
- testes de lógica

---

# ⚙️ Decisões Técnicas

### Arquitetura Separada

- Frontend (Angular)
- Backend (FastAPI)

### API REST

- comunicação via JSON
- desacoplamento

### Banco

- MySQL

### Armazenamento

- imagens locais (simulando S3)

---

# 📁 Estrutura Geral do Projeto

```bash
mastermind/
├── frontend/
├── backend/
├── docs/
└── README.md
```

---

## Frontend

A estrutura do frontend segue os padrões do ecossistema Angular, priorizando organização, escalabilidade e reutilização de código.

### 📁 Estrutura Geral

```bash
frontend/
├── public/
│   ├── images/
│   └── favicon.ico
├── node_modules/
└── src/
    ├── environments/
    └── app/
        ├── core/
        │   ├── interceptors/
        │   ├── services/
        │   ├── guards/
        │   └── interfaces/
        ├── features/
        │   ├── dashboards/
        │   ├── home/
        │   ├── login/
        │   ├── mastermind/
        │   ├── ranking/
        │   └── regras/
        └── shared/
            ├── components/
            └── validators/
```

---

### 📦 Diretórios Principais

#### `public/`

Contém arquivos estáticos acessíveis diretamente pela aplicação:

- `images/` → imagens e assets visuais
- `favicon.ico` → ícone da aplicação no navegador

---

#### `node_modules/`

Gerado automaticamente pelo Node.js, armazena todas as dependências do projeto definidas no `package.json`.

---

#### `src/`

Diretório principal da aplicação Angular.

- `app/` → núcleo da aplicação
- `environments/` → configurações por ambiente (dev, prod)

---

### 🧠 Estrutura do `app/`

Organizada em três camadas principais:

#### `core/` (núcleo global)

Responsável por funcionalidades compartilhadas e críticas:

- `interceptors/` → manipulação de requisições HTTP (ex: JWT, erros)
- `services/` → comunicação com backend e lógica compartilhada
- `guards/` → controle de acesso às rotas
- `interfaces/` → tipagem e contratos de dados

---

#### `features/` (módulos da aplicação)

Cada feature representa uma funcionalidade isolada:

- `dashboards/` → gráficos e métricas
- `home/` → página inicial
- `login/` → autenticação
- `mastermind/` → lógica do jogo
- `ranking/` → classificação de jogadores
- `regras/` → instruções do jogo

Cada feature pode conter:

```bash
components/  # componentes específicos
pages/       # telas da feature
```

---

#### `shared/` (reutilização)

Componentes e utilidades compartilhadas:

- `components/` → botões, modais, cards, etc.
- `validators/` → validações customizadas

---

### 💡 Observações

- Estrutura modular facilita manutenção e escalabilidade
- Separação de responsabilidades evita acoplamento
- Reutilização reduz duplicação de código

---

## Backend

O backend segue uma arquitetura em camadas, separando responsabilidades entre API, lógica de negócio e acesso a dados.

---

### 📁 Estrutura Geral

```bash
backend/
├── .venv/
├── .env
├── main.py
├── src/
│   ├── assets/
│   ├── config/
│   ├── controllers/
│   ├── helpers/
│   ├── middlewares/
│   ├── models/
│   ├── interfaces/
│   ├── routes/
│   └── services/
│       ├── dashboard_service/
│       ├── game_service/
│       ├── login_service/
│       ├── validators/
│       └── request_services/
│           ├── request_dash/
│           ├── request_game/
│           └── request_auth/
└── tests/
    ├── controllers/
    ├── services/
    ├── routes/
    └── validators/
```

---

### 📦 Estrutura da Raiz

- `.venv/` → ambiente virtual Python
- `.env` → variáveis de ambiente
- `main.py` → ponto de entrada da API
- `src/` → código principal
- `tests/` → testes automatizados

---

### 🧠 Estrutura do `src/`

#### `assets/`

Armazena imagens dos usuários (simulando S3).

---

#### `config/`

Configurações do sistema e conexão com banco de dados.

---

#### `controllers/`

Orquestra as requisições:

- recebe chamadas
- direciona para services

---

#### `helpers/`

Funções auxiliares:

- geração de JWT
- validações gerais

---

#### `middlewares/`

Interceptação de requisições:

- autenticação
- validação

---

#### `models/`

Representação das entidades do banco.

---

#### `routes/`

routes/

Definição dos endpoints da API.

Documentação Swagger agora integrada via FastAPI.

Endpoint padrão:

http://localhost:8000/docs

---

### ⚙️ Camada `services/`

Responsável pela lógica de negócio:

- `dashboard_service/`
- `game_service/`
- `login_service/`
- `validators/`
- `request_services/`

---

### 🗄 `request_services/` (acesso ao banco)

- `request_dash/` → dashboards
- `request_game/` → partidas
- `request_auth/` → autenticação

---

### 🧪 Testes

A pasta `tests/` replica a estrutura principal:

- controllers
- services
- routes
- validators

---

### 💡 Observações

- Arquitetura desacoplada facilita testes
- Separação clara entre regra e persistência
- Estrutura preparada para escalar

---

# 🚧 Melhorias Futuras

- WebSockets (tempo real)
- OAuth (Google/GitHub)
- AWS S3
- recuperação de senha por email
- deploy na AWS

---
