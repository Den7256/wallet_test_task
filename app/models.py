from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Wallet(Base):
    """
       Модель базы данных, представляющая кошелек.

       Атрибуты:
           id (str): Уникальный идентификатор кошелька (первичный ключ).
           balance (float): Текущий баланс кошелька, по умолчанию равен 0.0.
       """
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, index=True)
    balance = Column(Float, default=0.0)