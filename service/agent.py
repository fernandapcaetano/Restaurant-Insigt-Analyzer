from typing import List
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage
from model.insight import ReviewInsight, VendaInsight
from model.agent_insight import AiInsightResumo
from dotenv import load_dotenv
import json
import os
load_dotenv()

class Agent:

    def __init__(self):
        model_base_url = os.getenv("MODEL_BASE_URL")
        api_key = os.getenv("API_KEY")
        model_name = os.getenv("MODEL_NAME")
        model_embedding_name = os.getenv("MODEL_EMBEDDING_NAME")

        if not all([model_base_url, api_key, model_name, model_embedding_name]):
            raise ValueError("One or more environment variables are missing.")

        self.chat_model = ChatOpenAI(
            base_url=model_base_url,
            model=model_name,
            api_key=api_key,
        )
    
    def generate_general_insight(self, reviewInsight: List[ReviewInsight], vendaInsight: List[VendaInsight]) -> AiInsightResumo:
        schema_json = json.dumps(AiInsightResumo.model_json_schema(), indent=2)
        systemMessage = SystemMessage(content=f'''
            You are an expert data analyst. Provide a concise summary of the insights from the provided data.
            Response must be returned in the following format, do not add any additional text outside the format:
            {schema_json}                     
        ''')
        message = [
            systemMessage,
            HumanMessage(content=f"Based on the following venda insights: {json.dumps([i.model_dump(mode="json") for i in vendaInsight], indent=2, ensure_ascii=False)} and review insights: {json.dumps([i.model_dump(mode="json") for i in reviewInsight], indent=2, ensure_ascii=False)} generate a general insight summary.")
        ]
        response = self.chat_model.invoke(message)
        return AiInsightResumo.model_validate_json(response.content)