from sqlalchemy.orm import Session

from app import models, schemas


def get_despesa(db: Session, despesa_id: int):
    return db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()


def get_despesas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Despesa).offset(skip).limit(limit).all()


def create_despesa(db: Session, despesa: schemas.DespesaCreate):
    db_despesa = models.Despesa(**despesa.model_dump())
    db.add(db_despesa)
    db.commit()
    db.refresh(db_despesa)
    return db_despesa


def update_despesa(db: Session, despesa_id: int, despesa: schemas.DespesaCreate):
    db_despesa = get_despesa(db, despesa_id)
    if db_despesa:
        for key, value in despesa.model_dump().items():
            setattr(db_despesa, key, value)
        db.commit()
        db.refresh(db_despesa)
    return db_despesa


def delete_despesa(db: Session, despesa_id: int):
    db_despesa = get_despesa(db, despesa_id)
    if db_despesa:
        db.delete(db_despesa)
        db.commit()
    return db_despesa