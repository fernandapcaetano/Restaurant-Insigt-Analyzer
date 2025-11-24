from model.agent_insight import AiInsightResumo
from service.load_data import DataLoader
from service.agent import Agent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting data loading process...")
data_loader = DataLoader()

logger.info("Loading pratos data...")
pratos = data_loader.load_pratos()
logger.info("Loading vendas data...")
vendas = data_loader.load_vendas()
logger.info("Loading reviews data...")
reviews = data_loader.load_reviews()

logger.info("Categorizing vendas by prato...")
categorizado_vendas = data_loader.categorize_venda_by_prato(vendas, pratos)
logger.info("Categorizing reviews...")
categorizado_reviews = data_loader.categorize_reviews(reviews)

logger.info("Generating general insights...")
agent = Agent()
logger.info("Generating general insights with agent...")
insight = agent.generate_general_insight(categorizado_reviews, categorizado_vendas)
logger.info("Insight generated successfully.")