from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# 인구
class Population(BaseModel):
    value: Optional[int] = None
    year: Optional[int] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    
# 날씨
class Weather(BaseModel):
    now: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    

# 관광지
class Attraction(BaseModel):
    name: str
    desc: str = ""
    source: Optional[str] = None
    source_url: Optional[str] = None
    
# 음식
class Food(BaseModel):
    name: str
    desc: str = ""
    source: Optional[str] = None
    source_url: Optional[str] = None
    
# 교통
class Transport(BaseModel):
    summary: str = ""
    source: Optional[str] = None
    source_url: Optional[str] = None
    
# 최종 결과
class CityReport(BaseModel):
    city: str
    population: Population
    weather: Weather
    attractions: List[Attraction]
    foods: List[Food]
    transport: Transport
    sources: Dict[str, str] = {}
    metadata: Dict[str, str] = {}