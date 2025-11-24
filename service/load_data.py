import datetime
import logging
import pandas as pd
from model.prato import Prato
from model.venda import Venda
from model.review import Review
from model.insight import ReviewInsight, VendaInsight
from typing import List
import os
from pathlib import Path
import re
logger = logging.getLogger(__name__)

class DataLoader:

    def __init__(self):
        base_path = os.getcwd()
        self.file_paths = {
            'pratos': os.path.join(base_path, 'resource\\menu.csv'),
            'vendas': os.path.join(base_path, 'resource\\venda.csv'),
            'reviews': os.path.join(base_path, 'resource\\reviews.csv')
        }

    def load_pratos(self) -> List[Prato]:
        df = pd.read_csv(self.file_paths['pratos'], sep=';')
        pratos = [Prato(**row.to_dict()) for index, row in df.iterrows()]
        return pratos

    def load_vendas(self) -> List[Venda]:
        df = pd.read_csv(self.file_paths['vendas'], sep=';')
        df['datetime'] = df['datetime'].apply(
            lambda x: datetime.datetime.strptime(x, '%d/%m/%Y %H:%M')
        )
        vendas = [Venda(**row.to_dict()) for index, row in df.iterrows()]
        return vendas

    def load_reviews(self) -> List[Review]:
        df = pd.read_csv(self.file_paths['reviews'], sep=';')
        df['datetime'] = df['datetime'].apply(
            lambda x: datetime.datetime.strptime(x, '%d/%m/%Y %H:%M')
        )
        df = df.rename(columns={
            'estrelas': 'rating',
            'comentario': 'comment'
        })
        reviews = [Review(**row.to_dict()) for index, row in df.iterrows()]
        return reviews
    
    def categorize_venda_by_prato(self, vendas: List[Venda], pratos: List[Prato]) -> List[VendaInsight]:

        prato_dict = {prato.nome: prato for prato in pratos}
        agrupado = {}
        for venda in vendas:
            nome_prato = venda.prato
            prato = prato_dict.get(nome_prato)

            if not prato:
                logger.warning(f"Prato '{nome_prato}' não encontrado.")
                continue

            if nome_prato not in agrupado:
                agrupado[nome_prato] = {
                    "total_valor": 0.0,
                    "total_pedidos": 0,
                    "horarios": []
                }

            agrupado[nome_prato]["total_valor"] += prato.preco * venda.quantidade
            agrupado[nome_prato]["total_pedidos"] += venda.quantidade

            agrupado[nome_prato]["horarios"].append(venda.datetime)

        insights = []

        for nome_prato, dados in agrupado.items():

            horas = [
                dt.replace(minute=0, second=0, microsecond=0)
                for dt in dados["horarios"]
            ]

            horario_pico = max(set(horas), key=horas.count) if horas else None

            insight = VendaInsight(
                prato=nome_prato,
                horario_pico=horario_pico,
                total_valor=dados["total_valor"],
                total_pedidos=dados["total_pedidos"],
                embedding=[]
            )

            insights.append(insight)

        return insights

    def categorize_reviews(self, reviews: List[Review]) -> List[ReviewInsight]:
        insights = []
        for review in reviews:
            is_positive = review.rating >= 3
            insight = ReviewInsight(
                date=review.datetime,
                is_positive=is_positive,
                comment=review.comment,
                embedding=[]
            )
            insights.append(insight)
        return insights


def format_insight_sections(data):

    formatted = {
        "pontos_positivos": [],
        "pontos_negativos": [],
        "produtos_lucro": [],
        "reclamacoes": []
    }

    # --- Pontos Positivos ---
    for item in data.get("pontos_positivos", []):
        formatted["pontos_positivos"].append({
            "titulo": item.get("descricao", ""),
            "detalhe": item.get("influencia", "")
        })

    # --- Pontos Negativos ---
    for item in data.get("pontos_negativos", []):
        formatted["pontos_negativos"].append({
            "titulo": item.get("descricao", ""),
            "detalhe": item.get("influencia", "")
        })

    # --- Produtos que Ajudam no Lucro ---
    for item in data.get("produtos_que_ajudam_no_lucro", []):
        formatted["produtos_lucro"].append({
            "titulo": f"{item.get('produto', '')} — R$ {item.get('lucro', 0)}",
            "detalhe": item.get("motivo", "")
        })

    # --- Reclamações ---
    for item in data.get("principais_reclamacoes", []):
        formatted["reclamacoes"].append({
            "titulo": f"{item.get('tipo', '')}",
            "detalhe": f"{item.get('quantidade', 0)} ocorrência(s)"
        })

    return formatted

