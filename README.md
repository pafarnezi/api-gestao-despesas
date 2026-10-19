# 💸 API de Gestão de Despesas Pessoais

API REST completa de **CRUD de despesas pessoais**, desenvolvida com **FastAPI + SQLAlchemy + SQLite + Pytest**, com foco em simplicidade, testabilidade e documentação clara.

> 📌 **Nota do projeto:** Esta API foi gerada integralmente com auxílio de LLMs (especificação, decisões de arquitetura, código e testes), como solicitado na disciplina de Engenharia de Software. O objetivo é entregar um repositório público pronto para avaliação, com documentação caprichada.

---

## 📑 Índice

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Stack Tecnológica](#stack-tecnológica)
- [Arquitetura e Decisões (ADR)](#arquitetura-e-decisões-adr)
- [Especificação](#especificação)
- [Endpoints da API](#endpoints-da-api)
- [Modelo de Dados](#modelo-de-dados)
- [Como Executar Localmente](#como-executar-localmente)
- [Como Executar os Testes](#como-executar-os-testes)
- [Exemplos de Requisição (cURL)](#exemplos-de-requisição-curl)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Licença](#licença)

---

## 📖 Sobre

Uma API RESTful para cadastro, consulta, atualização e remoção de despesas pessoais. Ideal para quem quer controlar gastos do dia a dia por categoria, valor e descrição.

A persistência é feita em **SQLite** (arquivo local `despesas.db`), não exigindo instalação de banco de dados externo — basta rodar a API e testar.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| `CREATE` | Cadastrar nova despesa (descrição, valor, categoria) |
| `READ (lista)` | Listar todas as despesas com paginação (`skip`, `limit`) |
| `READ (detalhe)` | Consultar uma despesa específica pelo ID |
| `UPDATE` | Atualizar campos de uma despesa existente |
| `DELETE` | Remover uma despesa pelo ID |
| Validação | Campos obrigatórios e retorno 404 quando não encontrado |

---

## 🛠 Stack Tecnológica

- **Python 3.9+**
- [FastAPI](https://fastapi.tiangolo.com/) — framework web assíncrono e geração automática de docs (Swagger/OpenAPI)
- [SQLAlchemy 2.0](https://www.sqlalchemy.org/) — ORM para persistência
- [SQLite](https://www.sqlite.org/) — banco de dados em arquivo local (zero config)
- [Pydantic v2](https://docs.pydantic.dev/) — validação e serialização de dados
- [Pytest](https://docs.pytest.org/) + [TestClient](https://fastapi.tiangolo.com/tutorial/testing/) — testes de API
- `uvicorn` — servidor ASGI para desenvolvimento

---

## 🏗 Arquitetura e Decisões (ADR)

As principais decisões de arquitetura, incluindo a estratégia de testes, estão documentadas em [ADR_TESTES.md](./ADR_TESTES.md).

Resumo da decisão:
- **Testes de integração** contra a API real (via TestClient), validando endpoints de ponta a ponta (status codes, corpo da resposta e persistência).
- Banco de dados SQLite recriado a cada execução dos testes para garantir isolamento.
- Fixture de limpeza automática entre testes para evitar acoplamento de dados.

---

## 📄 Especificação

A especificação completa de requisitos (RFs, RNFs, fluxo, critérios de aceitação) está em [ESPECIFICACAO.md](./ESPECIFICACAO.md).

---

## 🔌 Endpoints da API

Base path: `http://localhost:8000`

| Método | Endpoint | Descrição | Status de sucesso |
|--------|----------|-----------|-------------------|
| `POST` | `/despesas/` | Cria uma nova despesa | `201 Created` |
| `GET` | `/despesas/` | Lista despesas (paginado) | `200 OK` |
| `GET` | `/despesas/{id}` | Obtém uma despesa por ID | `200 OK` |
| `PUT` | `/despesas/{id}` | Atualiza uma despesa existente | `200 OK` |
| `DELETE` | `/despesas/{id}` | Remove uma despesa por ID | `204 No Content` |

Quando um recurso não é encontrado, a API retorna **`404 Not Found`** com `{"detail": "Despesa não encontrada"}`.

A documentação interativa é gerada automaticamente pelo FastAPI em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## 🗄 Modelo de Dados

Tabela: **despesas**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `id` | Integer | Sim (PK) | Identificador único, autoincremento |
| `descricao` | String (200) | Sim | Descrição da despesa (ex: "Supermercado") |
| `valor` | Float | Sim | Valor gasto (ex: `145.90`) |
| `categoria` | String (100) | Sim | Categoria (ex: "Alimentação") |
| `data` | DateTime | Sim | Data/hora do registro (auto preenchido) |

---

## ▶️ Como Executar Localmente

### 1. Acesse a pasta do projeto

```bash
cd api-gestao-despesas
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`. Acesse `http://localhost:8000/docs` para testar os endpoints no navegador.

---

## 🧪 Como Executar os Testes

Os testes estão na pasta `tests/` e utilizam **Pytest + TestClient**.

```bash
pytest -v
```

O que os testes validam:
- ✅ Criação de despesa (status 201 e campos retornados)
- ✅ Listagem de despesas
- ✅ Consulta de despesa inexistente (404)
- ✅ Atualização de despesa existente
- ✅ Remoção de despesa e verificação de 404 após exclusão

---

## 🌐 Exemplos de Requisição (cURL)

### Criar despesa
```bash
curl -X POST "http://localhost:8000/despesas/" \
     -H "Content-Type: application/json" \
     -d '{"descricao":"Almoço","valor":35.50,"categoria":"Alimentação"}'
```

### Listar despesas
```bash
curl -X GET "http://localhost:8000/despesas/?skip=0&limit=10"
```

### Obter despesa por ID
```bash
curl -X GET "http://localhost:8000/despesas/1"
```

### Atualizar despesa
```bash
curl -X PUT "http://localhost:8000/despesas/1" \
     -H "Content-Type: application/json" \
     -d '{"descricao":"Jantar","valor":60.00,"categoria":"Alimentação"}'
```

### Remover despesa
```bash
curl -X DELETE "http://localhost:8000/despesas/1"
```

---

## 📂 Estrutura do Projeto

```
api-gestao-despesas/
├── README.md                 # Este arquivo (documentação principal)
├── ESPECIFICACAO.md          # Especificação de requisitos (RFs e RNFs)
├── ADR_TESTES.md             # Architecture Decision Record sobre testes
├── requirements.txt          # Dependências Python
├── .gitignore                # Arquivos ignorados pelo Git
├── app/
│   ├── __init__.py
│   ├── main.py               # App FastAPI e roteamento
│   ├── database.py           # Conexão SQLite e sessão
│   ├── models.py             # Modelos SQLAlchemy
│   ├── schemas.py            # Schemas Pydantic (entrada/saída)
│   ├── crud.py               # Operações de banco (CRUD)
│   └── routers/
│       ├── __init__.py
│       └── despesas.py       # Endpoints da API
└── tests/
    ├── __init__.py
    └── test_api.py           # Testes de integração da API
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar, estudar e modificar.

---

## 🤖 Sobre o uso de LLMs

Este repositório foi produzido com apoio de Modelos de Linguagem (LLMs), incluindo:
- Elaboração da especificação de requisitos
- Decisões de arquitetura registradas em ADR
- Implementação da API, modelos, schemas e rotas
- Criação dos testes automatizados
- Revisão e documentação do README

O código foi revisado, ajustado e testado para garantir funcionamento real antes da entrega.