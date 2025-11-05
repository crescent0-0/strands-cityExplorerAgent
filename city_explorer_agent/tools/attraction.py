from city_explorer_agent.models import Attraction
from city_explorer_agent.utils.cache import cached

TTL_ATTRACTION = 60 * 60 * 24 * 90

@cached(lambda city: f"attraction:{city.lower()}", TTL_ATTRACTION)
def attraction_tool(city: str) -> Attraction:
    # TODO: Wikidata/도시 공식 API로 교체
    return Attraction(
        name="N/A",
        decs="N/A",
        source="N/A",
        source_url=None,
    )