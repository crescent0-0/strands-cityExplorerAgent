from city_explorer_agent.models import Food
from city_explorer_agent.utils.cache import cached

TTL_FOOD = 60 * 60 * 24 * 90

@cached(lambda city: f"food:{city.lower()}", TTL_FOOD)
def food_tool(city: str) -> Food:
    # TODO: Wikidata/UNData/ 도시 공식 통계 API로 교체
    return Food(
        name="N/A",
        decs="N/A",
        source="N/A",
        source_url=None,
    )