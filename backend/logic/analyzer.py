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
    ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"], # 양일간(+)
    ["겁재", "비견", "상관", "식신", "정재", "편재", "정관", "편관", "정인", "편인"]  # 음일간(-)
]

# --- 데이터 파일 경로 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ILJU_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'ilju_data.json')
SIPSUNG_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'sipsung_data.json')

# --- 핵심 계산 함수 ---
def get_saju_details(year, month, day, hour, minute):
    """
    순수 Python 코드로 사주팔자와 십성 정보를 계산합니다.
    """
    # 1. 기준점: 1899년 12월 22일 0시 0분 = 경자년 무자월 갑자일 갑자시
    ref_date = datetime.datetime(1899, 12, 22, 0, 0)
    target_date = datetime.datetime(year, month, day, hour, minute)
    
    # 2. 일주 계산
    delta_days = (target_date - ref_date).days
    day_gan_idx = (delta_days + 0) % 10  # 기준일이 갑자일
    day_ji_idx = (delta_days + 0) % 12
    day_gan = CHEONGAN[day_gan_idx]
    day_ji = JIJI[day_ji_idx]
    
    # 3. 입춘 계산 (간이법) 및 연주 결정
    # 24절기 계산은 복잡하므로, 여기서는 입춘을 대략 양력 2월 4일로 간주
    ipchun = datetime.datetime(year, 2, 4)
    saju_year = year if target_date >= ipchun else year - 1
    year_gan_idx = (saju_year - 1864) % 10 # 1864년이 갑자년
    year_ji_idx = (saju_year - 1864) % 12
    year_gan = CHEONGAN[year_gan_idx]
    year_ji = JIJI[year_ji_idx]

    # 4. 월주 계산 (월건법)
    month_ji_map = {1:"寅", 2:"卯", 3:"辰", 4:"巳", 5:"午", 6:"未", 7:"申", 8:"酉", 9:"戌", 10:"亥", 11:"子", 12:"丑"}
    month_ji = month_ji_map[month] # 실제로는 절기 기준이지만 간소화
    gan_start_map = {"甲己":"丙", "乙庚":"戊", "丙辛":"庚", "丁壬":"壬", "戊癸":"甲"}
    year_gan_key = [k for k in gan_start_map if year_gan in k][0]
    month_gan_start_idx = CHEONGAN.find(gan_start_map[year_gan_key])
    month_offset = (JIJI.find("寅") - JIJI.find(month_ji)) # 월지와 인목의 차이
    month_gan_idx = (month_gan_start_idx - month_offset + 12) % 10
    month_gan = CHEONGAN[month_gan_idx]

    # 5. 시주 계산
    hour_ji_idx = (hour + 1) // 2 % 12
    hour_ji = JIJI[hour_ji_idx]
    gan_start_map_hour = {"甲己":"甲", "乙庚":"丙", "丙辛":"戊", "丁壬":"庚", "戊癸":"壬"}
    day_gan_key = [k for k in gan_start_map_hour if day_gan in k][0]
    hour_gan_start_idx = CHEONGAN.find(gan_start_map_hour[day_gan_key])
    hour_gan_idx = (hour_gan_start_idx + hour_ji_idx) % 10
    hour_gan = CHEONGAN[hour_gan_idx]

    # --- 결과 조합 ---
    pillars_char = {
        'year_gan': year_gan, 'year_ji': year_ji,
        'month_gan': month_gan, 'month_ji': month_ji,
        'day_gan': day_gan, 'day_ji': day_ji,
        'hour_gan': hour_gan, 'hour_ji': hour_ji
    }

    sipsung_result = calculate_sipsung(pillars_char)
    sipsung_analysis = analyze_sipsung_by_period(sipsung_result)
    ilju_key = f"{day_gan}{day_ji}"
    ilju_analysis_data = get_ilju_analysis_data(ilju_key)
    
    return {
        "year_pillar": f"{year_gan}{year_ji}",
        "month_pillar": f"{month_gan}{month_ji}",
        "day_pillar": f"{day_gan}{day_ji}",
        "hour_pillar": f"{hour_gan}{hour_ji}",
        "sipsung_raw": sipsung_result,
        "sipsung_analysis": sipsung_analysis,
        "ilju_analysis": ilju_analysis_data
    }

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
    
    # ... (분석 텍스트 생성 로직은 동일)
    analysis = {
        "초년운": f"{sipsung_result['year_gan']}, {sipsung_result['year_ji']}의 영향: {sipsung_data.get(sipsung_result['year_gan'], {}).get('positive', '')}",
        "청년운": f"{sipsung_result['month_gan']}, {sipsung_result['month_ji']}의 영향: {sipsung_data.get(sipsung_result['month_gan'], {}).get('positive', '')}",
        "중년운": f"{sipsung_result['day_ji']}의 영향: {sipsung_data.get(sipsung_result['day_ji'], {}).get('positive', '')}",
        "말년운": f"{sipsung_result['hour_gan']}, {sipsung_result['hour_ji']}의 영향: {sipsung_data.get(sipsung_result['hour_gan'], {}).get('positive', '')}"
    }
    return analysis

def get_ilju_analysis_data(ilju_key):
    try:
        with open(ILJU_DATA_FILE, 'r', encoding='utf-8') as f:
            all_ilju_data = json.load(f)
        
        # 한글 키로 변환
        ilju_key_korean = "".join([CHEONGAN_KOR[CHEONGAN.find(c)] if c in CHEONGAN else JIJI_KOR[JIJI.find(c)] for c in ilju_key])
        return all_ilju_data.get(ilju_key_korean, {
            "title": f"{ilju_key} 일주 분석",
            "description": f"데이터 없음"
        })
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "일주 데이터 파일을 읽는 데 문제가 발생했습니다."}
