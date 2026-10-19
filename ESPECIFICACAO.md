# 📄 Especificação — API de Gestão de Despesas Pessoais

> **Disciplina:** Engenharia de Software  
> **Status:** Versão 1.0  
> **Produto:** API REST de CRUD para cadastro de despesas pessoais  
> **Nota:** Este documento foi elaborado com auxílio de LLMs, conforme demanda da disciplina.

---

## 1. Introdução

Este documento especifica os requisitos, o escopo, os endpoints e o modelo de dados de uma API REST para gestão de despesas pessoais. A aplicação permite ao usuário cadastrar, listar, consultar, atualizar e remover despesas do dia a dia, classificadas por descrição, valor e categoria.

---

## 2. Objetivo

Fornecer uma interface programável simples e funcional para controle financeiro pessoal, servindo como projeto acadêmico de demonstração de desenvolvimento de API com boas práticas de documentação, versionamento e testes.

---

## 3. Escopo

### 3.1 Inclui

- Cadastro de novas despesas.
- Listagem paginada de todas as despesas.
- Consulta de despesa por identificador.
- Atualização total de campos de uma despesa existente.
- Remoção de despesa por identificador.
- Documentação interativa automática (Swagger/OpenAPI) via FastAPI.
- Testes automatizados de integração cobrindo o ciclo completo de CRUD.
- Persistência em banco de dados SQLite local (sem dependência de servidor externo).

### 3.2 Não inclui (fora do escopo v1)

- Autenticação e autorização de usuários (login, JWT, roles).
- Categorias pré-cadastradas ou gerenciamento de categorias.
- Relatórios financeiros, gráficos ou exportação (CSV/PDF).
- Integração com bancos ou cartões de crédito.
- Frontend/web interface.

---

## 4. Requisitos Funcionais (RF)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF01 | O sistema deve permitir cadastrar uma despesa com descrição, valor e categoria. | Alta |
| RF02 | O sistema deve listar todas as despesas cadastradas, com suporte a paginação (`skip` e `limit`). | Alta |
| RF03 | O sistema deve retornar os detalhes de uma despesa específica informando seu ID. | Alta |
| RF04 | O sistema deve permitir atualizar descrição, valor e categoria de uma despesa existente. | Alta |
| RF05 | O sistema deve permitir excluir uma despesa informando seu ID. | Alta |
| RF06 | O sistema deve retornar erro `404 Not Found` quando a despesa solicitada não existir. | Média |
| RF07 | A API deve expor documentação interativa automática em `/docs` e `/redoc`. | Média |

---

## 5. Requisitos Não Funcionais (RNF)

| ID | Requisito | Detalhe |
|----|-----------|---------|
| RNF01 | Desempenho | Endpoints devem responder em média abaixo de 200 ms para cargas locais. |
| RNF02 | Portabilidade | Executar em qualquer máquina com Python 3.9+ sem instalação de banco externo. |
| RNF03 | Manutenibilidade | Código organizado em camadas (rotas, CRUD, modelos, schemas) e documentado. |
| RNF04 | Testabilidade | Cobertura dos principais fluxos de CRUD com testes automatizados. |
| RNF05 | Observabilidade | Logs de erro claros e respostas HTTP semânticas (200, 201, 204, 404). |

---

## 6. Endpoints da API

Todos os caminhos estão sob o prefixo `/despesas`.

| Método | Endpoint | Descrição | Corpo da requisição | Resposta de sucesso |
|--------|----------|-----------|---------------------|---------------------|
| `POST` | `/despesas/` | Cria uma nova despesa | `{ descricao, valor, categoria }` | `201 Created` + objeto da despesa |
| `GET` | `/despesas/` | Lista despesas (paginado) | Query: `skip`, `limit` | `200 OK` + lista de despesas |
| `GET` | `/despesas/{id}` | Obtém despesa por ID | — | `200 OK` + objeto da despesa |
| `PUT` | `/despesas/{id}` | Atualiza despesa existente | `{ descricao, valor, categoria }` | `200 OK` + objeto atualizado |
| `DELETE` | `/despesas/{id}` | Remove despesa por ID | — | `204 No Content` |

---

## 7. Modelo de Dados

Tabela **despesas**:

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id` | Integer | PK, autoincremento | Identificador único |
| `descricao` | String(200) | NOT NULL | Texto descritivo da despesa |
| `valor` | Float | NOT NULL | Valor monetário gasto |
| `categoria` | String(100) | NOT NULL | Categoria da despesa |
| `data` | DateTime | NOT NULL, default agora | Data/hora do cadastro |

---

## 8. Fluxo de Trabalho (Casos de Uso)

1. **Cadastrar despesa:** Usuário envia `POST /despesas/` com JSON válido → API valida, persiste e retorna a despesa com `id` gerado e `data`.
2. **Listar despesas:** Usuário envia `GET /despesas/` → API retorna lista paginada.
3. **Consultar despesa:** Usuário envia `GET /despesas/{id}` → API retorna a despesa ou `404` se não existir.
4. **Atualizar despesa:** Usuário envia `PUT /despesas/{id}` com novos dados → API atualiza e retorna o objeto modificado.
5. **Excluir despesa:** Usuário envia `DELETE /despesas/{id}` → API remove o registro e retorna `204`.

---

## 9. Stack Tecnológica

- **Linguagem:** Python 3.9+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Banco:** SQLite (arquivo local `despesas.db`)
- **Validação/Serialização:** Pydantic v2
- **Testes:** Pytest + FastAPI TestClient
- **Servidor:** Uvicorn

---

## 10. Critérios de Aceitação

- [ ] Cadastrar despesa retorna `201` com os campos preenchidos e `id` gerado.
- [ ] Listar despesas retorna `200` e uma lista (mesmo que vazia).
- [ ] Consultar despesa inexistente retorna `404`.
- [ ] Atualizar despesa existente retorna `200` com os novos valores refletidos.
- [ ] Deletar despesa existente retorna `204`; consulta posterior retorna `404`.
- [ ] Documentação Swagger disponível em `/docs`.
- [ ] Testes automatizados passam (`pytest` verde).

---

## 11. Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Sem autenticação | Escopo acadêmico v1; adicionar auth em versão futura. |
| Banco em arquivo local | Adequado para demonstração; não recomendado para produção concorrente. |
| Dados de teste persistem | Fixture de limpeza entre testes no Pytest. |

---

## 12. Apêndice — Exemplo de Payload

**Requisição (POST /despesas/):**
```json
{
  "descricao": "Supermercado",
  "valor": 145.90,
  "categoria": "Alimentação"
}
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "descricao": "Supermercado",
  "valor": 145.9,
  "categoria": "Alimentação",
  "data": "2026-10-18T22:30:00"
}
```