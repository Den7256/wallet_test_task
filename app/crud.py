from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

def perform_operation(db: Session, wallet_uuid: str, operation: schemas.Operation):
    """
    Выполняет операцию (пополнение или снятие средств) для указанного кошелька.
    Типы операций:
    DEPOSIT - пополнение
    WITHDRAW - снятие

    Args:
        db (Session): SQLAlchemy сессия для взаимодействия с базой данных.
        wallet_uuid (str): Уникальный идентификатор кошелька.
        operation (schemas.Operation): Операция, которую нужно выполнить, включая тип операции и сумму.

    Raises:
        HTTPException: Если кошелек не найден, если недостаточно средств для снятия,
        или если указан неверный тип операции.

    Returns:
        dict: Словарь с уникальным идентификатором кошелька и новым балансом.
    """
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_uuid).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if operation.operationType == "DEPOSIT":
        wallet.balance += operation.amount
    elif operation.operationType == "WITHDRAW":
        if wallet.balance < operation.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        wallet.balance -= operation.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid operation type")

    db.commit()
    db.refresh(wallet)
    return {"wallet_uuid": wallet_uuid, "new_balance": wallet.balance}

def get_wallet_balance(db: Session, wallet_uuid: str):
    """
       Получает текущий баланс указанного кошелька.

       Args:
           db (Session): SQLAlchemy сессия для взаимодействия с базой данных.
           wallet_uuid (str): Уникальный идентификатор кошелька.

       Returns:
           float or None: Текущий баланс кошелька или None, если кошелек не найден.
       """
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_uuid).first()
    if wallet is None:
        return None
    return wallet.balance