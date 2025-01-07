from pydantic import BaseModel


class Operation(BaseModel):
    """
        Модель данных, представляющая операцию для кошелька.

        Атрибуты:
            operationType (str): Тип операции (например, 'DEPOSIT' или 'WITHDRAWAL').
            amount (float): Сумма, на которую производится операция.

        Конфигурация:
            schema_extra (dict): Пример данных для документации, показывающий
            ожидаемую структуру входных данных.
        """
    operationType: str
    amount: float

    class Config:
        schema_extra = {
            "example": {
                "operationType": "DEPOSIT",
                "amount": 1000
            }
        }