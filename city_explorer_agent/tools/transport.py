from city_explorer_agent.models import Transport
from city_explorer_agent.utils.cache import cached

TTL_TRANSPORT = 60 * 60 * 24 * 90

@cached(lambda city: f"Transport:{city.lower()}", TTL_TRANSPORT)
def transport_tool(city: str) -> Transport:
    # TODO: Wikidata/도시 공식 API로 교체
    return Transport(
        summary="N/A",
        source="N/A",
        source_url=None,
    )