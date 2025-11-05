import os
import requests
from typing import Optional
from datetime import date
from geopy.geocoders import Nominatim
from strands import tool
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
        # 단위
    units = (units or weather_data.get("units") or "standard").lower()
    temp_unit = {"metric": "°C", "imperial": "°F"}.get(units, "K")
    speed_unit = "mph" if units == "imperial" else "m/s"

    # 값 뽑기 (직접 접근)
    t = weather_data.get("temperature", {}) or {}
    h = weather_data.get("humidity", {}) or {}
    c = weather_data.get("cloud_cover", {}) or {}
    p = weather_data.get("precipitation", {}) or {}
    w = weather_data.get("wind", {}) or {}
    wmax = (w.get("max") or {})

    t_min_k  = t.get("min")
    t_max_k  = t.get("max")
    t_pm_k   = t.get("afternoon")
    t_morn_k = t.get("morning")
    t_eve_k  = t.get("evening")
    t_night_k= t.get("night")

    humidity = h.get("afternoon")
    cloud    = c.get("afternoon")
    precip   = p.get("total")
    wind_spd = wmax.get("speed")
    wind_dir = wmax.get("direction")

    # 온도 변환 (입력은 Kelvin 가정)
    def conv(k):
        if k is None: return None
        if units == "metric":
            return k - 273.15
        if units == "imperial":
            return (k - 273.15) * 9/5 + 32
        return k  # standard(K)

    t_min  = conv(t_min_k)
    t_max  = conv(t_max_k)
    t_pm   = conv(t_pm_k)
    t_morn = conv(t_morn_k)
    t_eve  = conv(t_eve_k)
    t_night= conv(t_night_k)

    # 풍향(도 → 16방위, 필요 없으면 지워도 됨)
    def compass(deg):
        if deg is None: return ""
        dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
                "S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return dirs[int((deg % 360) / 22.5 + 0.5) % 16]

    # 문장 만들기 (있는 값은 그대로 출력)
    parts = []
    if t_pm is not None:
        parts.append(f"오후 {t_pm:.1f}{temp_unit}")
    if t_min is not None and t_max is not None:
        parts.append(f"(최저 {t_min:.1f}·최고 {t_max:.1f}{temp_unit})")
    if t_morn is not None:
        parts.append(f"아침 {t_morn:.1f}{temp_unit}")
    if t_eve is not None:
        parts.append(f"저녁 {t_eve:.1f}{temp_unit}")
    if t_night is not None:
        parts.append(f"밤 {t_night:.1f}{temp_unit}")
    if humidity is not None:
        parts.append(f"습도 {humidity:.0f}%")
    if cloud is not None:
        parts.append(f"구름 {cloud:.0f}%")
    if precip is not None:
        parts.append(f"강수 {precip:.1f}mm")
    if wind_spd is not None:
        wd = compass(wind_dir)
        parts.append(f"바람 {wind_spd:.1f}{speed_unit}" + (f" {wd}" if wd else ""))

    return ", ".join(parts) if parts else "날씨 정보를 불러올 수 없습니다."



@tool(description="도시의 날씨 정보를 조회합니다")
def weather_tool(city: str, units: str = "metric") -> Weather:
    """
    OpenWeatherMap API를 사용하여 도시의 현재 날씨와 5일 예보를 가져옵니다.
    
    Args:
        city: 도시명 (예: "Seoul", "Tokyo", "New York")
        units: 단위 시스템 ("metric" for Celsius, "imperial" for Fahrenheit)
    
    Returns:
        Weather: 현재 날씨와 예보 정보
    """
    print(f"🔧 weather_tool 실행 중... (도시: {city}, 단위: {units})")
    
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
        
        result = Weather(
            now=current_weather,
            source="OpenWeatherMap",
            source_url=f"https://openweathermap.org/city/{current_data.get('id', '')}"
        )
        
        print(f"✅ 날씨 정보: {result.now if result.now else 'N/A'}")
        return result
        
    except requests.exceptions.RequestException as e:
        print("⚠️ 날씨 정보를 가져오는 중 네트워크 오류가 발생했습니다")
        return Weather(
            now=f"날씨 정보를 가져오는 중 네트워크 오류가 발생했습니다: {str(e)}",
            source="Network Error",
            source_url=None
        )
    except requests.exceptions.HTTPError as e:
        if "401" in str(e):
            print("⚠️ 잘못된 API 키입니다")
            return Weather(
                now="잘못된 API 키입니다. WEATHER_API_KEY를 확인해주세요.",
                source="Authentication Error",
                source_url="https://openweathermap.org/api"
            )
        elif "404" in str(e):
            print(f"⚠️ '{city}' 도시를 찾을 수 없습니다")
            return Weather(
                now=f"'{city}' 도시를 찾을 수 없습니다. 도시명을 확인해주세요.",
                source="City Not Found",
                source_url=None
            )
        else:
            print("⚠️ 날씨 API 오류가 발생했습니다")
            return Weather(
                now=f"날씨 API 오류: {str(e)}",
                source="API Error",
                source_url=None
            )
    except Exception as e:
        print("⚠️ 예상치 못한 오류가 발생했습니다")
        return Weather(
            now=f"예상치 못한 오류가 발생했습니다: {str(e)}",
            source="Unknown Error",
            source_url=None
        )