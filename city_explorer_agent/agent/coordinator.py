import time
from strands import Agent
from core.agent_factory import create_agent
from city_explorer_agent.tools.population import population_tool
from city_explorer_agent.tools.weather import weather_tool
from city_explorer_agent.tools.attraction import attraction_tool
from city_explorer_agent.tools.food import food_tool
from city_explorer_agent.tools.transport import transport_tool
from city_explorer_agent.tools.web_search import web_search_tool
from city_explorer_agent.models import CityReport


def make_coordinator() -> Agent:
    agent = create_agent(
        system_prompt=(
            "도시 정보를 수집/요약한다. 인구, 날씨, 관광지, 음식, 교통을 다루며",
            "가능하면 공식 출처를 우선 사용하고, 실패 시 웹검색으로 보완한다.",
            "출처와 최신성을 명시하고, 사실이 불명확하면 'N/A'로 표시한다."
        ),
        tools=[
            population_tool, weather_tool, attraction_tool,
            food_tool, transport_tool, web_search_tool
        ]
    )
    return agent


def build_city_report(city: str, units: str ="metric") -> CityReport:
    # 수집
    population = population_tool(city)
    weather = weather_tool(city, units)
    attractions = attraction_tool(city)
    food = food_tool(city)
    transport = transport_tool(city)
    
    # 부족한 섹션은 웹 검색으로 보완
    sources = {}
    warnings = []
    if not population.value:
        sources |= web_search_tool(f"{city} population latest official statistics"); warnings.append("population from web_search")
    if not weather.now:
        sources |= web_search_tool(f"{city} current weather forecast"); warnings.append("weather from web_search")
    if not attractions:
        sources |= web_search_tool(f"top attractions in {city}"); warnings.append("attractions from web_search")
    if not food:
        sources |= web_search_tool(f"local foods in {city}"); warnings.append("food from web_search")
    if not transport.summary:
        sources |= web_search_tool(f"{city} public transport / airport / metro / pass"); warnings.append("transport from web_search")
    
    
    return CityReport(
        city=city,
        population=population,
        weather=weather,
        attractions=[attractions],
        foods=[food],
        transport=transport,
        sources=sources,
        metadata={"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "warnings": ";".join(warnings)}
    )
