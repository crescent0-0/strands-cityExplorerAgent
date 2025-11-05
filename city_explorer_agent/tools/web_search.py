from typing import Dict
from city_explorer_agent.utils.cache import cached

@cached(lambda q: f"search:{q}", 60 * 60)
def web_search_tool(query:str) -> Dict[str,str]:
    #  TODO SerpSAPI/ Tavily / 커스텀 크롤러 연결 후 {label: url} 반환
    return {}