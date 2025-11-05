from city_explorer_agent.models import Weather
from city_explorer_agent.utils.cache import cached

TTL_WEATHER = 60 * 60 * 24 * 90

@cached(lambda city, units="metric": f"weather:{city.lower()}:{units}", TTL_WEATHER)
def weather_tool(city: str, units: str = "metric") -> Weather:
    # TODO: OpenWeather 등으로 교체
    return Weather(
        now=None,
        next_days=[],
        source="N/A",
        source_url=None
    )