# 🏛️ ADR-001 — Estratégia de Testes da API de Despesas

| Campo | Valor |
|-------|-------|
| **Título** | Estratégia de Testes da API de Gestão de Despesas |
| **Status** | Aceito |
| **Data** | 18/10/2026 |
| **Autor** | Projeto gerado com auxílio de LLM |
| **Decisores** | Equipe de Engenharia de Software (docente + discentes) |

---

## 1. Contexto

Estamos desenvolvendo uma API REST de CRUD para despesas pessoais com FastAPI + SQLAlchemy + SQLite. Como parte dos requisitos da disciplina de Engenharia de Software, é necessário entregar testes automatizados que comprovem o funcionamento da API.

Precisamos decidir:
- Que tipo de testes escrever (unitário, integração, end-to-end).
- Quais ferramentas utilizar.
- Como garantir isolamento entre testes sem depender de banco externo.
- Qual nível de cobertura é suficiente para este escopo acadêmico.

---

## 2. Decisão

Adotar **testes de integração** contra a aplicação FastAPI real utilizando o **TestClient** do Starlette/FastAPI, com banco **SQLite em arquivo local** recriado a cada sessão de testes e limpeza automática de registros entre cada caso de teste via fixture do Pytest.

Não serão escritos testes unitários isolados de funções CRUD nem testes end-to-end com navegador, por escopo e complexidade do projeto.

---

## 3. Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da rejeição |
|-------------|------|---------|--------------------|
| **A. Testes unitários puros** (mock de sessão SQLAlchemy) | Rápidos, isolados | Não validam rotas, serialização, status HTTP nem integração real com o banco | Baixo valor para validar uma API REST |
| **B. Testes end-to-end com navegador (Selenium/Playwright)** | Valida a experiência completa | Muito pesado, lento, exige frontend, fora do escopo de uma API | Overkill para este projeto |
| **C. Testes de integração com TestClient + SQLite** (escolhido) | Valida endpoints reais, status codes, corpo JSON e persistência; simples e rápido | O banco compartilhado exige cuidado com isolamento | Atende aos requisitos com baixo custo |

---

## 4. Consequências

### Positivas
- Validação real dos 5 endpoints CRUD (status `200`, `201`, `204`, `404`).
- Detecção precoce de regressões em rotas, validação Pydantic e mapeamento ORM.
- Execução rápida (SQLite local, sem rede externa).
- Documentação viva de como a API deve se comportar.

### Negativas / Riscos
- Testes compartilham o mesmo arquivo de banco (`despesas.db`) se não houver limpeza; mitigado com fixture que limpa tabelas após cada teste.
- Não testam concorrência nem cargas pesadas (não é requisito do escopo v1).
- Não substituem testes de segurança/autenticação (fora do escopo v1).

---

## 5. Ferramentas

- **Pytest** — framework de execução e fixtures.
- **FastAPI TestClient** — cliente HTTP síncrono para chamar os endpoints da aplicação em memória.
- **SQLAlchemy** — ORM usada tanto na aplicação quanto nos testes para limpeza de tabelas.

---

## 6. Organização dos Testes

Arquivo: `tests/test_api.py`

Cada teste:
1. Usa fixture `client` que cria as tabelas no banco SQLite.
2. Executa uma requisição HTTP real contra a API.
3. Valida status code e campos do corpo JSON.
4. Ao final, a fixture limpa todas as linhas das tabelas, evitando acoplamento entre testes.

Exemplos de cenários cobertos:
- `test_criar_despesa` — criação com sucesso (`201`).
- `test_listar_despesas` — listagem retorna ao menos um item (`200`).
- `test_obter_despesa_nao_encontrada` — ID inexistente retorna `404`.
- `test_atualizar_despesa` — atualização reflete novos valores (`200`).
- `test_deletar_despesa` — exclusão retorna `204` e consulta seguinte retorna `404`.

---

## 7. Critério de Sucesso

```
pytest -v
```
Deve finalizar com **todos os testes passando (verde)** antes de qualquer entrega ou subida ao GitHub.

---

## 8. Referências

- [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest — Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [SQLAlchemy 2.0 — Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)