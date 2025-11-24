from git import List
from pydantic import BaseModel, Field
from datetime import datetime

class VendaInsight(BaseModel):
    prato: str 
    horario_pico: datetime
    total_valor: float
    total_pedidos: int
    #embedding: List[float] = Field(default=..., description="Embedding vector for the venda insight")

class ReviewInsight(BaseModel):
    date: datetime = Field(..., description="Date of the review")
    is_positive: bool = Field(..., description="Indicates if the review is positive")
    comment: str = Field(..., description="Review comment")
    #embedding: List[float] = Field(default=..., description="Embedding vector for the review insight")


