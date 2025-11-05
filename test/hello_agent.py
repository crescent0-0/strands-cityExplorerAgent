from core.agent_factory import create_agent
from strands import tool
from strands_tools import calculator

# Tool 등록 방법
@tool
def weather():
    """ Get Weather """
    return "흐림"


# agent 설정
agent = create_agent(
    system_prompt="너는 한국어로 친절히 답하며, 간단한 수학 계산과 날씨를 알려줄 수 있는 어시스턴트야.",
    tools=[weather, calculator]
)

# 질의 및 답변 출력
def hello(question: str):
    print("질의: ", question)
    print(agent(question))