import os
import requests
from typing import Optional
from datetime import date
from geopy.geocoders import Nominatim
from city_explorer_agent.models import Weather
from city_explorer_agent.utils.cache import cached

TTL_WEATHER = 60 * 60 * 6  # 6시간 캐시 (날씨는 자주 변하므로)


def get_lat_lon(city: str) -> Optional[tuple[float, float]]:
    """도시 이름을 받아 위도와 경도를 반환"""
    geolocoder = Nominatim(user_agent="city_explorer_agent", timeout=None)
    geo = geolocoder.geocode(city)

    if geo:
        return geo.latitude, geo.longitude

    return None


def get_weather_description(weather_data: dict, units: str) -> str:
    """날씨 데이터를 사람이 읽기 쉬운 형태로 변환"""
    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"
    
    main = weather_data.get("main", {})
    weather = weather_data.get("weather", [{}])[0]
    wind = weather_data.get("wind", {})
    
    temp = main.get("temp", 0)
    feels_like = main.get("feels_like", 0)
    humidity = main.get("humidity", 0)
    description = weather.get("description", "").title()
    wind_speed = wind.get("speed", 0)
    
    return f"{description}, {temp:.1f}{temp_unit} (체감 {feels_like:.1f}{temp_unit}), 습도 {humidity}%, 바람 {wind_speed:.1f}{speed_unit}"



@cached(lambda city, units="metric": f"weather:{city.lower()}:{units}", TTL_WEATHER)
def weather_tool(city: str, units: str = "metric") -> Weather:
    """
    OpenWeatherMap API를 사용하여 도시의 현재 날씨와 5일 예보를 가져옵니다.
    
    Args:
        city: 도시명 (예: "Seoul", "Tokyo", "New York")
        units: 단위 시스템 ("metric" for Celsius, "imperial" for Fahrenheit)
    
    Returns:
        Weather: 현재 날씨와 예보 정보
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        return Weather(
            now="날씨 API 키가 설정되지 않았습니다. .env 파일에 WEATHER_API_KEY를 설정해주세요.",
            next_days=["OpenWeatherMap API 키가 필요합니다: https://openweathermap.org/api"],
            source="Configuration Error",
            source_url="https://openweathermap.org/api"
        )
    
    try:
        # 도시의 위도,경도 가져오기
        city_lat, city_lon = get_lat_lon(city)
        
        # 오늘 날씨 가져오기
        current_url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary"
        current_params = {
            "lat": city_lat,
            "lon": city_lon,
            "date": date.today(),
            "appid": api_key,
            "lang": "kr"  # 한국어 설명
        }
        
        current_response = requests.get(current_url, params=current_params, timeout=10)
        current_response.raise_for_status()
        current_data = current_response.json()
        
        
        # 현재 날씨 정보 생성
        current_weather = get_weather_description(current_data, units)
        
        
        return Weather(
            now=current_weather,
            next_days=daily_forecasts,
            source="OpenWeatherMap",
            source_url=f"https://openweathermap.org/city/{current_data.get('id', '')}"
        )
        
    except requests.exceptions.RequestException as e:
        return Weather(
            now=f"날씨 정보를 가져오는 중 네트워크 오류가 발생했습니다: {str(e)}",
            next_days=["인터넷 연결을 확인해주세요."],
            source="Network Error",
            source_url=None
        )
    except requests.exceptions.HTTPError as e:
        if "401" in str(e):
            return Weather(
                now="잘못된 API 키입니다. WEATHER_API_KEY를 확인해주세요.",
                next_days=["OpenWeatherMap에서 유효한 API 키를 발급받아주세요."],
                source="Authentication Error",
                source_url="https://openweathermap.org/api"
            )
        elif "404" in str(e):
            return Weather(
                now=f"'{city}' 도시를 찾을 수 없습니다. 도시명을 확인해주세요.",
                next_days=["해당 도시의 위도,경도 값이 올바른지 확인해주세요."],
                source="City Not Found",
                source_url=None
            )
        else:
            return Weather(
                now=f"날씨 API 오류: {str(e)}",
                next_days=["잠시 후 다시 시도해주세요."],
                source="API Error",
                source_url=None
            )
    except Exception as e:
        return Weather(
            now=f"예상치 못한 오류가 발생했습니다: {str(e)}",
            next_days=["개발자에게 문의해주세요."],
            source="Unknown Error",
            source_url=None
        )