"""
Agent 생성을 위한 팩토리 함수들
"""
from strands import Agent
from strands.models.ollama import OllamaModel
from config import OLLAMA_HOST, STRANDS_MODEL

def create_ollama_model():
    """Ollama 모델 인스턴스 생성"""
    return OllamaModel(
        host=OLLAMA_HOST,
        model_id=STRANDS_MODEL
    )

def create_agent(system_prompt: str, tools=None, model=create_ollama_model()):
    """Agent 인스턴스 생성"""
    return Agent(
        model=model,
        tools=tools or [],
        system_prompt=system_prompt
    )