\import json
import os
import datetime
from pycalcal import astro

# 천간(天干)과 지지(地支) 리스트
CHEONGAN = "갑을병정무기경신임계"
JIJI = "자축인묘진사오미신유술해"
JIJI_ORDER = {j: i for i, j in enumerate(JIJI)}

# 데이터 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'ilju_data.json')


def get_saju_details(year, month, day, hour, minute):
    """
    pycalcal 라이브러리를 사용하여 정확한 사주팔자를 계산합니다.
    """
    # 1. 율리우스력(JD)으로 변환
    jd = astro.calendar_to_jd(year, month, day, hour, minute, 0)

    # 2. 사주팔자 계산
    # pycalcal의 to_chinese_char 함수는 JD를 기반으로 년,월,일,시의 간지를 반환합니다.
    # 결과는 (천간 인덱스, 지지 인덱스) 튜플의 리스트로 나옵니다.
    # [연주, 월주, 일주, 시주]
    pillars = astro.to_chinese_char(jd)
    
    year_gan_idx, year_ji_idx = pillars[0]
    month_gan_idx, month_ji_idx = pillars[1]
    day_gan_idx, day_ji_idx = pillars[2]
    hour_gan_idx, hour_ji_idx = pillars[3]
    
    # 인덱스를 한글 간지로 변환
    year_pillar = f"{CHEONGAN[year_gan_idx-1]}{JIJI[year_ji_idx-1]}"
    month_pillar = f"{CHEONGAN[month_gan_idx-1]}{JIJI[month_ji_idx-1]}"
    day_pillar = f"{CHEONGAN[day_gan_idx-1]}{JIJI[day_ji_idx-1]}"
    hour_pillar = f"{CHEONGAN[hour_gan_idx-1]}{JIJI[hour_ji_idx-1]}"

    # 3. 일주 분석 데이터 가져오기
    ilju_key = f"{CHEONGAN[day_gan_idx-1]}{JIJI[day_ji_idx-1]}"
    ilju_analysis_data = get_ilju_analysis_data(ilju_key)

    return {
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
        "hour_pillar": hour_pillar,
        "ilju_analysis": ilju_analysis_data
    }

def get_ilju_analysis_data(ilju_key):
    """
    JSON 파일에서 일주 이름(키)에 맞는 분석 데이터를 찾아 반환합니다.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            all_ilju_data = json.load(f)
        
        return all_ilju_data.get(ilju_key, {
            "title": f"{ilju_key} 일주 분석",
            "description": f"입력된 생년월일에 해당하는 '{ilju_key}' 일주에 대한 상세 분석 데이터는 아직 준비되지 않았습니다.",
            "pros": [],
            "cons": [],
            "animal": ""
        })
    except FileNotFoundError:
        return {"error": f"데이터 파일을 찾을 수 없습니다: {DATA_FILE}"}
    except json.JSONDecodeError:
        return {"error": "데이터 파일의 형식이 올바르지 않습니다."}

