from strands import Agent
from core.agent_factory import create_agent
from city_explorer_agent.tools.population import population_tool
from city_explorer_agent.tools.weather import weather_tool
from city_explorer_agent.tools.attraction import attraction_tool
from city_explorer_agent.tools.food import food_tool
from city_explorer_agent.tools.transport import transport_tool
from city_explorer_agent.tools.web_search import web_search_tool


def create_city_explorer_agent() -> Agent:
    agent = create_agent(
        system_prompt=(
            "당신은 도시 정보 전문가입니다. 사용자가 요청한 도시에 대한 종합적인 여행 가이드를 작성해주세요.\n\n"
            "**중요: 반드시 제공된 도구들을 사용해서 실제 데이터를 수집해야 합니다. 자체 지식으로 답변하지 마세요.**\n\n"
            "주의사항:\n"
            "- 도구를 사용하지 않고 자체 지식으로 답변하는 것은 금지됩니다\n"
            "- 각 도구에서 반환된 실제 데이터만 사용하세요\n"
            "- 예외적으로, 각 도구에서 반환된 실제 데이터가 없는 경우, 자체 지식으로 답변하는 것을 허용하며, 이 때 자체 지식으로 답변중인 사실을 밝혀야합니다\n"
            "- 한국어로 친근하게 작성하고 이모지를 적절히 사용하세요"
        ),
        tools=[
            population_tool, weather_tool, attraction_tool,
            food_tool, transport_tool, web_search_tool
        ]
    )
    return agent



def generate_city_response(city: str, units: str = "metric") -> str:
    """LLM 에이전트가 필요한 도구를 선택적으로 사용하여 도시 가이드 생성"""
    
    print(f"🤖 AI 에이전트가 '{city}' 도시 정보 수집을 시작합니다...")
    print("-" * 50)
    print("🔍 AI가 필요한 도구들을 선택하여 정보를 수집합니다...")
    print("   (도구 사용 시 실시간으로 결과를 표시합니다)")
    
    # 도시 정보 수집 에이전트 생성
    city_explorer_agent = create_city_explorer_agent()
    
    # LLM에게 도시 정보 수집 요청
    prompt = f"""
        '{city}' 도시에 대한 종합적인 여행 가이드를 작성해주세요.

        각 도구에서 수집한 실제 데이터를 바탕으로 여행자에게 유용한 가이드를 작성해주세요.
        자체 지식을 사용하지 말고 오직 도구에서 반환된 데이터만 사용하세요.
    """
    
    # LLM이 도구를 사용하여 응답 생성
    response = city_explorer_agent(prompt)
    
    print("\n✅ AI 에이전트가 도시 가이드 작성을 완료했습니다!")
    print("-" * 50)
    
    return response


def test_single_tool():
    """단일 도구 테스트 및 디버깅"""
    print("=== 도구 직접 테스트 ===")
    
    city = "서울"
    
    # 도구 함수들의 타입 및 속성 확인
    print(f"population_tool 타입: {type(population_tool)}")
    print(f"population_tool.__name__: {getattr(population_tool, '__name__', 'N/A')}")
    print(f"population_tool 속성들: {[attr for attr in dir(population_tool) if not attr.startswith('_')]}")
    
    # @tool 데코레이터 관련 속성 확인
    if hasattr(population_tool, '__wrapped__'):
        print(f"population_tool.__wrapped__: {population_tool.__wrapped__}")
    if hasattr(population_tool, 'tool_name'):
        print(f"population_tool.tool_name: {population_tool.tool_name}")
    
    print(f"\n직접 population_tool 호출:")
    try:
        result = population_tool(city)
        print(f"결과: {result}")
    except Exception as e:
        print(f"오류: {e}")
    
    print(f"\n직접 weather_tool 호출:")
    try:
        result = weather_tool(city, "metric")
        print(f"결과: {result}")
    except Exception as e:
        print(f"오류: {e}")
    
    print("=== 테스트 완료 ===\n")

