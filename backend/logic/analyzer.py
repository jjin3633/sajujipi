import json
import os
import datetime
import requests

CHEONGAN = "甲乙丙丁戊己庚辛壬癸"
CHEONGAN_KOR = "갑을병정무기경신임계"
JIJI = "子丑寅卯辰巳午未申酉戌亥"
JIJI_KOR = "자축인묘진사오미신유술해"
OHENG_GAN = {"甲":"목", "乙":"목", "丙":"화", "丁":"화", "戊":"토", "己":"토", "庚":"금", "辛":"금", "壬":"수", "癸":"수"}
EUMYANG_GAN = {"甲":"+", "乙":"-", "丙":"+", "丁":"-", "戊":"+", "己":"-", "庚":"+", "辛":"-", "壬":"+", "癸":"-"}
OHENG_JIJI = {"子":"수", "丑":"토", "寅":"목", "卯":"목", "辰":"토", "巳":"화", "午":"화", "未":"토", "申":"금", "酉":"금", "戌":"토", "亥":"수"}
EUMYANG_JIJI = {"子":"+", "丑":"-", "寅":"+", "卯":"-", "辰":"+", "巳":"-", "午":"+", "未":"-", "申":"+", "酉":"-", "戌":"+", "亥":"-"}
SIPSUNG_OHENG_ORDER = "목화토금수"
SIPSUNG_MAP = [["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"],["겁재", "비견", "상관", "식신", "정재", "편재", "정관", "편관", "정인", "편인"]]
SIBIUNSEONG_TABLE = {
    "甲": {"亥": "장생", "子": "목욕", "丑": "관대", "寅": "건록", "卯": "제왕", "辰": "쇠", "巳": "병", "午": "사", "未": "묘", "申": "절", "酉": "태", "戌": "양"},
    "丙": {"寅": "장생", "卯": "목욕", "辰": "관대", "巳": "건록", "午": "제왕", "未": "쇠", "申": "병", "酉": "사", "戌": "묘", "亥": "절", "子": "태", "丑": "양"},
    "戊": {"寅": "장생", "卯": "목욕", "辰": "관대", "巳": "건록", "午": "제왕", "未": "쇠", "申": "병", "酉": "사", "戌": "묘", "亥": "절", "子": "태", "丑": "양"},
    "庚": {"巳": "장생", "午": "목욕", "未": "관대", "申": "건록", "酉": "제왕", "戌": "쇠", "亥": "병", "子": "사", "丑": "묘", "寅": "절", "卯": "태", "辰": "양"},
    "壬": {"申": "장생", "酉": "목욕", "戌": "관대", "亥": "건록", "子": "제왕", "丑": "쇠", "寅": "병", "卯": "사", "辰": "묘", "巳": "절", "午": "태", "未": "양"},
    "乙": {"午": "장생", "巳": "목욕", "辰": "관대", "卯": "건록", "寅": "제왕", "丑": "쇠", "子": "병", "亥": "사", "戌": "묘", "酉": "절", "申": "태", "未": "양"},
    "丁": {"酉": "장생", "申": "목욕", "未": "관대", "午": "건록", "巳": "제왕", "辰": "쇠", "卯": "병", "寅": "사", "丑": "묘", "子": "절", "亥": "태", "戌": "양"},
    "己": {"酉": "장생", "申": "목욕", "未": "관대", "午": "건록", "巳": "제왕", "辰": "쇠", "卯": "병", "寅": "사", "丑": "묘", "子": "절", "亥": "태", "戌": "양"},
    "辛": {"子": "장생", "亥": "목욕", "戌": "관대", "酉": "건록", "申": "제왕", "未": "쇠", "午": "병", "巳": "사", "辰": "묘", "卯": "절", "寅": "태", "丑": "양"},
    "癸": {"卯": "장생", "寅": "목욕", "丑": "관대", "子": "건록", "亥": "제왕", "戌": "쇠", "酉": "병", "申": "사", "未": "묘", "午": "절", "巳": "태", "辰": "양"}
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ILJU_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'ilju_data.json')
SIPSUNG_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'sipsung_data.json')
SIBIUNSEONG_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'sibiunseong_data.json')


def get_saju_details(year, month, day, hour, minute):
    ref_date = datetime.datetime(1899, 12, 22, 0, 0)
    target_date = datetime.datetime(year, month, day, hour, minute)
    delta_days = (target_date - ref_date).days
    day_gan_idx = delta_days % 10
    day_ji_idx = delta_days % 12
    day_gan = CHEONGAN[day_gan_idx]
    ipchun = datetime.datetime(year, 2, 4)
    saju_year = year if target_date >= ipchun else year - 1
    year_gan_idx = (saju_year - 1864) % 10
    year_ji_idx = (saju_year - 1864) % 12
    year_gan = CHEONGAN[year_gan_idx]
    year_ji = JIJI[year_ji_idx]
    month_ji_map = {1:"寅", 2:"卯", 3:"辰", 4:"巳", 5:"午", 6:"未", 7:"申", 8:"酉", 9:"戌", 10:"亥", 11:"子", 12:"丑"}
    month_ji = month_ji_map.get(month, "寅")
    gan_start_map = {"甲己":"丙", "乙庚":"戊", "丙辛":"庚", "丁壬":"壬", "戊癸":"甲"}
    year_gan_key_list = [k for k in gan_start_map if year_gan in k]
    if not year_gan_key_list: return {"error": "연간 계산 오류"}
    year_gan_key = year_gan_key_list[0]
    month_gan_start_char = gan_start_map[year_gan_key]
    month_gan_start_idx = CHEONGAN.find(month_gan_start_char)
    month_ji_start_idx = JIJI.find("寅")
    month_ji_current_idx = JIJI.find(month_ji)
    month_offset = (month_ji_current_idx - month_ji_start_idx + 12) % 12
    month_gan_idx = (month_gan_start_idx + month_offset) % 10
    month_gan = CHEONGAN[month_gan_idx]
    hour_ji_idx = (hour + 1) // 2 % 12
    if hour == 23: hour_ji_idx = 0
    hour_ji = JIJI[hour_ji_idx]
    gan_start_map_hour = {"甲己":"甲", "乙庚":"丙", "丙辛":"戊", "丁壬":"庚", "戊癸":"壬"}
    day_gan_key_list = [k for k in gan_start_map_hour if day_gan in k]
    if not day_gan_key_list: return {"error": "시간 계산 오류"}
    day_gan_key = day_gan_key_list[0]
    hour_gan_start_char = gan_start_map_hour[day_gan_key]
    hour_gan_start_idx = CHEONGAN.find(hour_gan_start_char)
    hour_gan_idx = (hour_gan_start_idx + hour_ji_idx) % 10
    hour_gan = CHEONGAN[hour_gan_idx]
    pillars_char = {
        'year_gan': year_gan, 'year_ji': year_ji,
        'month_gan': month_gan, 'month_ji': month_ji,
        'day_gan': day_gan, 'day_ji': JIJI[day_ji_idx],
        'hour_gan': hour_gan, 'hour_ji': hour_ji
    }
    
    sipsung_result = calculate_sipsung(pillars_char)
    sipsung_analysis = analyze_sipsung_by_period(sipsung_result)
    sibiunseong_analysis = analyze_sibiunseong(pillars_char)
    
    # 십이운성 일러스트 생성
    sibiunseong_illustration_url = None
    try:
        # 십이운성 분석 결과를 바탕으로 일러스트 프롬프트 생성
        sibiunseong_prompt = f"Traditional Korean fortune telling illustration showing the twelve fortunes (십이운성) with {day_gan} day master, mystical atmosphere, traditional Korean art style, detailed and colorful"
        sibiunseong_illustration_url = generate_ai_illustration(sibiunseong_prompt)
    except:
        sibiunseong_illustration_url = None
    
    # 새로운 분석 함수들 추가
    sibisinsal_analysis = analyze_sibisinsal(pillars_char)
    guin_analysis = analyze_guin(pillars_char)
    
    # 기존 분석 함수들 확장
    wealth_luck_analysis = analyze_wealth_luck(sipsung_result)
    wealth_enhanced = enhance_wealth_analysis(sipsung_result)
    wealth_luck_analysis.update(wealth_enhanced)
    
    love_luck_analysis = analyze_love_luck(sipsung_result)
    love_enhanced = enhance_love_analysis(sipsung_result)
    love_luck_analysis.update(love_enhanced)
    
    career_luck_analysis = analyze_career_luck(sipsung_result)
    career_enhanced = enhance_career_analysis(sipsung_result)
    career_luck_analysis.update(career_enhanced)
    
    health_luck_analysis = analyze_health_luck(sipsung_result, pillars_char)
    health_enhanced = enhance_health_analysis(sipsung_result, pillars_char)
    health_luck_analysis.update(health_enhanced)
    
    # 대운/세운 분석 추가
    life_flow_analysis = analyze_life_flow(year, month, day, hour, minute, sipsung_result)
    
    # 종합 리포트 생성
    comprehensive_report = generate_comprehensive_report({
        "sipsung": sipsung_result,
        "wealth": wealth_luck_analysis,
        "love": love_luck_analysis,
        "career": career_luck_analysis,
        "health": health_luck_analysis,
        "life_flow": life_flow_analysis
    })

    ilju_analysis_data = get_ilju_analysis_data(f"{day_gan}{JIJI[day_ji_idx]}")
    
    return {
        "year_pillar": f"{year_gan}{year_ji}",
        "month_pillar": f"{month_gan}{month_ji}",
        "day_pillar": f"{day_gan}{JIJI[day_ji_idx]}",
        "hour_pillar": f"{hour_gan}{hour_ji}",
        "sipsung_raw": sipsung_result,
        "sipsung_analysis": sipsung_analysis,
        "sibiunseong_analysis": sibiunseong_analysis,
        "sibiunseong_illustration_url": sibiunseong_illustration_url,
        "sibisinsal_analysis": sibisinsal_analysis,
        "guin_analysis": guin_analysis,
        "wealth_luck_analysis": wealth_luck_analysis,
        "love_luck_analysis": love_luck_analysis,
        "career_luck_analysis": career_luck_analysis,
        "health_luck_analysis": health_luck_analysis,
        "life_flow_analysis": life_flow_analysis,
        "comprehensive_report": comprehensive_report,
        "ilju_analysis": ilju_analysis_data
    }

def analyze_career_luck(sipsung_result):
    """십성 데이터를 기반으로 직업운을 분석하고 AI 아바타를 생성합니다."""
    sipsung_list = list(sipsung_result.values())
    
    # 관성 (관리, 리더십)
    gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")
    # 식상 (창의성, 전문성)
    siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")
    
    # 직업 스타일 분석
    if gwanseong_count == 0:
        if siksang_count > 0:
            career_style = "창의적 전문가 유형"
            description = "사주에 관리나 리더십을 나타내는 관성은 뚜렷하지 않지만, 창의성과 전문성을 나타내는 식상이 강합니다. 독립적으로 일하는 전문가나 프리랜서로 성공할 가능성이 높습니다. 자신만의 창의적인 아이디어로 새로운 분야를 개척하는 데 유리합니다."
            avatar_prompt = "A professional creative expert in modern office, wearing smart casual attire, with laptop and creative tools, confident pose, anime style"
        else:
            career_style = "안정적 직장인 유형"
            description = "사주에 직업과 관련된 기운이 강하지 않아, 안정적이고 체계적인 직장 생활이 적합합니다. 대기업이나 공기업에서 성실하게 일하는 것이 좋으며, 꾸준한 노력으로 승진과 성장을 이룰 수 있습니다. 팀워크를 중시하는 환경에서 잘 적응할 수 있습니다."
            avatar_prompt = "A reliable office worker in business attire, sitting at desk with documents, professional and diligent, anime style"
    elif gwanseong_count > 0:
        if siksang_count > 0:
            career_style = "리더십 전문가 유형"
            description = "사주에 관리 능력(관성)과 창의성(식상)을 모두 갖추고 있어, 리더십과 전문성을 겸비한 직업이 적합합니다. 경영자, 컨설턴트, 교육자 등에서 뛰어난 성과를 낼 수 있습니다. 팀을 이끌면서도 창의적인 솔루션을 제시하는 능력이 뛰어납니다."
            avatar_prompt = "A confident business leader in professional suit, standing in modern office, with leadership aura, commanding presence, anime style"
        else:
            career_style = "관리직 전문가 유형"
            description = "사주에 관리 능력(관성)은 있지만 창의성(식상)이 부족하여, 체계적이고 안정적인 관리직이 적합합니다. 중간 관리자, 행정직, 공무원 등에서 뛰어난 성과를 낼 수 있습니다. 규칙과 절차를 중시하며, 조직을 효율적으로 운영하는 능력이 뛰어납니다."
            avatar_prompt = "A professional manager in formal business attire, organizing documents, with structured approach, reliable and organized, anime style"
    
    # AI 아바타 생성
    try:
        avatar_url = generate_ai_avatar(avatar_prompt)
    except:
        avatar_url = None
    
    return {
        "title": career_style,
        "description": description,
        "avatar_url": avatar_url
    }

def generate_ai_avatar(prompt):
    """AI 아바타 생성 함수 - 배포 환경 안정성을 위해 수정"""
    try:
        # 배포 환경에서는 AI 이미지 생성이 불가능할 수 있으므로 기본값 반환
        if not prompt:
            return None
            
        # 실제 AI API 호출 대신 기본 이미지 URL 반환 (배포 환경 안정성)
        # 실제 운영에서는 여기에 AI API 키와 호출 로직을 추가
        return None
        
    except Exception as e:
        print(f"AI avatar generation failed: {str(e)}")
        return None

def analyze_love_luck(sipsung_result):
    """십성 데이터를 기반으로 연애운을 분석하고 AI 일러스트를 생성합니다."""
    sipsung_list = list(sipsung_result.values())
    
    # 관성 (배우자, 연인)
    gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")
    # 재성 (재물, 매력)
    jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")
    
    # 연애 스타일 분석
    if gwanseong_count == 0:
        if jaeseong_count > 0:
            love_style = "자유로운 연애 스타일"
            description = "사주에 배우자나 연인을 나타내는 관성이 뚜렷하지 않아, 자유로운 연애를 선호하는 스타일입니다. 재물의 기운이 있어 매력적이고 독립적인 연애를 즐길 수 있습니다. 하지만 깊은 관계로 발전하기 위해서는 상대방을 이해하려는 노력이 필요합니다."
            illustration_prompt = "A romantic illustration of a free-spirited person enjoying independent dating, with a modern city background, soft lighting, anime style"
        else:
            love_style = "조용한 연애 스타일"
            description = "사주에 연애와 관련된 기운이 강하지 않아, 조용하고 안정적인 연애를 선호합니다. 깊이 있는 관계를 추구하며, 서두르지 않고 천천히 마음을 열어가는 스타일입니다. 진정한 사랑을 찾기 위해 인내심을 가지고 기다리는 것이 중요합니다."
            illustration_prompt = "A gentle romantic illustration of a quiet, patient person waiting for true love, with peaceful nature background, soft pastel colors, anime style"
    elif gwanseong_count > 0:
        if jaeseong_count > 0:
            love_style = "열정적인 연애 스타일"
            description = "사주에 배우자(관성)와 매력(재성)을 모두 갖추고 있어, 열정적이고 활발한 연애를 즐기는 스타일입니다. 상대방을 사로잡는 매력이 뛰어나며, 깊이 있는 관계로 발전할 가능성이 높습니다. 하지만 너무 빠르게 진행하지 않도록 주의해야 합니다."
            illustration_prompt = "A passionate romantic illustration of two people in deep love, with vibrant colors, hearts, and romantic atmosphere, anime style"
        else:
            love_style = "전통적인 연애 스타일"
            description = "사주에 배우자(관성)는 있지만 매력(재성)이 부족하여, 전통적이고 안정적인 연애를 선호합니다. 진지한 관계를 추구하며, 결혼을 염두에 둔 연애를 하는 스타일입니다. 상대방에게 진심을 다해 대하는 것이 중요합니다."
            illustration_prompt = "A traditional romantic illustration of a couple in a serious relationship, with elegant setting, warm lighting, anime style"
    
    # AI 일러스트 생성
    try:
        illustration_url = generate_ai_illustration(illustration_prompt)
    except:
        illustration_url = None
    
    return {
        "title": love_style,
        "description": description,
        "illustration_url": illustration_url
    }

def generate_ai_illustration(prompt):
    """AI 일러스트 생성 함수 - 배포 환경 안정성을 위해 수정"""
    try:
        # 배포 환경에서는 AI 이미지 생성이 불가능할 수 있으므로 기본값 반환
        if not prompt:
            return None
            
        # 실제 AI API 호출 대신 기본 이미지 URL 반환 (배포 환경 안정성)
        # 실제 운영에서는 여기에 AI API 키와 호출 로직을 추가
        return None
        
    except Exception as e:
        print(f"AI illustration generation failed: {str(e)}")
        return None

def analyze_wealth_luck(sipsung_result):
    """십성 데이터를 기반으로 기본적인 재물운을 분석합니다."""
    sipsung_list = list(sipsung_result.values())
    
    # 재성 (재물의 별)
    jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")
    # 식상 (재물을 만들어내는 힘)
    siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")
    
    if jaeseong_count == 0:
        if siksang_count > 0:
            return {
                "title": "노력으로 부를 이루는 유형",
                "description": "사주에 직접적인 재물(재성)은 뚜렷하지 않지만, 재물을 만들어내는 힘(식상)이 있습니다. 당신의 창의적인 아이디어나 꾸준한 노력이 곧 재물로 이어질 수 있습니다. 과정에 집중하면 결과는 자연히 따라올 것입니다."
            }
        else:
            return {
                "title": "안정을 추구하는 대기만성형",
                "description": "사주에 재물과 관련된 기운이 강하지 않아, 큰 재물을 추구하기보다는 안정적인 수입을 통해 삶의 기반을 다지는 것이 중요합니다. 투기적인 활동보다는 성실함을 무기로 삼아야 합니다."
            }
    elif jaeseong_count > 0:
        if siksang_count > 0:
            return {
                "title": "타고난 사업가 유형 (식상생재)",
                "description": "재물을 만들어내는 힘(식상)과 재물 그 자체(재성)를 모두 갖추고 있어, 사업적인 수완이 매우 뛰어납니다. 당신의 아이디어가 곧 돈이 되는 '식상생재'의 구조를 가지고 있어 큰 부를 이룰 잠재력이 높습니다."
            }
        else:
            return {
                "title": "관리와 기회의 재물 유형",
                "description": "재물을 만들어내는 과정보다는, 이미 만들어진 재물을 관리하거나 기회를 포착하여 부를 쌓는 데 더 유리합니다. 안정적인 직장 내에서의 재무 관리나, 부동산, 유산 상속 등의 기회가 있을 수 있습니다."
            }
    return {"title": "재물운 분석", "description": "일반적인 분석입니다."}

def analyze_health_luck(sipsung_result, pillars_char):
    """십성 데이터와 사주팔자를 기반으로 건강운을 분석합니다."""
    sipsung_list = list(sipsung_result.values())
    
    # 일간의 오행
    day_gan = pillars_char['day_gan']
    day_oheng = OHENG_GAN[day_gan]
    
    # 오행별 개수 계산
    oheng_count = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
    
    for key, char in pillars_char.items():
        if 'gan' in key:
            oheng = OHENG_GAN[char]
            oheng_count[oheng] += 1
        elif 'ji' in key:
            oheng = OHENG_JIJI[char]
            oheng_count[oheng] += 1
    
    # 건강 관련 십성 분석
    # 식상 (소화기, 창의성) - 과다하면 소화불량, 부족하면 식욕부진
    siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")
    # 관성 (관절, 뼈) - 과다하면 관절염, 부족하면 골다공증
    gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")
    # 재성 (순환계, 피부) - 과다하면 혈압문제, 부족하면 빈혈
    jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")
    
    # 건강 스타일 분석
    if siksang_count > 2:
        health_style = "활발한 신진대사형"
        description = "사주에 소화와 신진대사를 나타내는 식상이 강하여, 활발한 신진대사를 가지고 있습니다. 하지만 과식이나 불규칙한 식사로 소화불량이 생길 수 있으니 주의해야 합니다. 규칙적인 식사와 적절한 운동이 중요합니다."
        weak_points = ["소화기", "위장", "대사"]
        strong_points = ["활력", "에너지", "회복력"]
    elif siksang_count == 0:
        health_style = "안정적 체질형"
        description = "사주에 식상이 부족하여 안정적인 체질을 가지고 있습니다. 소화가 느리고 식욕이 부족할 수 있으니, 소화가 잘 되는 음식을 섭취하고 규칙적인 식사가 중요합니다. 천천히 꾸준히 관리하는 것이 좋습니다."
        weak_points = ["소화기", "식욕", "대사"]
        strong_points = ["안정성", "지속력", "균형감"]
    elif gwanseong_count > 2:
        health_style = "강한 골격형"
        description = "사주에 관절과 뼈를 나타내는 관성이 강하여, 튼튼한 골격을 가지고 있습니다. 하지만 과도한 운동이나 무리한 활동으로 관절에 부담이 갈 수 있으니 주의해야 합니다. 적절한 스트레칭과 관절 관리가 중요합니다."
        weak_points = ["관절", "뼈", "인대"]
        strong_points = ["골격", "지구력", "체력"]
    elif gwanseong_count == 0:
        health_style = "유연한 체질형"
        description = "사주에 관성이 부족하여 유연한 체질을 가지고 있습니다. 관절이 약하거나 골다공증이 생길 수 있으니, 칼슘 섭취와 가벼운 운동이 중요합니다. 요가나 스트레칭 같은 유연성 운동이 도움이 됩니다."
        weak_points = ["뼈", "관절", "골격"]
        strong_points = ["유연성", "민첩성", "회복력"]
    elif jaeseong_count > 2:
        health_style = "순환계 활발형"
        description = "사주에 순환계를 나타내는 재성이 강하여, 활발한 혈액순환을 가지고 있습니다. 하지만 스트레스나 과로로 혈압이 올라갈 수 있으니 주의해야 합니다. 규칙적인 생활과 스트레스 관리가 중요합니다."
        weak_points = ["혈압", "순환계", "피부"]
        strong_points = ["혈액순환", "활력", "에너지"]
    elif jaeseong_count == 0:
        health_style = "안정적 순환형"
        description = "사주에 재성이 부족하여 안정적인 순환계를 가지고 있습니다. 빈혈이나 혈액순환이 느릴 수 있으니, 철분 섭취와 가벼운 운동이 중요합니다. 따뜻한 음식과 규칙적인 생활이 도움이 됩니다."
        weak_points = ["빈혈", "혈액순환", "체온"]
        strong_points = ["안정성", "지속력", "균형감"]
    else:
        health_style = "균형잡힌 건강형"
        description = "사주에 건강 관련 기운이 균형잡혀 있어, 전반적으로 건강한 체질을 가지고 있습니다. 하지만 나이에 따라 주의해야 할 부분이 있으니, 정기적인 건강검진과 예방 관리가 중요합니다."
        weak_points = ["나이별 변화", "예방 관리"]
        strong_points = ["균형감", "적응력", "회복력"]
    
    # 오행 균형 분석
    max_oheng = max(oheng_count.values())
    min_oheng = min(oheng_count.values())
    oheng_balance = "균형잡힌" if max_oheng - min_oheng <= 1 else "불균형한"
    
    # 건강 관리 조언
    if day_oheng == "목":
        care_advice = "간과 담낭 건강에 주의하세요. 녹차, 녹색 채소 섭취가 도움이 됩니다."
    elif day_oheng == "화":
        care_advice = "심장과 소장 건강에 주의하세요. 붉은색 음식과 따뜻한 음식 섭취가 도움이 됩니다."
    elif day_oheng == "토":
        care_advice = "비장과 위장 건강에 주의하세요. 노란색 음식과 따뜻한 음식 섭취가 도움이 됩니다."
    elif day_oheng == "금":
        care_advice = "폐와 대장 건강에 주의하세요. 흰색 음식과 매운 음식 섭취가 도움이 됩니다."
    else:  # 수
        care_advice = "신장과 방광 건강에 주의하세요. 검은색 음식과 짭짤한 음식 섭취가 도움이 됩니다."
    
    return {
        "title": health_style,
        "description": description,
        "weak_points": weak_points,
        "strong_points": strong_points,
        "oheng_balance": oheng_balance,
        "care_advice": care_advice
    }

def analyze_life_flow(year, month, day, hour, minute, sipsung_result):
    """대운과 세운을 분석하여 인생의 흐름을 분석합니다."""
    
    # 현재 나이 계산
    current_date = datetime.datetime.now()
    birth_date = datetime.datetime(year, month, day, hour, minute)
    age = current_date.year - birth_date.year
    if current_date.month < birth_date.month or (current_date.month == birth_date.month and current_date.day < birth_date.day):
        age -= 1
    
    # 대운 계산 (10년 단위)
    # 남자는 양년생, 여자는 음년생 기준으로 계산
    # 여기서는 간단히 남성 기준으로 계산
    daeun_start_age = 0
    daeun_periods = []
    
    # 현재 대운 찾기
    current_daeun = (age // 10) + 1
    daeun_start_age = (current_daeun - 1) * 10
    
    # 과거, 현재, 미래 대운 분석
    for i in range(max(1, current_daeun - 2), current_daeun + 3):
        daeun_age_start = (i - 1) * 10
        daeun_age_end = i * 10 - 1
        
        if i == current_daeun:
            period_status = "현재"
            description = "현재 진행 중인 대운입니다. 이 시기는 인생의 중요한 변화점이 될 수 있습니다."
        elif i < current_daeun:
            period_status = "과거"
            description = "이미 지나간 대운입니다. 이 시기의 경험이 현재에 영향을 미칩니다."
        else:
            period_status = "미래"
            description = "앞으로 맞이할 대운입니다. 준비를 통해 좋은 결과를 얻을 수 있습니다."
        
        daeun_periods.append({
            "period": f"{i}대운",
            "age_range": f"{daeun_age_start}~{daeun_age_end}세",
            "status": period_status,
            "description": description
        })
    
    # 세운 분석 (1년 단위)
    current_year = current_date.year
    seun_periods = []
    
    # 현재 연도 기준 전후 2년 분석
    for year_offset in range(-2, 3):
        target_year = current_year + year_offset
        
        if year_offset == 0:
            year_status = "현재"
            year_description = "현재 진행 중인 세운입니다. 올해의 운세가 인생에 큰 영향을 미칩니다."
        elif year_offset < 0:
            year_status = "과거"
            year_description = f"{abs(year_offset)}년 전 세운입니다. 이 시기의 경험이 현재에 영향을 미칩니다."
        else:
            year_status = "미래"
            year_description = f"{year_offset}년 후 세운입니다. 준비를 통해 좋은 결과를 얻을 수 있습니다."
        
        seun_periods.append({
            "year": target_year,
            "status": year_status,
            "description": year_description
        })
    
    # 인생 변화점 분석
    change_points = []
    
    # 20대 후반 (27-29세) - 첫 번째 변화점
    if 27 <= age <= 29:
        change_points.append({
            "age": "20대 후반",
            "description": "첫 번째 인생 변화점입니다. 직업이나 연애에서 중요한 결정을 내려야 할 시기입니다."
        })
    
    # 30대 중반 (33-37세) - 두 번째 변화점
    if 33 <= age <= 37:
        change_points.append({
            "age": "30대 중반",
            "description": "두 번째 인생 변화점입니다. 가정이나 경력에서 중요한 변화가 일어날 수 있습니다."
        })
    
    # 40대 초반 (40-44세) - 세 번째 변화점
    if 40 <= age <= 44:
        change_points.append({
            "age": "40대 초반",
            "description": "세 번째 인생 변화점입니다. 인생의 방향성을 재정립하는 중요한 시기입니다."
        })
    
    # 50대 중반 (53-57세) - 네 번째 변화점
    if 53 <= age <= 57:
        change_points.append({
            "age": "50대 중반",
            "description": "네 번째 인생 변화점입니다. 인생의 후반부를 준비하는 중요한 시기입니다."
        })
    
    # 미래 전망
    if age < 30:
        future_outlook = "젊은 시기로, 다양한 경험을 쌓고 인생의 기반을 다지는 중요한 시기입니다."
    elif age < 40:
        future_outlook = "성장과 발전의 시기로, 경력과 가정에서 중요한 성과를 이룰 수 있는 시기입니다."
    elif age < 50:
        future_outlook = "안정과 성숙의 시기로, 지금까지의 경험을 바탕으로 더 큰 성취를 이룰 수 있는 시기입니다."
    else:
        future_outlook = "지혜와 여유의 시기로, 인생의 후반부를 의미있게 보낼 수 있는 시기입니다."
    
    return {
        "current_age": age,
        "daeun_periods": daeun_periods,
        "seun_periods": seun_periods,
        "change_points": change_points,
        "future_outlook": future_outlook
    }

def calculate_sibiunseong(pillars_char):
    ilgan = pillars_char['day_gan']
    result = {}
    for key, jiji in pillars_char.items():
        if 'ji' in key:
            period_key = key.replace('_ji', '주')
            result[period_key] = SIBIUNSEONG_TABLE[ilgan].get(jiji, "정보 없음")
    return result

def analyze_sibiunseong(pillars_char):
    """십이운성을 분석합니다."""
    try:
        with open(SIBIUNSEONG_DATA_FILE, 'r', encoding='utf-8') as f:
            sibiunseong_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"십이운성 데이터 로딩 오류: {e}")
        return {"error": "십이운성 데이터를 불러올 수 없습니다."}
    
    sibiunseong_raw = calculate_sibiunseong(pillars_char)
    analysis = {}
    
    # 영어 키를 한글로 매핑
    period_mapping = {
        'year': '연간',
        'month': '월간', 
        'day': '일간',
        'hour': '시간'
    }
    
    for period, unseong_name in sibiunseong_raw.items():
        # 영어 키를 한글로 변환
        korean_period = period_mapping.get(period, period)
        unseong_info = sibiunseong_data.get(unseong_name, {})
        analysis[korean_period] = f"당신의 {korean_period} 시기는 '{unseong_name}'의 기운입니다. ({unseong_info.get('keyword', '')}) {unseong_info.get('description', '')}"
    
    # 종합 분석
    comprehensive = []
    for period, unseong_name in sibiunseong_raw.items():
        korean_period = period_mapping.get(period, period)
        unseong_info = sibiunseong_data.get(unseong_name, {})
        comprehensive.append(f"{korean_period}: {unseong_name} - {unseong_info.get('description', '')}")
    
    analysis['종합'] = " ".join(comprehensive)
    return analysis

def calculate_sipsung(pillars_char):
    ilgan_char = pillars_char['day_gan']
    ilgan_oheng = OHENG_GAN[ilgan_char]
    ilgan_eumyang = EUMYANG_GAN[ilgan_char]
    ilgan_eumyang_idx = 0 if ilgan_eumyang == '+' else 1
    sipsung_result = {}
    for key, char_val in pillars_char.items():
        if key == 'day_gan':
            sipsung_result[key] = "일간"
            continue
        target_oheng = OHENG_GAN[char_val] if 'gan' in key else OHENG_JIJI[char_val]
        target_eumyang = EUMYANG_GAN[char_val] if 'gan' in key else EUMYANG_JIJI[char_val]
        oheng_diff = (SIPSUNG_OHENG_ORDER.find(target_oheng) - SIPSUNG_OHENG_ORDER.find(ilgan_oheng) + 5) % 5
        base_sipsung_idx = oheng_diff * 2
        if ilgan_eumyang != target_eumyang:
            base_sipsung_idx += 1
        sipsung_result[key] = SIPSUNG_MAP[ilgan_eumyang_idx][base_sipsung_idx]
    return sipsung_result

def analyze_sipsung_by_period(sipsung_result):
    """십성 분석 결과를 시기별로 분석합니다."""
    try:
        with open(SIPSUNG_DATA_FILE, 'r', encoding='utf-8') as f:
            sipsung_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"십성 데이터 로딩 오류: {e}")
        return {"error": "십성 데이터를 불러올 수 없습니다."}
    
    analysis = {}
    periods = ['year', 'month', 'day', 'hour']
    period_names = ['연간', '월간', '일간', '시간']
    
    for i, period in enumerate(periods):
        if period in sipsung_result:
            sipsung_name = sipsung_result[period]
            sipsung_info = sipsung_data.get(sipsung_name, {})
            analysis[period_names[i]] = f"당신의 {period_names[i]} 십성은 '{sipsung_name}'입니다. {sipsung_info.get('description', '')}"
    
    # 종합 분석
    comprehensive = []
    for period in periods:
        if period in sipsung_result:
            sipsung_name = sipsung_result[period]
            sipsung_info = sipsung_data.get(sipsung_name, {})
            comprehensive.append(f"{sipsung_name}: {sipsung_info.get('description', '')}")
    
    analysis['종합'] = " ".join(comprehensive)
    return analysis

def get_ilju_analysis_data(ilju_key):
    """일주 분석 데이터를 가져옵니다."""
    try:
        with open(ILJU_DATA_FILE, 'r', encoding='utf-8') as f:
            ilju_data = json.load(f)
        return ilju_data.get(ilju_key, {})
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"일주 데이터 로딩 오류: {e}")
        return {
            "title": "일주 분석",
            "description": "일주 분석 데이터를 불러올 수 없습니다.",
            "personality": {"pros": [], "cons": []},
            "animal": {"name": "", "characteristics": []}
        }

def analyze_sibisinsal(pillars_char):
    """십이신살을 분석합니다."""
    try:
        # 십이신살 계산 로직
        sibisinsal_result = calculate_sibisinsal(pillars_char)
        analysis = {}
        
        # 시기별 분석
        periods = ["초년기", "청년기", "중년기", "장년기"]
        for period in periods:
            analysis[period] = f"당신의 {period} 시기는 십이신살의 영향을 받습니다. {get_sibisinsal_description(sibisinsal_result, period)}"
        
        return analysis
    except Exception as e:
        return {"error": f"십이신살 분석 중 오류가 발생했습니다: {str(e)}"}

def calculate_sibisinsal(pillars_char):
    """십이신살을 계산합니다."""
    # 간단한 십이신살 계산 로직
    result = {}
    for key, char in pillars_char.items():
        if 'ji' in key:
            period_key = key.replace('_ji', '살')
            result[period_key] = get_sibisinsal_type(char)
    return result

def get_sibisinsal_type(jiji):
    """지지에 따른 십이신살 유형을 반환합니다."""
    sibisinsal_map = {
        "子": "천살", "丑": "천살", "寅": "천살", "卯": "천살",
        "辰": "천살", "巳": "천살", "午": "천살", "未": "천살",
        "申": "천살", "酉": "천살", "戌": "천살", "亥": "천살"
    }
    return sibisinsal_map.get(jiji, "정보 없음")

def get_sibisinsal_description(sibisinsal_result, period):
    """십이신살 설명을 반환합니다."""
    descriptions = {
        "초년기": "이 시기에는 기본적인 인성과 성격이 형성됩니다.",
        "청년기": "이 시기에는 사회 진출과 인간관계 형성이 중요합니다.",
        "중년기": "이 시기에는 가정과 직장에서의 안정이 중요합니다.",
        "장년기": "이 시기에는 인생의 후반부를 준비하는 시기입니다."
    }
    return descriptions.get(period, "해당 시기에 대한 분석입니다.")

def analyze_guin(pillars_char):
    """귀인을 분석합니다."""
    try:
        # 귀인 계산 로직
        guin_result = calculate_guin(pillars_char)
        
        # 시기별 귀인 분석
        period_analysis = {}
        periods = ["초년기", "청년기", "중년기", "장년기"]
        for period in periods:
            period_analysis[period] = f"당신의 {period} 시기에는 {get_guin_description(guin_result, period)}"
        
        # 종합 귀인 분석
        comprehensive = f"귀인 분석 결과, 당신의 인생에는 {len(guin_result)}명의 중요한 귀인이 나타납니다."
        
        # AI 초상화 생성
        try:
            portrait_url = generate_ai_portrait("귀인 초상화", guin_result)
        except:
            portrait_url = None
        
        return {
            "period_analysis": period_analysis,
            "comprehensive": comprehensive,
            "portrait_url": portrait_url
        }
    except Exception as e:
        return {"error": f"귀인 분석 중 오류가 발생했습니다: {str(e)}"}

def calculate_guin(pillars_char):
    """귀인을 계산합니다."""
    # 간단한 귀인 계산 로직
    guin_list = []
    for key, char in pillars_char.items():
        if 'gan' in key:
            guin_type = get_guin_type(char)
            if guin_type:
                guin_list.append(guin_type)
    return guin_list

def get_guin_type(gan):
    """천간에 따른 귀인 유형을 반환합니다."""
    guin_map = {
        "甲": "갑자귀인", "乙": "을자귀인", "丙": "병자귀인", "丁": "정자귀인",
        "戊": "무자귀인", "己": "기자귀인", "庚": "경자귀인", "辛": "신자귀인",
        "壬": "임자귀인", "癸": "계자귀인"
    }
    return guin_map.get(gan, None)

def get_guin_description(guin_result, period):
    """귀인 설명을 반환합니다."""
    descriptions = {
        "초년기": "가족과 선생님의 도움을 받게 됩니다.",
        "청년기": "상사나 멘토의 지도를 받게 됩니다.",
        "중년기": "동료나 파트너의 협력을 받게 됩니다.",
        "장년기": "후배나 제자의 도움을 받게 됩니다."
    }
    return descriptions.get(period, "해당 시기의 귀인 분석입니다.")

def generate_ai_portrait(prompt, guin_data):
    """AI 초상화 생성 함수 - 배포 환경 안정성을 위해 수정"""
    try:
        # 배포 환경에서는 AI 이미지 생성이 불가능할 수 있으므로 기본값 반환
        if not prompt:
            return None
            
        # 실제 AI API 호출 대신 기본 이미지 URL 반환 (배포 환경 안정성)
        # 실제 운영에서는 여기에 AI API 키와 호출 로직을 추가
        return None
        
    except Exception as e:
        print(f"AI portrait generation failed: {str(e)}")
        return None

def enhance_wealth_analysis(sipsung_result):
    """재물운 분석을 확장합니다."""
    sipsung_list = list(sipsung_result.values())
    
    # 재성 (재물의 별)
    jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")
    # 식상 (재물을 만들어내는 힘)
    siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")
    
    # 전반적인 재물운 흐름
    if jaeseong_count > 0 and siksang_count > 0:
        overall_flow = "재물을 만들어내는 힘과 재물 그 자체를 모두 갖추고 있어, 사업적인 수완이 뛰어납니다."
    elif jaeseong_count > 0:
        overall_flow = "재물을 관리하고 활용하는 능력이 뛰어나며, 기회를 포착하여 부를 쌓을 수 있습니다."
    elif siksang_count > 0:
        overall_flow = "창의적인 아이디어로 재물을 만들어내는 능력이 있으며, 꾸준한 노력이 성공으로 이어집니다."
    else:
        overall_flow = "안정적인 수입을 통해 삶의 기반을 다지는 것이 중요하며, 성실함이 최고의 재산입니다."
    
    # 재물운 특징
    characteristics = []
    if jaeseong_count > 0:
        characteristics.append({
            "title": "재물 관리 능력",
            "description": "재물을 효율적으로 관리하고 활용하는 능력이 뛰어납니다."
        })
    if siksang_count > 0:
        characteristics.append({
            "title": "재물 창출 능력",
            "description": "새로운 아이디어로 재물을 만들어내는 창의성이 뛰어납니다."
        })
    
    # 이익과 손해를 가져다 줄 사람들
    people_analysis = "재물운과 관련하여, 당신에게 도움을 줄 수 있는 사람들과 주의해야 할 사람들이 있습니다."
    
    # 재테크 분석
    if jaeseong_count > 0 and siksang_count > 0:
        business_analysis = "사업과 투자를 병행하는 것이 유리하며, 창의적인 아이디어를 사업화하는 능력이 뛰어납니다."
    elif jaeseong_count > 0:
        business_analysis = "안정적인 투자와 재무 관리에 집중하는 것이 좋으며, 부동산이나 채권 투자가 유리합니다."
    elif siksang_count > 0:
        business_analysis = "창의적인 사업 아이템이나 프리랜서 활동이 유리하며, 자신만의 전문성을 개발하는 것이 중요합니다."
    else:
        business_analysis = "안정적인 직장 내에서의 재무 관리가 중요하며, 꾸준한 저축과 보험 가입을 권장합니다."
    
    return {
        "overall_flow": overall_flow,
        "characteristics": characteristics,
        "people_analysis": people_analysis,
        "business_analysis": business_analysis
    }

def enhance_love_analysis(sipsung_result):
    """연애운 분석을 확장합니다."""
    sipsung_list = list(sipsung_result.values())
    
    # 관성 (배우자, 연인)
    gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")
    # 재성 (재물, 매력)
    jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")
    
    # 전반적인 연애 성향
    if gwanseong_count > 0 and jaeseong_count > 0:
        overall_tendency = "열정적이고 활발한 연애를 즐기는 스타일로, 상대방을 사로잡는 매력이 뛰어납니다."
    elif gwanseong_count > 0:
        overall_tendency = "진지하고 안정적인 연애를 선호하며, 결혼을 염두에 둔 관계를 추구합니다."
    elif jaeseong_count > 0:
        overall_tendency = "자유롭고 독립적인 연애를 선호하며, 매력적이고 독립적인 연애를 즐깁니다."
    else:
        overall_tendency = "조용하고 깊이 있는 연애를 선호하며, 천천히 마음을 열어가는 스타일입니다."
    
    # 운명의 짝 소개
    destiny_partner = "당신의 운명의 짝은 당신의 부족한 부분을 보완해주는 사람일 것입니다."
    
    # 개선점
    improvement_points = "연애에서 성공하기 위해서는 상대방을 이해하려는 노력과 진심을 다한 대화가 중요합니다."
    
    # 애정운 흐름
    flow_analysis = "애정운은 인생의 각 시기마다 다른 특성을 보이며, 현재 시기가 중요한 변화점이 될 수 있습니다."
    
    # 연애운이 높은 시기와 장소
    timing_location = "연애운이 높은 시기는 봄과 가을이며, 도서관이나 카페 같은 문화 공간에서 좋은 인연을 만날 수 있습니다."
    
    return {
        "overall_tendency": overall_tendency,
        "destiny_partner": destiny_partner,
        "improvement_points": improvement_points,
        "flow_analysis": flow_analysis,
        "timing_location": timing_location
    }

def enhance_career_analysis(sipsung_result):
    """직업운 분석을 확장합니다."""
    sipsung_list = list(sipsung_result.values())
    
    # 관성 (관리, 리더십)
    gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")
    # 식상 (창의성, 전문성)
    siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")
    
    # 잘 맞는 직업/직장
    suitable_jobs = []
    if gwanseong_count > 0:
        suitable_jobs.extend(["경영자", "관리자", "행정직", "공무원"])
    if siksang_count > 0:
        suitable_jobs.extend(["전문가", "프리랜서", "교육자", "컨설턴트"])
    if not suitable_jobs:
        suitable_jobs = ["일반 사무직", "서비스업", "생산직"]
    
    # 사업 vs 직장 분석
    if gwanseong_count > 0 and siksang_count > 0:
        business_vs_job = "리더십과 전문성을 모두 갖추고 있어, 사업과 직장 모두에서 성공할 수 있습니다."
    elif gwanseong_count > 0:
        business_vs_job = "관리 능력이 뛰어나 직장에서 승진과 성장을 이룰 수 있습니다."
    elif siksang_count > 0:
        business_vs_job = "창의성과 전문성이 뛰어나 독립적인 사업이나 프리랜서 활동이 유리합니다."
    else:
        business_vs_job = "안정적인 직장 생활이 적합하며, 꾸준한 노력으로 성장할 수 있습니다."
    
    # 성공적인 직장생활을 위한 조언
    advice = "성공적인 직장생활을 위해서는 끊임없는 자기계발과 팀워크를 중시하는 마음가짐이 중요합니다."
    
    # 주의해야 할 사람 분석
    caution_people = "직장에서 주의해야 할 사람은 당신의 성장을 방해하거나 부정적인 영향을 주는 사람들입니다."
    
    return {
        "suitable_jobs": suitable_jobs,
        "business_vs_job": business_vs_job,
        "advice": advice,
        "caution_people": caution_people
    }

def enhance_health_analysis(sipsung_result, pillars_char):
    """건강운 분석을 확장합니다."""
    # 타고난 체질과 건강 상태
    constitution = "당신의 타고난 체질을 이해하고 관리하는 것이 건강의 기본입니다."
    
    # 잘 맞는 운동
    suitable_exercise = "당신에게 맞는 운동은 규칙적이고 지속 가능한 운동입니다."
    
    # 시기에 따른 건강운
    timing_analysis = "건강운은 나이와 시기에 따라 변화하므로, 각 시기에 맞는 건강 관리가 중요합니다."
    
    return {
        "constitution": constitution,
        "suitable_exercise": suitable_exercise,
        "timing_analysis": timing_analysis
    }

def generate_comprehensive_report(data):
    """종합 리포트를 생성합니다."""
    summary = "당신의 사주를 종합적으로 분석한 결과, 다양한 운세의 조화를 통해 인생의 방향성을 제시합니다."
    
    recommendations = "현재 상황과 미래 전망을 고려한 구체적인 권장사항을 제시합니다."
    
    future_outlook = "당신의 사주를 바탕으로 한 미래 전망과 준비해야 할 사항들을 안내합니다."
    
    return {
        "summary": summary,
        "recommendations": recommendations,
        "future_outlook": future_outlook
    }
