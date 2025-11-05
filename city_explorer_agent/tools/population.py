import requests
from typing import Optional
from strands import tool
from city_explorer_agent.models import Population
from city_explorer_agent.utils.cache import cached

TTL_POPULATION = 60 * 60 * 24 * 90

def get_wikidata_population(city: str) -> Optional[Population]:
    """Wikidata SPARQL을 사용해 도시 인구 정보를 가져옵니다."""
    try:
        # SPARQL 쿼리로 도시 인구 정보 검색
        sparql_query = f"""
        SELECT ?city ?population ?year WHERE {{
          ?city rdfs:label "{city}"@en .
          ?city wdt:P1082 ?population .
          OPTIONAL {{ ?city p:P1082/pq:P585 ?year }}
        }}
        ORDER BY DESC(?year)
        LIMIT 1
        """
        
        url = "https://query.wikidata.org/sparql"
        headers = {
            "User-Agent": "CityExplorer/1.0 (https://example.com/contact)",
            "Accept": "application/json"
        }
        
        response = requests.get(
            url, 
            params={"query": sparql_query, "format": "json"}, 
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", {}).get("bindings", [])
            
            if results:
                result = results[0]
                population_value = int(result["population"]["value"])
                
                # 연도 추출 (있는 경우)
                year = None
                if "year" in result:
                    year_str = result["year"]["value"]
                    year = int(year_str[:4])  # 2020-01-01T00:00:00Z -> 2020
                
                return Population(
                    value=population_value,
                    year=year,
                    source="Wikidata",
                    source_url=f"https://www.wikidata.org/wiki/Special:Search/{city}"
                )
        
        return None
        
    except Exception as e:
        print(f"Wikidata SPARQL Population 오류: {e}")
        return None


# @cached(lambda city: f"population:{city.lower()}", TTL_POPULATION)
@tool(description="도시의 인구 정보를 조회합니다")
def population_tool(city: str) -> Population:
    """도시 인구 정보를 Wikidata SPARQL을 통해 가져옵니다."""
    
    print(f"🔧 population_tool 실행 중... (도시: {city})")
    
    # Wikidata 시도
    result = get_wikidata_population(city)
    if result:
        log_msg = f"✅ 인구 정보: {result.value if result.value else 'N/A'}"
        if result.source:
            log_msg += f" (출처: {result.source})"
        print(log_msg)
        return result

    # 실패시 기본값
    print("⚠️ 인구 정보를 찾을 수 없습니다")
    return Population(
        value=None,
        year=None,
        source="N/A",
        source_url=None,
    )