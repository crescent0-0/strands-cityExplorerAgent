import argparse
from city_explorer_agent.agent.coordinator import build_city_report

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True)
    p.add_argument("--units", default="metric")
    args = p.parse_args()

    report = build_city_report(args.city, units=args.units)
    # 보기 좋은 출력(임시)
    from pprint import pprint
    pprint(report.model_dump())