from fastapi import FastAPI

from app.database import engine, Base
from app.routers import despesas

# Cria as tabelas no banco SQLite ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestão de Despesas Pessoais",
    description="CRUD completo para cadastro, consulta, atualização e remoção de despesas pessoais.",
    version="1.0.0",
    contact={
        "name": "Engenharia de Software",
        "url": "https://github.com/seu-usuario/api-gestao-despesas",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(despesas.router, prefix="/despesas", tags=["despesas"])


@app.get("/", tags=["root"])
def root():
    return {"message": "Bem-vindo à API de Gestão de Despesas Pessoais. Acesse /docs para a documentação interativa."}