from pydantic import BaseModel

class Prato(BaseModel):
    nome: str
    ingredientes: str
    preco: float