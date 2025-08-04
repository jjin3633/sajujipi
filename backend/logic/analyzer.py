import json
import os
import datetime

# --- 기본 상수 정의 ---
CHEONGAN = "甲乙丙丁戊己庚辛壬癸"
CHEONGAN_KOR = "갑을병정무기경신임계"
JIJI = "子丑寅卯辰巳午未申酉戌亥"
JIJI_KOR = "자축인묘진사오미신유술해"

OHENG_GAN = {"甲":"목", "乙":"목", "丙":"화", "丁":"화", "戊":"토", "己":"토", "庚":"금", "辛":"금", "壬":"수", "癸":"수"}
EUMYANG_GAN = {"甲":"+", "乙":"-", "丙":"+", "丁":"-", "戊":"+", "己":"-", "庚":"+", "辛":"-", "壬":"+", "癸":"-"}
OHENG_JIJI = {"子":"수", "丑":"토", "寅":"목", "卯":"목", "辰":"토", "巳":"화", "午":"화", "未":"토", "申":"금", "酉":"금", "戌":"토", "亥":"수"}
EUMYANG_JIJI = {"子":"+", "丑":"-", "寅":"+", "卯":"-", "辰":"+", "巳":"-", "午":"+", "未":"-", "申":"+", "酉":"-", "戌":"+", "亥":"-"}

SIPSUNG_OHENG_ORDER = "목화토금수"
SIPSUNG_MAP = [
    ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"],
    ["겁재", "비견", "상관", "식신", "정재", "편재", "정관", "편관", "정인", "편인"]
]

# 십이운성 포태법 테이블
SIBIUNSEONG_TABLE = {
    "甲": {"亥": "장생", "子": "목욕", "丑": "관대", "寅": "건록", "卯": "제왕", "辰": "쇠", "巳": "병", "午": "사", "未": "묘", "申": "절", "酉": "태", "戌": "양"},
    "丙": {"寅": "장생", "卯": "목욕", "辰": "관대", "巳": "건록", "午": "제왕", "未": "쇠", "申": "병", "酉": "사", "戌": "묘", "亥": "절", "子": "태", "丑": "양"},
    "戊": {"寅": "장생", "卯": "목욕", "辰": "관대", "巳": "건록", "午": "제왕", "未": "쇠", "申": "병", "酉": "사", "戌": "묘", "亥": "절", "子": "태", "丑": "양"},
    "庚": {"巳": "장생", "午": "목욕", "未": "관대", "申": "건록", "酉": "제왕", "戌": "쇠", "亥": "병", "子": "사", "丑": "묘", "寅": "절", "卯": "태", "辰": "양"},
    "壬": {"申": "장생", "酉": "목욕", "戌": "관대", "亥": "건록", "子": "제왕", "丑": "쇠", "寅": "병", "卯": "사", "辰": "묘", "巳": "절", "午": "태", "未": "양"},
    # 음간은 역행
    "乙": {"午": "장생", "巳": "목욕", "辰": "관대", "卯": "건록", "寅": "제왕", "丑": "쇠", "子": "병", "亥": "사", "戌": "묘", "酉": "절", "申": "태", "未": "양"},
    "丁": {"酉": "장생", "申": "목욕", "未": "관대", "午": "건록", "巳": "제왕", "辰": "쇠", "卯": "병", "寅": "사", "丑": "묘", "子": "절", "亥": "태", "戌": "양"},
    "己": {"酉": "장생", "申": "목욕", "未": "관대", "午": "건록", "巳": "제왕", "辰": "쇠", "卯": "병", "寅": "사", "丑": "묘", "子": "절", "亥": "태", "戌": "양"},
    "辛": {"子": "장생", "亥": "목욕", "戌": "관대", "酉": "건록", "申": "제왕", "未": "쇠", "午": "병", "巳": "사", "辰": "묘", "卯": "절", "寅": "태", "丑": "양"},
    "癸": {"卯": "장생", "寅": "목욕", "丑": "관대", "子": "건록", "亥": "제왕", "戌": "쇠", "酉": "병", "申": "사", "未": "묘", "午": "절", "巳": "태", "辰": "양"}
}

# --- 데이터 파일 경로 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ILJU_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'ilju_data.json')
SIPSUNG_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'sipsung_data.json')
SIBIUNSEONG_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'sibiunseong_data.json')

# --- 핵심 계산 함수 ---
def get_saju_details(year, month, day, hour, minute):
    # ... (기존의 사주팔자 계산 로직은 동일) ...
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
    year_gan_key = [k for k in gan_start_map if year_gan in k][0]
    month_gan_start_idx = CHEONGAN.find(gan_start_map[year_gan_key])
    month_offset = (JIJI.find(month_ji) - JIJI.find("寅") + 12) % 12
    month_gan_idx = (month_gan_start_idx + month_offset) % 10
    month_gan = CHEONGAN[month_gan_idx]
    
    hour_ji_idx = (hour + 1) // 2 % 12
    if hour == 23: hour_ji_idx = 0
    hour_ji = JIJI[hour_ji_idx]
    gan_start_map_hour = {"甲己":"甲", "乙庚":"丙", "丙辛":"戊", "丁壬":"庚", "戊癸":"壬"}
    day_gan_key = [k for k in gan_start_map_hour if day_gan in k][0]
    hour_gan_start_idx = CHEONGAN.find(gan_start_map_hour[day_gan_key])
    hour_gan_idx = (hour_gan_start_idx + hour_ji_idx) % 10
    hour_gan = CHEONGAN[hour_gan_idx]

    pillars_char = {
        'year_gan': year_gan, 'year_ji': year_ji,
        'month_gan': month_gan, 'month_ji': JIJI[day_ji_idx], # 버그 수정: 월지 -> 일지
        'day_gan': day_gan, 'day_ji': JIJI[day_ji_idx],
        'hour_gan': hour_gan, 'hour_ji': hour_ji
    }
    pillars_char['month_ji'] = month_ji # 월지 재할당

    sipsung_result = calculate_sipsung(pillars_char)
    sipsung_analysis = analyze_sipsung_by_period(sipsung_result)
    
    # 십이운성 분석 추가
    sibiunseong_analysis = analyze_sibiunseong(pillars_char)

    ilju_analysis_data = get_ilju_analysis_data(f"{day_gan}{JIJI[day_ji_idx]}")
    
    return {
        "year_pillar": f"{year_gan}{year_ji}",
        "month_pillar": f"{month_gan}{month_ji}",
        "day_pillar": f"{day_gan}{JIJI[day_ji_idx]}",
        "hour_pillar": f"{hour_gan}{hour_ji}",
        "sipsung_raw": sipsung_result,
        "sipsung_analysis": sipsung_analysis,
        "sibiunseong_analysis": sibiunseong_analysis, # 결과에 추가
        "ilju_analysis": ilju_analysis_data
    }

def calculate_sibiunseong(pillars_char):
    """일간을 기준으로 각 지지의 십이운성을 계산합니다."""
    ilgan = pillars_char['day_gan']
    result = {}
    for key, jiji in pillars_char.items():
        if 'ji' in key:
            period_key = key.replace('_ji', '주') # 예: year_ji -> 연주
            result[period_key] = SIBIUNSEONG_TABLE[ilgan].get(jiji, "정보 없음")
    return result

def analyze_sibiunseong(pillars_char):
    """계산된 십이운성과 데이터 파일을 결합하여 분석 텍스트를 생성합니다."""
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

# ... (calculate_sipsung, analyze_sipsung_by_period, get_ilju_analysis_data 함수는 기존과 동일) ...
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
            "title": f"{ilju_key} 일주 분석",
            "description": f"'{ilju_key_korean}' 일주에 대한 데이터가 아직 준비되지 않았습니다."
        })
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "일주 데이터 파일을 읽는 데 문제가 발생했습니다."}
