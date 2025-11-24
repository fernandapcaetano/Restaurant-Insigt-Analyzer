from pydantic import BaseModel
from datetime import datetime

class Venda(BaseModel):
    datetime: datetime
    prato: str
    quantidade: int
    total_preco: float