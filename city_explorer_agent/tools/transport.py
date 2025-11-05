from strands import tool
from city_explorer_agent.models import Transport
from city_explorer_agent.utils.cache import cached

TTL_TRANSPORT = 60 * 60 * 24 * 90

@tool(description="도시의 교통 정보를 조회합니다")
def transport_tool(city: str) -> Transport:
    """도시의 교통 정보를 조회합니다"""
    
    print(f"🔧 transport_tool 실행 중... (도시: {city})")
    
    # TODO: Wikidata/도시 공식 API로 교체
    result = Transport(
        summary="N/A",
        source="N/A",
        source_url=None,
    )
    
    print("⚠️ 교통 정보를 찾을 수 없습니다")
    return result