from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.DespesaResponse, status_code=201, tags=["despesas"])
def criar_despesa(despesa: schemas.DespesaCreate, db: Session = Depends(get_db)):
    return crud.create_despesa(db=db, despesa=despesa)


@router.get("/", response_model=list[schemas.DespesaResponse], tags=["despesas"])
def listar_despesas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_despesas(db=db, skip=skip, limit=limit)


@router.get("/{despesa_id}", response_model=schemas.DespesaResponse, tags=["despesas"])
def obter_despesa(despesa_id: int, db: Session = Depends(get_db)):
    db_despesa = crud.get_despesa(db=db, despesa_id=despesa_id)
    if not db_despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return db_despesa


@router.put("/{despesa_id}", response_model=schemas.DespesaResponse, tags=["despesas"])
def atualizar_despesa(
    despesa_id: int, despesa: schemas.DespesaCreate, db: Session = Depends(get_db)
):
    db_despesa = crud.update_despesa(db=db, despesa_id=despesa_id, despesa=despesa)
    if not db_despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return db_despesa


@router.delete("/{despesa_id}", status_code=204, tags=["despesas"])
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    db_despesa = crud.delete_despesa(db=db, despesa_id=despesa_id)
    if not db_despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return None