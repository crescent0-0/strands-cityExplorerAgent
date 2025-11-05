import requests
from typing import List
from city_explorer_agent.models import Attraction
from city_explorer_agent.utils.cache import cached

TTL_ATTRACTION = 60 * 60 * 24 * 90


def get_wikidata_attraction(city: str) -> List[Attraction]:
    """Wikidata SPARQL을 사용해 도시 관광지 정보를 가져옵니다."""
    try:

        # SPARQL 쿼리로 도시 인구 정보 검색
        sparql_query = f"""
        SELECT ?item ?itemLabel ?itemDescription ?sitelinks ?article ?coord ?qid
        WHERE {{
          {{ ?city rdfs:label "{city}"@en }}
            UNION
          {{ ?city rdfs:label "{city}"@ko }}
          BIND(STR(REPLACE(STR(?city), ".*/", "")) AS ?qid)

          ?item wdt:P131* ?city .
          ?item wdt:P31/wdt:P279* wd:Q570116 .

          OPTIONAL {{ ?item wikibase:sitelinks ?sitelinks . }}
          OPTIONAL {{
            ?article schema:about ?item ;
                     schema:isPartOf [ wikibase:wikiGroup "wikipedia" ] ;
                     schema:inLanguage "ko" .
          }}
          OPTIONAL {{ ?item wdt:P625 ?coord . }}

          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "ko,en" .
          }}
        }}
        ORDER BY DESC(?sitelinks)
        LIMIT 10
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
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            rows = data.get("results", {}).get("bindings", [])
            attractions: List[Attraction] = []
            
            for b in rows:
                name = b.get("itemLabel", {}).get("value", "") or ""
                desc = b.get("itemDescription", {}).get("value", "") or ""
                qid_item = b.get("item", {}).get("value", "").split("/")[-1]
                wd_url = f"https://www.wikidata.org/wiki/{qid_item}"
                article = b.get("article", {}).get("value")  # lang 위키백과가 있을 때 우선

                attractions.append(
                    Attraction(
                        name=name,
                        desc=desc,
                        source="Wikidata",
                        source_url=article or wd_url,
                    )
                )
                
            return attractions
        
        return []
        
    except Exception as e:
        print(f"Wikidata SPARQL 오류: {e}")
        return []



@cached(lambda city: f"attraction:{city.lower()}", TTL_ATTRACTION)
def attraction_tool(city: str) -> List[Attraction]:
    """도시 관광지 정보를 Wikidata SPARQL을 통해 가져옵니다."""
    
    # Wikidata 시도
    result = get_wikidata_attraction(city)
    if result:
        return result
    
    return [Attraction(
        name="N/A",
        desc="N/A",
        source="N/A",
        source_url=None,
    )]