def generate_final_summary_detailed(pillars_char: Dict[str, str], basic_results: Dict[str, Any], life_flow: Dict[str, Any]) -> Dict[str, Any]:
    """종합 리포트 - 상세 버전"""
    
    # 각 분석에서 핵심 내용 추출
    day_gan = pillars_char.get('day_gan', '')
    day_ji = pillars_char.get('day_ji', '')
    ilju_key = f"{day_gan}{day_ji}"
    
    # 십성 분석에서 핵심 특성 추출
    sipsung_raw = basic_results.get('sipsung_raw', {})
    sipsung_list = list(sipsung_raw.values())
    gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")
    jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")
    siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")
    
    # 성격 유형 결정
    personality_type = ""
    if gwanseong_count > 1:
        personality_type = "리더십형"
    elif jaeseong_count > 1:
        personality_type = "경제형"
    elif siksang_count > 1:
        personality_type = "창의형"
    else:
        personality_type = "균형형"
    
    analysis_text = f"""
【종합 리포트】

20년 역술가의 관점에서 당신의 사주를 종합적으로 분석한 결과입니다.
이 리포트는 당신의 인생 전반에 걸친 운세와 특성을 상세히 분석하여,
더 나은 미래를 위한 길잡이가 되고자 합니다.

【사주 기본 정보】

▣ 일주: {ilju_key}
▣ 사주 구성: {pillars_char.get('year_gan', '')}{pillars_char.get('year_ji', '')}년 {pillars_char.get('month_gan', '')}{pillars_char.get('month_ji', '')}월 {day_gan}{day_ji}일 {pillars_char.get('hour_gan', '')}{pillars_char.get('hour_ji', '')}시
▣ 성격 유형: {personality_type}

【핵심 분석 요약】

1. 성격적 특징
   당신의 사주는 {ilju_key} 일주의 특성을 기본으로 하여 독특한 성격을 형성합니다.
   특히 {personality_type}의 특성이 강하게 나타나며, 이는 당신의 인생에서 큰 강점이 됩니다.

2. 대인관계 분석
   사주에서 나타나는 십성과 운성의 조합을 보면,
   특히 {'강한 리더십과 통솔력을 가진' if gwanseong_count > 0 else '자유롭고 독립적인'} 사람들과 잘 어울립니다.
   또한 귀인 분석에 따르면 인생의 각 시기마다 도움을 주는 사람들이 나타납니다.

3. 직업적 성향
   일주의 특성과 십성의 조합을 고려할 때,
   {'관리직이나 리더십을 발휘하는' if gwanseong_count > 0 else '창의적이고 전문적인' if siksang_count > 0 else '안정적이고 실무적인'} 분야가 적합합니다.
   재물운 분석에 따르면 {'사업가적 재능이 뛰어나' if jaeseong_count > 0 and siksang_count > 0 else '안정적인 수입을 통해' if jaeseong_count == 0 else '지혜롭게 재물을 관리하며'} 부를 축적할 수 있습니다.

4. 운세의 흐름
   십이운성의 조합을 보면, 특정 시기의 기운이 강하게 나타나는 시기가 있으며,
   특히 현재 진행 중인 대운에서는 중요한 변화와 기회가 예상됩니다.
   향후 5년간의 세운 분석에 따르면, 특히 주의가 필요한 시기와 적극적으로 활동해야 할 시기가 구분됩니다.

5. 사랑과 결혼
   연애운 분석에 따르면 {'열정적이고 활발한' if gwanseong_count > 0 and jaeseong_count > 0 else '진지하고 안정적인' if gwanseong_count > 0 else '자유롭고 독립적인' if jaeseong_count > 0 else '조용하고 깊이 있는'} 연애를 선호합니다.
   운명의 짝은 당신의 부족한 부분을 보완해주는 사람일 가능성이 높습니다.

6. 건강 관리
   건강운 분석에 따르면 {'활발한 신진대사를 가지고 있으나 과로에 주의' if siksang_count > 2 else '안정적인 체질을 가지고 있으나 꾸준한 관리가 필요' if siksang_count == 0 else '균형잡힌 건강 상태를 유지'}하고 있습니다.
   특히 {day_gan}의 오행 특성상 {'간과 담낭' if day_gan in ['甲', '乙'] else '심장과 소장' if day_gan in ['丙', '丁'] else '비장과 위장' if day_gan in ['戊', '己'] else '폐와 대장' if day_gan in ['庚', '辛'] else '신장과 방광'} 건강에 주의가 필요합니다.

【전문가 권장사항】

1. 성격 개발
   • 강점 활용: 당신의 {personality_type} 특성을 최대한 활용하세요.
   • 약점 보완: 특히 {'독선적이 되기 쉽다' if gwanseong_count > 2 else '우유부단한 면이 있다' if gwanseong_count == 0 else '균형을 유지해야 한다'}는 점을 주의하세요.
   • 성장 방향: 당신의 일주 특성을 기반으로 지속적인 자기계발을 하세요.

2. 대인관계 관리
   • 적합한 관계: {'협력적이고 지원적인' if personality_type == '균형형' else '독립적이고 창의적인' if personality_type == '창의형' else '책임감 있고 신뢰할 수 있는'} 사람들과의 관계를 중시하세요.
   • 갈등 해결: 특히 대운이 바뀌는 시기에는 대인관계에 특별히 주의하세요.
   • 귀인 활용: 각 시기에 나타나는 귀인을 소중히 여기고 감사하는 마음을 가지세요.

3. 직업적 발전
   • 적합한 분야: {'경영, 관리, 행정' if gwanseong_count > 0 else '예술, 교육, 컨설팅' if siksang_count > 0 else '사무, 금융, 부동산'} 분야를 고려하세요.
   • 발전 방향: {'사업가적 마인드로 독립' if jaeseong_count > 0 and siksang_count > 0 else '조직 내에서의 승진' if gwanseong_count > 0 else '전문성을 키워 프리랜서로'}하는 방향을 모색하세요.
   • 재물 관리: 재물운의 특성을 고려하여 적절한 투자와 저축 계획을 세우세요.

4. 운세 활용
   • 긍정적 시기: 특히 현재 진행 중인 대운의 기운을 최대한 활용하세요.
   • 주의 시기: 삼재가 예상되는 시기를 미리 대비하고 신중히 행동하세요.
   • 기회 포착: 매년 변화하는 세운의 특성을 파악하여 적절히 대응하세요.
   • 장기 계획: 대운의 큰 흐름을 이해하고 10년 단위의 장기 계획을 세우세요.

5. 사랑과 가정
   • 연애 전략: 당신의 연애 스타일을 이해하고 상대방을 배려하는 자세를 가지세요.
   • 결혼 생활: 서로의 차이를 인정하고 존중하는 관계를 유지하세요.
   • 개선 노력: 연애운 분석에서 제시된 개선점을 지속적으로 노력하세요.

6. 건강 유지
   • 체질 관리: 당신의 타고난 체질을 이해하고 그에 맞는 건강 관리를 하세요.
   • 예방 주의: 특히 약한 부분으로 지적된 신체 부위를 주의 깊게 관리하세요.
   • 운동 선택: 당신에게 적합한 운동을 꾸준히 실천하세요.
   • 오행 균형: 일간의 오행 특성에 맞는 음식과 생활습관을 유지하세요.

【미래 전망】

당신의 사주를 종합적으로 분석한 결과, 특별한 재능과 가능성을 가지고 있습니다.
특히 {personality_type}의 특성을 잘 활용한다면 크게 성공할 수 있을 것입니다.

향후 5년간은 당신에게 있어 중요한 전환점이 될 것으로 보입니다.
특히 현재 진행 중인 대운의 기운을 잘 활용하고,
매년 변화하는 세운의 흐름을 파악하여 대응한다면
더 큰 성공과 행복을 이룰 수 있을 것입니다.

인생은 정해진 운명이 아니라, 자신의 노력과 선택으로 만들어가는 것입니다.
사주는 당신의 타고난 특성과 가능성을 보여주는 나침반일 뿐,
어떻게 활용하고 발전시키는가는 전적으로 당신의 몸에 달려 있습니다.

【마무리 말씀】

이상의 분석은 20년 역술가의 경험을 바탕으로 한 전문적인 해석입니다.

당신의 사주는 특별한 장점과 가능성을 가지고 있으며,
이를 잘 파악하고 활용한다면 분명 크게 성공할 수 있을 것입니다.

가장 중요한 것은 자신을 믿고, 긍정적인 마인드로 인생을 살아가는 것입니다.
사주에서 제시된 길은 하나의 가이드라인일 뿐,
당신의 선택과 노력이 더 나은 미래를 만들어 갈 것입니다.

행복하고 성공적인 인생을 살아가시길 진심으로 기원합니다.

- 20년 경력의 역술가 올림 -
"""
    
    return {
        "title": "종합 리포트",
        "content": analysis_text.strip()
    }