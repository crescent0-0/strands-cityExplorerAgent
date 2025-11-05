from strands import Agent
from strands_tools import calculator, current_time #, letter_counter

message = """
다음 4개의 질문에 답하세요.

1. 현재 서울 시간은 정확히 몇시 인가요??
2. 다음을 계산하세요 : 3111696 / 74088
3. 다음 단어에서 문자 'r'은 몇개인가요? : "strawberry"
4. 위 답변을 출력하는 스크립트를 작성하고, 결과값이 맞는지 검증하세요. (python tool을 사용하세요.)
"""

agent_no_tools = Agent()

agent_tools = Agent(tools=[calculator, current_time]) # , letter_counter


def compare():
    # (1) 도구 없는 에이전트
    print("## 단순 LLM 답변 (no tools)\n")
    print(agent_no_tools(message))
    
    # (2) 도구가 있는 에이전트
    print("\n" + "-"*80 + "\n")
    print("## Strand Agent (with tools)\n")
    print(agent_tools(message))