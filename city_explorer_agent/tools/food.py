from strands import tool
from city_explorer_agent.models import Food
from city_explorer_agent.utils.cache import cached

TTL_FOOD = 60 * 60 * 24 * 90

@tool(description="도시의 지역 음식 정보를 조회합니다")
def food_tool(city: str) -> Food:
    """도시의 지역 음식 정보를 조회합니다"""
    
    print(f"🔧 food_tool 실행 중... (도시: {city})")
    
    # TODO: Wikidata/UNData/ 도시 공식 통계 API로 교체
    result = Food(
        name="N/A",
        decs="N/A",
        source="N/A",
        source_url=None,
    )
    
    print("⚠️ 음식 정보를 찾을 수 없습니다")
    return result