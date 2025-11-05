from typing import Dict
from strands import tool
from city_explorer_agent.utils.cache import cached

@tool(description="웹 검색을 통해 추가 정보를 조회합니다")
def web_search_tool(query: str) -> Dict[str, str]:
    """웹 검색을 통해 추가 정보를 조회합니다"""
    
    print(f"🔧 web_search_tool 실행 중... (검색어: {query})")
    
    #  TODO SerpSAPI/ Tavily / 커스텀 크롤러 연결 후 {label: url} 반환
    result = {}
    
    print("⚠️ 웹 검색 결과를 찾을 수 없습니다")
    return result