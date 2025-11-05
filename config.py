"""
환경변수 설정을 중앙화하는 모듈
"""
import os
from dotenv import load_dotenv

# 한 번만 로드
load_dotenv()

# 환경변수들을 상수로 정의
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
STRANDS_MODEL = os.getenv("STRANDS_MODEL", "deepseek-r1:8b")
STRANDS_MODEL_PROVIDER = os.getenv("STRANDS_MODEL_PROVIDER", "ollama")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 15))
REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", 3))

# 필요하면 검증 로직도 추가 가능
if not OLLAMA_HOST.startswith(('http://', 'https://')):
    raise ValueError("OLLAMA_HOST must be a valid URL")