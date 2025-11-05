from strands_tools import calculator, current_time
from agent_factory import create_agent

# agent 설정
agent = create_agent(
    system_prompt="도구를 적절히 사용해서 정확히 계산하고, 시간을 알려줄래?",
    tools=[calculator, current_time]
)

# 질의 및 답변 출력
print(agent("144의 제곱근을 구해서 알려줄래? 그리고 한국을 기준으로 현재 시간도 같이 알려줘."))
