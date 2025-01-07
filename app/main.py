from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from . import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость для получения сессии базы данных
def get_db():
    """
        Создает и возвращает сессию базы данных.

        Yields:
            Session: Объект SQLAlchemy Session, который следует использовать для
            взаимодействия с базой данных.
        """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/wallets/{wallet_uuid}/operation")
def perform_operation(wallet_uuid: str, operation: schemas.Operation, db: Session = Depends(get_db)):
    """
    Выполняет операцию (пополнение или снятие средств) для указанного кошелька.
    Типы операций:
    DEPOSIT - пополнение
    WITHDRAW - снятие

    Args:
        wallet_uuid (str): Уникальный идентификатор кошелька, для которого
        выполняется операция.
        operation (schemas.Operation): Данные о операции, включая тип операции
        и сумму.
        db (Session, optional): Объект сессии базы данных, переданный автоматически
        через зависимость.

    Returns:
        dict: Словарь с уникальным идентификатором кошелька и новым балансом.

    Raises:
        HTTPException: Если кошелек не найден или если операция невозможна
        (например, недостаточно средств).
    """
    return crud.perform_operation(db, wallet_uuid, operation)

@app.get("/api/v1/wallets/{wallet_uuid}")
def get_balance(wallet_uuid: str, db: Session = Depends(get_db)):
    """
    Получает текущий баланс указанного кошелька.

    Args:
        wallet_uuid (str): Уникальный идентификатор кошелька.

        db (Session, optional): Объект сессии базы данных, переданный автоматически
        через зависимость.

    Returns:
        dict: Словарь с уникальным идентификатором кошелька и его текущим балансом.

    Raises:
        HTTPException: Если кошелек не найден в базе данных.
    """
    balance = crud.get_wallet_balance(db, wallet_uuid)
    if balance is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"wallet_uuid": wallet_uuid, "balance": balance}