from city_explorer_agent.agent.coordinator import generate_city_response, test_single_tool


def main():
    print("🌍 도시 탐험 에이전트에 오신 것을 환영합니다!")
    print("탐험하고 싶은 도시명을 입력해주세요. (종료하려면 'quit' 또는 'exit' 입력)")
    print("테스트 명령어: 'test-tools' (도구 직접 테스트)")
    
    while True:
        try:
            # 사용자 입력 받기
            user_input = input("\n🏙️ 도시명: ").strip()
            
            # 종료 조건
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print("👋 도시 탐험을 마칩니다. 안녕히 가세요!")
                break
            
            # 테스트 모드
            if user_input.lower() == 'test-tools':
                test_single_tool()
                continue

            
            # 빈 입력 처리
            if not user_input:
                print("❌ 도시명을 입력해주세요.")
                continue
            
            # 단위 설정 (선택사항)
            units = 'metric'
            
            # AI 에이전트가 도구를 선택적으로 사용하여 가이드 생성
            response = generate_city_response(user_input, units=units)
            
            # 결과 출력
            print(f"\n🏙️ {user_input} 도시 가이드")
            print("=" * 60)
            print(response)
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")
            print("다시 시도해주세요.")


if __name__ == "__main__":
    main()