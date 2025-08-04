import json
import os
import datetime
import requests

# ... (기존의 모든 상수 정의 및 데이터 파일 경로는 동일) ...
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
    # ... (기존 사주팔자 계산 로직은 동일)
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
    
    # 재물운 분석 추가
    wealth_luck_analysis = analyze_wealth_luck(sipsung_result)
    
    # 연애운 분석 추가
    love_luck_analysis = analyze_love_luck(sipsung_result)

    ilju_analysis_data = get_ilju_analysis_data(f"{day_gan}{JIJI[day_ji_idx]}")
    
    return {
        "year_pillar": f"{year_gan}{year_ji}",
        "month_pillar": f"{month_gan}{month_ji}",
        "day_pillar": f"{day_gan}{JIJI[day_ji_idx]}",
        "hour_pillar": f"{hour_gan}{hour_ji}",
        "sipsung_raw": sipsung_result,
        "sipsung_analysis": sipsung_analysis,
        "sibiunseong_analysis": sibiunseong_analysis,
        "wealth_luck_analysis": wealth_luck_analysis,
        "love_luck_analysis": love_luck_analysis, # 결과에 추가
        "ilju_analysis": ilju_analysis_data
    }

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
    """AI 일러스트를 생성합니다."""
    try:
        # 여기서는 예시로 간단한 API 호출을 시뮬레이션합니다
        # 실제로는 Stable Diffusion API나 다른 AI 이미지 생성 서비스를 사용합니다
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY', '')}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["artifacts"][0]["base64"]
        else:
            return None
    except:
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

# ... (나머지 함수들은 기존과 동일)
def calculate_sibiunseong(pillars_char):
    ilgan = pillars_char['day_gan']
    result = {}
    for key, jiji in pillars_char.items():
        if 'ji' in key:
            period_key = key.replace('_ji', '주')
            result[period_key] = SIBIUNSEONG_TABLE[ilgan].get(jiji, "정보 없음")
    return result

def analyze_sibiunseong(pillars_char):
    try:
        with open(SIBIUNSEONG_DATA_FILE, 'r', encoding='utf-8') as f:
            sibiunseong_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "십이운성 데이터 파일을 읽는 데 문제가 발생했습니다."}
    sibiunseong_raw = calculate_sibiunseong(pillars_char)
    analysis = {}
    for period, unseong_name in sibiunseong_raw.items():
        unseong_info = sibiunseong_data.get(unseong_name, {})
        analysis[period] = f"당신의 {period} 시기는 '{unseong_name}'의 기운입니다. ({unseong_info.get('keyword', '')}) {unseong_info.get('description', '')}"
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
    try:
        with open(SIPSUNG_DATA_FILE, 'r', encoding='utf-8') as f:
            sipsung_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "십성 데이터 파일을 읽는 데 문제가 발생했습니다."}
    analysis = {
        "초년운 (연주)": f"당신의 초년은 {sipsung_result['year_gan']}과(와) {sipsung_result['year_ji']}의 영향을 받습니다. {sipsung_data.get(sipsung_result['year_gan'], {}).get('positive', '')} 또한, {sipsung_data.get(sipsung_result['year_ji'], {}).get('positive', '')}",
        "청년운 (월주)": f"청년기, 특히 사회생활과 직업 환경은 {sipsung_result['month_gan']}과(와) {sipsung_result['month_ji']}의 영향을 크게 받습니다. 이는 {sipsung_data.get(sipsung_result['month_gan'], {}).get('positive', '')} 그리고 {sipsung_data.get(sipsung_result['month_ji'], {}).get('positive', '')}",
        "중년운 (일주)": f"중년기의 당신 자신과 배우자와의 관계는 {sipsung_result['day_ji']}의 영향을 받습니다. {sipsung_data.get(sipsung_result['day_ji'], {}).get('positive', '')}",
        "말년운 (시주)": f"말년의 삶과 당신의 내면, 자녀와의 관계는 {sipsung_result['hour_gan']}과(와) {sipsung_result['hour_ji']}의 영향을 받습니다. {sipsung_data.get(sipsung_result['hour_gan'], {}).get('positive', '')} 그리고 {sipsung_data.get(sipsung_result['hour_ji'], {}).get('positive', '')}"
    }
    return analysis

def get_ilju_analysis_data(ilju_key):
    try:
        with open(ILJU_DATA_FILE, 'r', encoding='utf-8') as f:
            all_ilju_data = json.load(f)
        ilju_key_korean = "".join([CHEONGAN_KOR[CHEONGAN.find(c)] if c in CHEONGAN else JIJI_KOR[JIJI.find(c)] for c in ilju_key])
        return all_ilju_data.get(ilju_key_korean, {
            "title": f"{ilju_key} ({ilju_key_korean}) 일주 분석",
            "description": f"해당 일주에 대한 데이터는 아직 준비되지 않았습니다.",
            "pros": [],
            "cons": [],
            "animal": ""
        })
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "일주 데이터 파일을 읽는 데 문제가 발생했습니다."}
