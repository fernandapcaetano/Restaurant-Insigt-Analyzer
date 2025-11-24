from pydantic import BaseModel, Field
from typing import List, Optional


class InsightCausa(BaseModel):
    descricao: str = Field(..., description="Descrição da causa do insight")
    influencia: Optional[str] = Field(None, description="Descrição da influência da causa do insight")


class ProdutoLucro(BaseModel):
    produto: str = Field(..., description="Nome do produto")
    lucro: float = Field(..., description="Valor do lucro gerado pelo produto")
    motivo: str = Field(..., description="Motivo pelo qual o produto gera lucro")


class ClienteReclamacao(BaseModel):
    tipo: str = Field(..., description="Tipo de reclamação do cliente")
    quantidade: Optional[int] = Field(None, description="Quantidade de ocorrências da reclamação")


class AiInsightResumo(BaseModel):
    pontos_positivos: List[InsightCausa] = Field(..., description="Pontos bons e suas influências")
    pontos_negativos: List[InsightCausa] = Field(..., description="Pontos ruins e suas influências")
    produtos_que_ajudam_no_lucro: List[ProdutoLucro] = Field(..., description="Produtos que contribuem para o lucro")
    principais_reclamacoes: List[ClienteReclamacao] = Field(..., description="Principais reclamações dos clientes")