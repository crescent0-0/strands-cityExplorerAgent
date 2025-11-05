import requests
from typing import Optional
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
        
        print(sparql_query)
        response = requests.get(
            url, 
            params={"query": sparql_query, "format": "json"}, 
            headers=headers,
            timeout=10
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
        print(f"Wikidata SPARQL 오류: {e}")
        return None

def get_restcountries_population(city: str) -> Optional[Population]:
    """REST Countries API를 사용해 국가 인구를 가져옵니다 (도시가 수도인 경우)."""
    try:
        url = f"https://restcountries.com/v3.1/capital/{city}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                country = data[0]
                population = country.get("population")
                if population:
                    return Population(
                        value=population,
                        year=2023,  # REST Countries 데이터는 보통 최신
                        source="REST Countries API",
                        source_url=f"https://restcountries.com/v3.1/capital/{city}"
                    )
        return None
        
    except Exception as e:
        print(f"REST Countries API 오류: {e}")
        return None

@cached(lambda city: f"population:{city.lower()}", TTL_POPULATION)
def population_tool(city: str) -> Population:
    """도시 인구 정보를 여러 소스에서 가져옵니다."""
    
    # 1. Wikidata 시도
    result = get_wikidata_population(city)
    if result:
        return result
    
    # 2. REST Countries (수도인 경우) 시도
    result = get_restcountries_population(city)
    if result:
        return result
    
    # 3. 모든 방법 실패시 기본값
    return Population(
        value=None,
        year=None,
        source="N/A",
        source_url=None,
    )