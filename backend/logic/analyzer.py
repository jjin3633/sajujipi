import json
import os
import datetime
import requests
from functools import lru_cache
from typing import Dict, List, Optional, Any

# 상수 정의
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
    "甲": {"亥": "장생", "子": "목욕", "丑": "관대", "寅": "건록", "卯": "제왕", "辰": "쇠", "巳": "병", "未": "묘", "申": "절", "酉": "태", "戌": "양"},
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

# 파일 경로 상수
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ILJU_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'ilju_data.json')
SIPSUNG_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'sipsung_data.json')
SIBIUNSEONG_DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'sibiunseong_data.json')

# 데이터 캐싱을 위한 전역 변수
_DATA_CACHE = {}

# 유틸리티 함수들
def safe_load_json(file_path: str, default: Dict = None) -> Dict:
    """안전하게 JSON 파일을 로드합니다."""
    try:
        print(f"파일 로딩 시도: {file_path}")
        if not os.path.exists(file_path):
            print(f"파일이 존재하지 않음: {file_path}")
            return default or {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"파일 로딩 성공: {file_path}")
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"데이터 로딩 오류 ({file_path}): {e}")
        return default or {}
    except Exception as e:
        print(f"예상치 못한 오류 ({file_path}): {e}")
        return default or {}

@lru_cache(maxsize=128)
def get_cached_data(data_type: str) -> Dict:
    """캐시된 데이터를 반환합니다."""
    if data_type not in _DATA_CACHE:
        file_map = {
            'ilju': ILJU_DATA_FILE,
            'sipsung': SIPSUNG_DATA_FILE,
            'sibiunseong': SIBIUNSEONG_DATA_FILE
        }
        _DATA_CACHE[data_type] = safe_load_json(file_map.get(data_type, ''))
    return _DATA_CACHE[data_type]

def validate_date_input(year: int, month: int, day: int, hour: int, minute: int) -> bool:
    """날짜 입력값을 검증합니다."""
    try:
        datetime.datetime(year, month, day, hour, minute)
        return 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23 and 0 <= minute <= 59
    except ValueError:
        return False

def create_error_response(message: str, error_type: str = "validation_error") -> Dict:
    """표준화된 오류 응답을 생성합니다."""
    return {"error": message, "error_type": error_type}

def safe_ai_generation(func_name: str, prompt: str) -> Optional[str]:
    """안전한 AI 이미지 생성을 수행합니다."""
    try:
        if not prompt:
            return None
        
        # 배포 환경에서는 AI 이미지 생성이 비활성화되므로 placeholder URL 반환
        if func_name == "illustration":
            return "https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=사주+일러스트"
        elif func_name == "portrait":
            return "https://via.placeholder.com/300x400/FF6B6B/FFFFFF?text=사주+초상화"
        elif func_name == "avatar":
            return "https://via.placeholder.com/200x200/50C878/FFFFFF?text=사주+아바타"
        else:
            return "https://via.placeholder.com/400x300/9B59B6/FFFFFF?text=사주+이미지"
            
    except Exception as e:
        print(f"AI {func_name} generation failed: {str(e)}")
        return None

def get_saju_details(year: int, month: int, day: int, hour: int, minute: int) -> Dict[str, Any]:
    """사주 분석의 메인 함수 - 최적화된 버전"""
    
    try:
        # 입력값 검증
        if not validate_date_input(year, month, day, hour, minute):
            return create_error_response("유효하지 않은 날짜/시간 입력입니다.")
        
        # 사주 계산
        pillars_char = calculate_saju_pillars(year, month, day, hour, minute)
        if "error" in pillars_char:
            return pillars_char
        
        # 기본 분석 수행
        analysis_results = perform_basic_analysis(pillars_char)
        if "error" in analysis_results:
            return analysis_results
        
        # 고급 분석 수행
        enhanced_results = perform_enhanced_analysis(pillars_char, analysis_results, year, month, day, hour, minute)
        if "error" in enhanced_results:
            return enhanced_results
        
        # AI 이미지 생성 (배포 환경에서는 비활성화)
        ai_results = generate_ai_images(pillars_char)
        
        # 최종 결과 조합
        final_result = {
            **analysis_results,
            **enhanced_results,
            **ai_results
        }
        
        return final_result
        
    except Exception as e:
        print(f"사주 분석 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return create_error_response(f"분석 중 오류가 발생했습니다: {str(e)}")

def calculate_saju_pillars(year: int, month: int, day: int, hour: int, minute: int) -> Dict[str, str]:
    """사주 사주를 계산합니다."""
    try:
        ref_date = datetime.datetime(1899, 12, 22, 0, 0)
        target_date = datetime.datetime(year, month, day, hour, minute)
        delta_days = (target_date - ref_date).days
        
        # 일간 계산
        day_gan_idx = delta_days % 10
        day_ji_idx = delta_days % 12
        day_gan = CHEONGAN[day_gan_idx]
        
        # 연간 계산
        ipchun = datetime.datetime(year, 2, 4)
        saju_year = year if target_date >= ipchun else year - 1
        year_gan_idx = (saju_year - 1864) % 10
        year_ji_idx = (saju_year - 1864) % 12
        year_gan = CHEONGAN[year_gan_idx]
        year_ji = JIJI[year_ji_idx]
        
        # 월간 계산
        month_ji_map = {1:"寅", 2:"卯", 3:"辰", 4:"巳", 5:"午", 6:"未", 7:"申", 8:"酉", 9:"戌", 10:"亥", 11:"子", 12:"丑"}
        month_ji = month_ji_map.get(month, "寅")
        month_gan = calculate_month_gan(year_gan, month_ji)
        
        # 시간 계산
        hour_ji_idx = (hour + 1) // 2 % 12
        if hour == 23: hour_ji_idx = 0
        hour_ji = JIJI[hour_ji_idx]
        hour_gan = calculate_hour_gan(day_gan, hour_ji_idx)
        
        print(f"사주 계산 결과: {year_gan}{year_ji} {month_gan}{month_ji} {day_gan}{JIJI[day_ji_idx]} {hour_gan}{hour_ji}")
        
        return {
            'year_gan': year_gan, 'year_ji': year_ji,
            'month_gan': month_gan, 'month_ji': month_ji,
            'day_gan': day_gan, 'day_ji': JIJI[day_ji_idx],
            'hour_gan': hour_gan, 'hour_ji': hour_ji
        }
        
    except Exception as e:
        print(f"사주 계산 중 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return create_error_response(f"사주 계산 오류: {str(e)}")

def calculate_month_gan(year_gan: str, month_ji: str) -> str:
    """월간을 계산합니다."""
    gan_start_map = {"甲己":"丙", "乙庚":"戊", "丙辛":"庚", "丁壬":"壬", "戊癸":"甲"}
    year_gan_key_list = [k for k in gan_start_map if year_gan in k]
    if not year_gan_key_list:
        raise ValueError("연간 계산 오류")
    
    year_gan_key = year_gan_key_list[0]
    month_gan_start_char = gan_start_map[year_gan_key]
    month_gan_start_idx = CHEONGAN.find(month_gan_start_char)
    month_ji_start_idx = JIJI.find("寅")
    month_ji_current_idx = JIJI.find(month_ji)
    month_offset = (month_ji_current_idx - month_ji_start_idx + 12) % 12
    month_gan_idx = (month_gan_start_idx + month_offset) % 10
    return CHEONGAN[month_gan_idx]

def calculate_hour_gan(day_gan: str, hour_ji_idx: int) -> str:
    """시간을 계산합니다."""
    gan_start_map_hour = {"甲己":"甲", "乙庚":"丙", "丙辛":"戊", "丁壬":"庚", "戊癸":"壬"}
    day_gan_key_list = [k for k in gan_start_map_hour if day_gan in k]
    if not day_gan_key_list:
        raise ValueError("시간 계산 오류")
    
    day_gan_key = day_gan_key_list[0]
    hour_gan_start_char = gan_start_map_hour[day_gan_key]
    hour_gan_start_idx = CHEONGAN.find(hour_gan_start_char)
    hour_gan_idx = (hour_gan_start_idx + hour_ji_idx) % 10
    return CHEONGAN[hour_gan_idx]

def perform_basic_analysis(pillars_char: Dict[str, str]) -> Dict[str, Any]:
    """기본 분석을 수행합니다."""
    sipsung_result = calculate_sipsung(pillars_char)
    
    return {
        "sipsung_raw": sipsung_result,
        "sipsung_analysis": analyze_sipsung_by_period(sipsung_result),
        "sibiunseong_analysis": analyze_sibiunseong(pillars_char),
        "sibisinsal_analysis": analyze_sibisinsal(pillars_char),
        "guin_analysis": analyze_guin(pillars_char)
    }

def perform_enhanced_analysis(pillars_char: Dict[str, str], basic_results: Dict[str, Any], year: int = None, month: int = None, day: int = None, hour: int = None, minute: int = None) -> Dict[str, Any]:
    """확장 분석을 수행합니다."""
    sipsung_result = basic_results["sipsung_raw"]
    
    # 기본 분석
    wealth_luck = analyze_wealth_luck(sipsung_result)
    love_luck = analyze_love_luck(sipsung_result)
    career_luck = analyze_career_luck(sipsung_result)
    health_luck = analyze_health_luck(sipsung_result, pillars_char)
    
    # 확장 분석
    wealth_enhanced = enhance_wealth_analysis(sipsung_result)
    love_enhanced = enhance_love_analysis(sipsung_result)
    career_enhanced = enhance_career_analysis(sipsung_result)
    health_enhanced = enhance_health_analysis(sipsung_result, pillars_char)
    
    # 대운 분석 - 날짜 정보가 있으면 정확한 분석 수행
    if all([year, month, day, hour, minute]):
        life_flow = analyze_life_flow(year, month, day, hour, minute, sipsung_result)
    else:
        life_flow = {
            "current_age": 0,
            "daeun_periods": [],
            "seun_periods": [],
            "change_points": [],
            "future_outlook": "대운 분석을 위해서는 원래 날짜 정보가 필요합니다."
        }
    
    # 종합 리포트 생성
    final_result = {
        "wealth_luck_analysis": {**wealth_luck, **wealth_enhanced},
        "love_luck_analysis": {**love_luck, **love_enhanced},
        "career_luck_analysis": {**career_luck, **career_enhanced},
        "health_luck_analysis": {**health_luck, **health_enhanced},
        "life_flow_analysis": life_flow,
        "comprehensive_report": generate_comprehensive_report_detailed(pillars_char, basic_results, life_flow)
    }
    
    return final_result

def generate_ai_images(pillars_char: Dict[str, str]) -> Dict[str, Any]:
    """AI 이미지들을 생성합니다."""
    day_gan = pillars_char['day_gan']
    
    # 십이운성 일러스트
    sibiunseong_prompt = f"Traditional Korean fortune telling illustration showing the twelve fortunes (십이운성) with {day_gan} day master, mystical atmosphere, traditional Korean art style, detailed and colorful"
    sibiunseong_illustration_url = safe_ai_generation("illustration", sibiunseong_prompt)
    
    return {
        "sibiunseong_illustration_url": sibiunseong_illustration_url
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

def analyze_life_flow(year: int, month: int, day: int, hour: int, minute: int, sipsung_result: Dict[str, str]) -> Dict[str, Any]:
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

def calculate_sibiunseong(pillars_char: Dict[str, str]) -> Dict[str, str]:
    """십이운성을 계산합니다."""
    ilgan = pillars_char['day_gan']
    result = {}
    for key, jiji in pillars_char.items():
        if 'ji' in key:
            period_key = key.replace('_ji', '주')
            result[period_key] = SIBIUNSEONG_TABLE[ilgan].get(jiji, "정보 없음")
    return result

def calculate_sipsung(pillars_char: Dict[str, str]) -> Dict[str, str]:
    """십성을 계산합니다."""
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

def analyze_sibisinsal(pillars_char: Dict[str, str]) -> Dict[str, str]:
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

def calculate_sibisinsal(pillars_char: Dict[str, str]) -> Dict[str, str]:
    """십이신살을 계산합니다."""
    # 간단한 십이신살 계산 로직
    result = {}
    for key, char in pillars_char.items():
        if 'ji' in key:
            period_key = key.replace('_ji', '살')
            result[period_key] = get_sibisinsal_type(char)
    return result

def get_sibisinsal_type(jiji: str) -> str:
    """지지에 따른 십이신살 유형을 반환합니다."""
    sibisinsal_map = {
        "子": "천살", "丑": "천살", "寅": "천살", "卯": "천살",
        "辰": "천살", "巳": "천살", "午": "천살", "未": "천살",
        "申": "천살", "酉": "천살", "戌": "천살", "亥": "천살"
    }
    return sibisinsal_map.get(jiji, "정보 없음")

def get_sibisinsal_description(sibisinsal_result: Dict[str, str], period: str) -> str:
    """십이신살 설명을 반환합니다."""
    descriptions = {
        "초년기": "이 시기에는 기본적인 인성과 성격이 형성됩니다.",
        "청년기": "이 시기에는 사회 진출과 인간관계 형성이 중요합니다.",
        "중년기": "이 시기에는 가정과 직장에서의 안정이 중요합니다.",
        "장년기": "이 시기에는 인생의 후반부를 준비하는 시기입니다."
    }
    return descriptions.get(period, "해당 시기에 대한 분석입니다.")

def analyze_guin(pillars_char: Dict[str, str]) -> Dict[str, Any]:
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

def calculate_guin(pillars_char: Dict[str, str]) -> List[str]:
    """귀인을 계산합니다."""
    # 간단한 귀인 계산 로직
    guin_list = []
    for key, char in pillars_char.items():
        if 'gan' in key:
            guin_type = get_guin_type(char)
            if guin_type:
                guin_list.append(guin_type)
    return guin_list

def get_guin_type(gan: str) -> Optional[str]:
    """천간에 따른 귀인 유형을 반환합니다."""
    guin_map = {
        "甲": "갑자귀인", "乙": "을자귀인", "丙": "병자귀인", "丁": "정자귀인",
        "戊": "무자귀인", "己": "기자귀인", "庚": "경자귀인", "辛": "신자귀인",
        "壬": "임자귀인", "癸": "계자귀인"
    }
    return guin_map.get(gan, None)

def get_guin_description(guin_result: List[str], period: str) -> str:
    """귀인 설명을 반환합니다."""
    descriptions = {
        "초년기": "가족과 선생님의 도움을 받게 됩니다.",
        "청년기": "상사나 멘토의 지도를 받게 됩니다.",
        "중년기": "동료나 파트너의 협력을 받게 됩니다.",
        "장년기": "후배나 제자의 도움을 받게 됩니다."
    }
    return descriptions.get(period, "해당 시기의 귀인 분석입니다.")

def generate_ai_portrait(prompt: str, guin_data: List[str]) -> Optional[str]:
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

def enhance_wealth_analysis(sipsung_result: Dict[str, str]) -> Dict[str, Any]:
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

def enhance_love_analysis(sipsung_result: Dict[str, str]) -> Dict[str, str]:
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

def enhance_career_analysis(sipsung_result: Dict[str, str]) -> Dict[str, Any]:
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

def enhance_health_analysis(sipsung_result: Dict[str, str], pillars_char: Dict[str, str]) -> Dict[str, str]:
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

def generate_comprehensive_report_detailed(pillars_char: Dict[str, str], basic_results: Dict[str, Any], life_flow: Dict[str, Any]) -> Dict[str, Any]:
    """20년 역술가 수준의 상세한 종합 리포트를 생성합니다."""
    
    # 1. 일주 분석
    ilju_analysis = generate_ilju_analysis_detailed(pillars_char)
    
    # 2. 십성 분석
    sipsung_analysis = generate_sipsung_analysis_detailed(basic_results)
    
    # 3. 십이운성 분석
    sibiunseong_analysis = generate_sibiunseong_analysis_detailed(pillars_char, basic_results)
    
    # 4. 십이신살 분석
    sibisinsal_analysis = generate_sibisinsal_analysis_detailed(pillars_char)
    
    # 5. 귀인 분석
    guin_analysis = generate_guin_analysis_detailed(pillars_char)
    
    # 6. 재물운 분석
    wealth_analysis = generate_wealth_analysis_detailed(basic_results)
    
    # 7. 연애운 & 결혼운 분석
    love_analysis = generate_love_analysis_detailed(basic_results)
    
    # 8. 직업운 분석
    career_analysis = generate_career_analysis_detailed(basic_results)
    
    # 9. 건강운 분석
    health_analysis = generate_health_analysis_detailed(basic_results, pillars_char)
    
    # 10. 대운 분석
    daeun_analysis = generate_daeun_analysis_detailed(life_flow)
    
    # 11. 종합 리포트
    final_summary = generate_final_summary_detailed(pillars_char, basic_results, life_flow)
    
    return {
        "ilju_analysis": ilju_analysis,
        "sipsung_analysis": sipsung_analysis,
        "sibiunseong_analysis": sibiunseong_analysis,
        "sibisinsal_analysis": sibisinsal_analysis,
        "guin_analysis": guin_analysis,
        "wealth_analysis": wealth_analysis,
        "love_analysis": love_analysis,
        "career_analysis": career_analysis,
        "health_analysis": health_analysis,
        "daeun_analysis": daeun_analysis,
        "final_summary": final_summary
    }

def generate_ilju_analysis_detailed(pillars_char: Dict[str, str]) -> Dict[str, Any]:
    """일주 분석 - 상세 버전"""
    day_gan = pillars_char.get('day_gan', '')
    day_ji = pillars_char.get('day_ji', '')
    ilju_key = f"{day_gan}{day_ji}"
    
    # 일주 일러스트 생성
    ilju_illustration_prompt = f"Traditional Korean fortune telling illustration showing the day pillar (일주) with {day_gan} day master and {day_ji} earthly branch, mystical atmosphere, traditional Korean art style, detailed and colorful"
    ilju_illustration_url = safe_ai_generation("illustration", ilju_illustration_prompt)
    
    # 일주 데이터 가져오기
    ilju_data = get_cached_data('ilju')
    ilju_info = ilju_data.get(ilju_key, {})
    
    # 성격 장단점
    personality = ilju_info.get('personality', {'pros': [], 'cons': []})
    
    # 동물 특징
    animal = ilju_info.get('animal', {'name': '', 'characteristics': []})
    
    analysis_text = f"""
【일주 분석 - {ilju_key}】

당신의 일주는 {day_gan}{day_ji}입니다. 이는 당신의 핵심 성격과 기질을 나타내는 가장 중요한 요소입니다.

【일주 일러스트】
{ilju_illustration_url if ilju_illustration_url else "일러스트 준비 중"}

【내 성격 장단점】

강점:
{chr(10).join([f"• {pro}" for pro in personality.get('pros', [])])}

주의사항:
{chr(10).join([f"• {con}" for con in personality.get('cons', [])])}

【내 일주 동물 특징】

상징 동물: {animal.get('name', '')}
동물적 특징:
{chr(10).join([f"• {char}" for char in animal.get('characteristics', [])])}

【전문가 해석】
{ilju_info.get('description', '일주 분석을 통해 당신의 기본 성격과 기질을 파악할 수 있습니다.')}

【인생에서의 영향】
1. 기본 성격: 이 일주는 당신의 기본 성격을 형성하는 핵심 요소입니다.
2. 대인관계: 일주의 특성에 따라 특정 유형의 사람들과 잘 어울리거나 갈등할 수 있습니다.
3. 직업적 성향: 일주의 특성은 적합한 직업이나 활동 분야를 결정하는 중요한 요소입니다.
4. 운세의 기반: 일주는 전체 운세의 기반이 되며, 다른 운세 요소들과 조화를 이룹니다.

【전문가 조언】
당신의 일주 특성을 잘 파악하고 긍정적 면모를 최대한 활용하는 것이 중요합니다. 
특히 주의사항에 해당하는 부분들은 미리 대비하여 부정적 영향을 최소화하시기 바랍니다.
"""
    
    return {
        "title": f"일주 분석 - {ilju_key}",
        "content": analysis_text.strip(),
        "illustration_url": ilju_illustration_url,
        "personality": personality,
        "animal": animal
    }

def generate_sipsung_analysis_detailed(basic_results: Dict[str, Any]) -> Dict[str, Any]:
    """십성 분석 - 상세 버전"""
    sipsung_analysis = basic_results.get('sipsung_analysis', {})
    
    # 시기별 성향 분석
    period_analysis = {}
    for period, analysis in sipsung_analysis.items():
        if period != '종합':
            period_analysis[period] = analysis
    
    # 종합 성향 분석
    comprehensive = sipsung_analysis.get('종합', '')
    
    analysis_text = f"""
【십성 분석】

십성은 사주에서 나타나는 열 가지 성격 유형으로, 당신의 성향과 특성을 나타냅니다.

【시기별 성향 분석】

초년기:
{period_analysis.get('연간', '해당 시기의 십성 분석입니다.')}

청년기:
{period_analysis.get('월간', '해당 시기의 십성 분석입니다.')}

중년기:
{period_analysis.get('일간', '해당 시기의 십성 분석입니다.')}

장년기:
{period_analysis.get('시간', '해당 시기의 십성 분석입니다.')}

【종합 성향 분석】

{comprehensive}

【전문가 해석】
십성의 조합을 통해 당신의 성격적 특징, 대인관계, 직업적 성향, 운세의 흐름을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 성격적 특징: 각 십성의 긍정적 면모들이 조화를 이루어 독특한 성격을 형성합니다.
2. 대인관계: 십성의 조합에 따라 특정 유형의 사람들과 잘 어울리거나 갈등할 수 있습니다.
3. 직업적 성향: 십성의 특성에 따라 적합한 직업이나 활동 분야가 결정됩니다.
4. 운세의 흐름: 각 시기별 십성의 변화에 따라 운세의 흐름이 달라집니다.

【전문가 조언】
당신의 십성 조합을 고려할 때, 각 시기의 특성을 잘 파악하고 긍정적 면모를 최대한 활용하는 것이 중요합니다. 
특히 주의사항에 해당하는 부분들은 미리 대비하여 부정적 영향을 최소화하시기 바랍니다.
"""
    
    return {
        "title": "십성 분석",
        "content": analysis_text.strip(),
        "period_analysis": period_analysis,
        "comprehensive": comprehensive
    }

def generate_sibiunseong_analysis_detailed(pillars_char: Dict[str, str], basic_results: Dict[str, Any]) -> Dict[str, Any]:
    """십이운성 분석 - 상세 버전"""
    sibiunseong_analysis = basic_results.get('sibiunseong_analysis', {})
    
    # 시기별 십이운성 분석
    period_analysis = {}
    for period, analysis in sibiunseong_analysis.items():
        if period != '종합':
            period_analysis[period] = analysis
    
    # 종합 십이운성 분석
    comprehensive = sibiunseong_analysis.get('종합', '')
    
    # 십이운성 일러스트 생성
    day_gan = pillars_char.get('day_gan', '')
    sibiunseong_illustration_prompt = f"Traditional Korean fortune telling illustration showing the twelve fortunes (십이운성) with {day_gan} day master, mystical atmosphere, traditional Korean art style, detailed and colorful"
    sibiunseong_illustration_url = safe_ai_generation("illustration", sibiunseong_illustration_prompt)
    
    analysis_text = f"""
【십이운성 분석】

십이운성은 사주에서 나타나는 열두 가지 운세 유형으로, 인생의 각 시기별 운세를 나타냅니다.

【시기별 십이운성 분석】

초년기:
{period_analysis.get('연간', '해당 시기의 십이운성 분석입니다.')}

청년기:
{period_analysis.get('월간', '해당 시기의 십이운성 분석입니다.')}

중년기:
{period_analysis.get('일간', '해당 시기의 십이운성 분석입니다.')}

장년기:
{period_analysis.get('시간', '해당 시기의 십이운성 분석입니다.')}

【종합 십이운성 분석】

{comprehensive}

【나의 십이운성 일러스트 및 분석】

{sibiunseong_illustration_url if sibiunseong_illustration_url else "일러스트 준비 중"}

【전문가 해석】
십이운성의 조합을 통해 당신의 인생 흐름, 성장 단계, 기회와 도전을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 인생의 흐름: 각 시기별 운성의 변화에 따라 인생의 전반적인 흐름이 결정됩니다.
2. 성장 단계: 십이운성은 인생의 성장 단계를 나타내며, 각 시기의 특성을 잘 파악하는 것이 중요합니다.
3. 기회와 도전: 각 운성의 특성에 따라 기회가 되는 시기와 도전이 필요한 시기가 구분됩니다.
4. 준비와 대응: 각 시기의 특성을 미리 파악하고 적절한 준비와 대응을 하는 것이 성공의 열쇠입니다.

【전문가 조언】
당신의 십이운성 조합을 고려할 때, 각 시기의 특성을 잘 파악하고 그에 맞는 적절한 대응을 하는 것이 중요합니다. 
특히 긍정적인 기운이 나타나는 시기에는 적극적으로 활동하고, 도전적인 시기에는 신중하게 대응하시기 바랍니다.

【시기별 권장사항】
• 연간: 장기적인 계획과 목표 설정에 적합한 시기
• 월간: 중기적인 활동과 발전에 집중할 시기  
• 일간: 일상적인 활동과 단기 계획에 적합한 시기
• 시간: 즉각적인 행동과 결정에 영향을 주는 시기
"""
    
    return {
        "title": "십이운성 분석",
        "content": analysis_text.strip(),
        "period_analysis": period_analysis,
        "comprehensive": comprehensive,
        "illustration_url": sibiunseong_illustration_url
    }

def generate_sibisinsal_analysis_detailed(pillars_char: Dict[str, str]) -> Dict[str, Any]:
    """십이신살 분석 - 상세 버전"""
    sibisinsal_analysis = analyze_sibisinsal(pillars_char)
    
    analysis_text = f"""
【십이신살 분석】

십이신살은 사주에서 나타나는 열두 가지 신살 유형으로, 특정 시기의 영향을 나타냅니다.

【시기별 십이신살 분석】

초년기:
{sibisinsal_analysis.get('초년기', '해당 시기의 십이신살 분석입니다.')}

청년기:
{sibisinsal_analysis.get('청년기', '해당 시기의 십이신살 분석입니다.')}

중년기:
{sibisinsal_analysis.get('중년기', '해당 시기의 십이신살 분석입니다.')}

장년기:
{sibisinsal_analysis.get('장년기', '해당 시기의 십이신살 분석입니다.')}

【전문가 해석】
십이신살의 조합을 통해 각 시기별 특별한 영향을 파악할 수 있습니다.

【인생에서의 영향】
1. 초년기: 기본적인 인성과 성격이 형성되는 시기입니다.
2. 청년기: 사회 진출과 인간관계 형성이 중요한 시기입니다.
3. 중년기: 가정과 직장에서의 안정이 중요한 시기입니다.
4. 장년기: 인생의 후반부를 준비하는 시기입니다.

【전문가 조언】
각 시기의 십이신살 특성을 잘 파악하고 적절한 대응을 하는 것이 중요합니다.
"""
    
    return {
        "title": "십이신살 분석",
        "content": analysis_text.strip(),
        "period_analysis": sibisinsal_analysis
    }

def generate_guin_analysis_detailed(pillars_char: Dict[str, str]) -> Dict[str, Any]:
    """귀인 분석 - 상세 버전"""
    guin_analysis = analyze_guin(pillars_char)
    
    # 귀인 초상화 생성
    guin_portrait_prompt = "Traditional Korean noble person portrait, dignified and wise appearance, traditional Korean art style, detailed and colorful"
    guin_portrait_url = safe_ai_generation("portrait", guin_portrait_prompt)
    
    analysis_text = f"""
【귀인 분석】

귀인은 당신의 인생에서 도움을 주는 중요한 사람들을 나타냅니다.

【시기별 귀인 분석】

초년기:
{guin_analysis.get('period_analysis', {}).get('초년기', '해당 시기의 귀인 분석입니다.')}

청년기:
{guin_analysis.get('period_analysis', {}).get('청년기', '해당 시기의 귀인 분석입니다.')}

중년기:
{guin_analysis.get('period_analysis', {}).get('중년기', '해당 시기의 귀인 분석입니다.')}

장년기:
{guin_analysis.get('period_analysis', {}).get('장년기', '해당 시기의 귀인 분석입니다.')}

【종합 귀인 분석】

{guin_analysis.get('comprehensive', '귀인 분석 결과입니다.')}

【귀인 초상화】

{guin_portrait_url if guin_portrait_url else "초상화 준비 중"}

【전문가 해석】
귀인의 조합을 통해 당신의 인생에서 도움을 주는 사람들의 특성을 파악할 수 있습니다.

【인생에서의 영향】
1. 초년기: 가족과 선생님의 도움을 받게 됩니다.
2. 청년기: 상사나 멘토의 지도를 받게 됩니다.
3. 중년기: 동료나 파트너의 협력을 받게 됩니다.
4. 장년기: 후배나 제자의 도움을 받게 됩니다.

【전문가 조언】
각 시기의 귀인 특성을 잘 파악하고 그들과의 관계를 중시하는 것이 중요합니다.
"""
    
    return {
        "title": "귀인 분석",
        "content": analysis_text.strip(),
        "period_analysis": guin_analysis.get('period_analysis', {}),
        "comprehensive": guin_analysis.get('comprehensive', ''),
        "portrait_url": guin_portrait_url
    }

def generate_wealth_analysis_detailed(basic_results: Dict[str, Any]) -> Dict[str, Any]:
    """재물운 분석 - 상세 버전"""
    wealth_analysis = basic_results.get('wealth_luck_analysis', {})
    
    # 재물운 그래프 생성 (간단한 텍스트 기반)
    wealth_graph = generate_wealth_graph()
    
    analysis_text = f"""
【재물운 분석】

재물운은 당신의 재물과 관련된 운세를 나타냅니다.

【전반적인 재물운 흐름】

{wealth_analysis.get('overall_flow', '재물운의 전반적인 흐름을 분석합니다.')}

【내 재물운 특징】

{chr(10).join([f"• {char.get('title', '')}: {char.get('description', '')}" for char in wealth_analysis.get('characteristics', [])])}

【나에게 이익과 손해를 가져다 줄 사람들】

{wealth_analysis.get('people_analysis', '재물운과 관련된 사람 분석입니다.')}

【내 재물운과 잘 맞는 사업 아이템 또는 재테크】

{wealth_analysis.get('business_analysis', '재물운과 관련된 사업/투자 분석입니다.')}

【인생의 재물운 그래프】

{wealth_graph}

【전문가 해석】
재물운의 조합을 통해 당신의 재물 관리 능력과 재물 창출 능력을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 재물 관리: 재물을 효율적으로 관리하고 활용하는 능력이 중요합니다.
2. 재물 창출: 새로운 아이디어로 재물을 만들어내는 창의성이 중요합니다.
3. 재물 활용: 기회를 포착하여 부를 쌓는 능력이 중요합니다.
4. 재물 보호: 안정적인 수입을 통해 삶의 기반을 다지는 것이 중요합니다.

【전문가 조언】
재물운의 특성을 잘 파악하고 적절한 재무 관리와 투자를 하는 것이 중요합니다.
"""
    
    return {
        "title": "재물운 분석",
        "content": analysis_text.strip(),
        "overall_flow": wealth_analysis.get('overall_flow', ''),
        "characteristics": wealth_analysis.get('characteristics', []),
        "people_analysis": wealth_analysis.get('people_analysis', ''),
        "business_analysis": wealth_analysis.get('business_analysis', ''),
        "wealth_graph": wealth_graph
    }

def generate_wealth_graph() -> str:
    """재물운 그래프 생성 (텍스트 기반)"""
    return """
재물운 흐름 그래프:
20대: ⬆️ 상승기 (기반 다지기)
30대: ⬆️⬆️ 급상승기 (재물 축적)
40대: ➡️ 안정기 (재물 관리)
50대: ⬆️ 성숙기 (재물 활용)
60대: ➡️ 유지기 (재물 보호)
"""

def generate_love_analysis_detailed(basic_results: Dict[str, Any]) -> Dict[str, Any]:
    """연애운 & 결혼운 분석 - 상세 버전"""
    love_analysis = basic_results.get('love_luck_analysis', {})
    
    # 운명의 짝 초상화 생성
    partner_portrait_prompt = "Traditional Korean romantic couple portrait, destined partner, traditional Korean art style, detailed and colorful"
    partner_portrait_url = safe_ai_generation("portrait", partner_portrait_prompt)
    
    analysis_text = f"""
【연애운 & 결혼운 분석】

연애운과 결혼운은 당신의 사랑과 관련된 운세를 나타냅니다.

【나의 전반적인 연애 성향】

{love_analysis.get('overall_tendency', '연애 성향 분석입니다.')}

【내 운명의 짝 소개】

{love_analysis.get('destiny_partner', '운명의 짝에 대한 분석입니다.')}

【이성에게 사랑받기 위한 나의 부족한 점 & 개선점】

{love_analysis.get('improvement_points', '연애에서의 개선점 분석입니다.')}

【내 애정운 전선, 흐름】

{love_analysis.get('flow_analysis', '애정운의 흐름 분석입니다.')}

【나의 연애운이 높은 시기와 장소】

{love_analysis.get('timing_location', '연애운이 높은 시기와 장소 분석입니다.')}

【운명의 짝 초상화 및 분석】

{partner_portrait_url if partner_portrait_url else "초상화 준비 중"}

【전문가 해석】
연애운과 결혼운의 조합을 통해 당신의 사랑과 관련된 운세를 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 연애 스타일: 당신의 연애 스타일과 선호하는 관계 유형을 나타냅니다.
2. 운명의 짝: 당신과 잘 맞는 상대방의 특성을 나타냅니다.
3. 개선점: 연애에서 성공하기 위해 보완해야 할 점을 나타냅니다.
4. 시기와 장소: 연애운이 높은 시기와 장소를 나타냅니다.

【전문가 조언】
연애운의 특성을 잘 파악하고 적절한 대응을 하는 것이 중요합니다.
"""
    
    return {
        "title": "연애운 & 결혼운 분석",
        "content": analysis_text.strip(),
        "overall_tendency": love_analysis.get('overall_tendency', ''),
        "destiny_partner": love_analysis.get('destiny_partner', ''),
        "improvement_points": love_analysis.get('improvement_points', ''),
        "flow_analysis": love_analysis.get('flow_analysis', ''),
        "timing_location": love_analysis.get('timing_location', ''),
        "partner_portrait_url": partner_portrait_url
    }

def generate_career_analysis_detailed(basic_results: Dict[str, Any]) -> Dict[str, Any]:
    """직업운 분석 - 상세 버전"""
    career_analysis = basic_results.get('career_luck_analysis', {})
    
    analysis_text = f"""
【직업운 분석】

직업운은 당신의 직업과 관련된 운세를 나타냅니다.

【나와 잘맞는 직업/직장】

{chr(10).join([f"• {job}" for job in career_analysis.get('suitable_jobs', [])])}

【사업 vs 직장 나에겐 뭐가 맞을까 분석】

{career_analysis.get('business_vs_job', '사업과 직장 비교 분석입니다.')}

【성공적인 직장생활을 위한 조언】

{career_analysis.get('advice', '직장생활을 위한 조언입니다.')}

【주의해야 할 사람 분석】

{career_analysis.get('caution_people', '직장에서 주의해야 할 사람 분석입니다.')}

【전문가 해석】
직업운의 조합을 통해 당신의 적합한 직업과 성공 가능성을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 적합한 직업: 당신에게 잘 맞는 직업이나 활동 분야를 나타냅니다.
2. 사업 vs 직장: 사업과 직장 중 어느 것이 더 적합한지 나타냅니다.
3. 성공 요인: 직장에서 성공하기 위한 중요한 요소들을 나타냅니다.
4. 주의사항: 직장에서 주의해야 할 사람이나 상황을 나타냅니다.

【전문가 조언】
직업운의 특성을 잘 파악하고 적절한 직업 선택과 발전을 하는 것이 중요합니다.
"""
    
    return {
        "title": "직업운 분석",
        "content": analysis_text.strip(),
        "suitable_jobs": career_analysis.get('suitable_jobs', []),
        "business_vs_job": career_analysis.get('business_vs_job', ''),
        "advice": career_analysis.get('advice', ''),
        "caution_people": career_analysis.get('caution_people', '')
    }

def generate_health_analysis_detailed(basic_results: Dict[str, Any], pillars_char: Dict[str, str]) -> Dict[str, Any]:
    """건강운 분석 - 상세 버전"""
    health_analysis = basic_results.get('health_luck_analysis', {})
    
    analysis_text = f"""
【건강운 분석】

건강운은 당신의 건강과 관련된 운세를 나타냅니다.

【타고난 체질과 건강 상태 브리핑】

{health_analysis.get('constitution', '체질과 건강 상태 분석입니다.')}

【부상 위험 있는 신체부위나 조심해야 할 질병】

{chr(10).join([f"• {point}" for point in health_analysis.get('weak_points', [])])}

【나와 잘 맞는 운동은?】

{health_analysis.get('suitable_exercise', '적합한 운동 분석입니다.')}

【시기에 따른 건강운】

{health_analysis.get('timing_analysis', '시기별 건강운 분석입니다.')}

【전문가 해석】
건강운의 조합을 통해 당신의 건강 상태와 관리 방법을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 체질: 당신의 타고난 체질과 건강 상태를 나타냅니다.
2. 주의사항: 건강에 주의해야 할 부분들을 나타냅니다.
3. 적합한 운동: 당신에게 잘 맞는 운동을 나타냅니다.
4. 시기별 관리: 각 시기별 건강 관리 방법을 나타냅니다.

【전문가 조언】
건강운의 특성을 잘 파악하고 적절한 건강 관리를 하는 것이 중요합니다.
"""
    
    return {
        "title": "건강운 분석",
        "content": analysis_text.strip(),
        "constitution": health_analysis.get('constitution', ''),
        "weak_points": health_analysis.get('weak_points', []),
        "suitable_exercise": health_analysis.get('suitable_exercise', ''),
        "timing_analysis": health_analysis.get('timing_analysis', '')
    }

def generate_daeun_analysis_detailed(life_flow: Dict[str, Any]) -> Dict[str, Any]:
    """대운 분석 - 상세 버전"""
    analysis_text = f"""
【대운 분석】

대운은 당신의 인생에서 10년 단위로 변화하는 운세를 나타냅니다.

【90세까지의 대운】

{chr(10).join([f"• {period.get('period', '')}: {period.get('age_range', '')} - {period.get('status', '')}" for period in life_flow.get('daeun_periods', [])])}

【향후 5년간의 연운과 삼재】

{chr(10).join([f"• {year.get('year', '')}: {year.get('status', '')}" for year in life_flow.get('seun_periods', [])])}

【향후 5년 동안의 연운】

{life_flow.get('future_outlook', '향후 전망 분석입니다.')}

【곧 맞딱뜨릴 삼재】

{chr(10).join([f"• {point.get('age', '')}: {point.get('description', '')}" for point in life_flow.get('change_points', [])])}

【전문가 해석】
대운의 조합을 통해 당신의 인생 흐름과 중요한 변화점을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 대운: 10년 단위로 변화하는 운세가 인생에 큰 영향을 미칩니다.
2. 세운: 1년 단위로 변화하는 운세가 당해의 운세를 결정합니다.
3. 변화점: 인생에서 중요한 변화가 일어나는 시기를 나타냅니다.
4. 미래 전망: 앞으로의 인생 흐름을 예측할 수 있습니다.

【전문가 조언】
대운의 특성을 잘 파악하고 적절한 준비와 대응을 하는 것이 중요합니다.
"""
    
    return {
        "title": "대운 분석",
        "content": analysis_text.strip(),
        "daeun_periods": life_flow.get('daeun_periods', []),
        "seun_periods": life_flow.get('seun_periods', []),
        "change_points": life_flow.get('change_points', []),
        "future_outlook": life_flow.get('future_outlook', '')
    }

def generate_final_summary_detailed(pillars_char: Dict[str, str], basic_results: Dict[str, Any], life_flow: Dict[str, Any]) -> Dict[str, Any]:
    """종합 리포트 - 상세 버전"""
    analysis_text = f"""
【종합 리포트】

20년 역술가의 관점에서 당신의 사주를 종합적으로 분석한 결과입니다.

【사주 기본 정보】
• 일주: {pillars_char.get('day_gan', '')}{pillars_char.get('day_ji', '')}
• 사주 구성: {pillars_char.get('year_gan', '')}{pillars_char.get('year_ji', '')}년 {pillars_char.get('month_gan', '')}{pillars_char.get('month_ji', '')}월 {pillars_char.get('day_gan', '')}{pillars_char.get('day_ji', '')}일 {pillars_char.get('hour_gan', '')}{pillars_char.get('hour_ji', '')}시

【핵심 분석 요약】

1. 성격적 특징
당신의 사주는 {pillars_char.get('day_gan', '')}일주의 특성을 기본으로 하여 독특한 성격을 형성합니다.

2. 대인관계 분석
사주에서 나타나는 십성과 운성의 조합을 보면, 특정 유형의 사람들과 잘 어울리며, 특정 시기에는 대인관계에서 특별한 변화가 있을 수 있습니다.

3. 직업적 성향
일주의 특성과 십성의 조합을 고려할 때, 특정 분야의 직업이나 활동이 적합합니다.

4. 운세의 흐름
십이운성의 조합을 보면, 특정 시기의 기운이 강하게 나타나는 시기가 있으며, 이 시기에는 중요한 변화가 있을 수 있습니다.

【전문가 권장사항】

1. 성격 개발
• 강점 활용: 사주의 긍정적 면모를 최대한 활용하세요.
• 약점 보완: 주의사항에 해당하는 부분들을 미리 대비하여 부정적 영향을 최소화하세요.

2. 대인관계 관리
• 적합한 관계: 특정 유형의 사람들과의 관계를 중시하세요.
• 갈등 해결: 특정 시기의 기운이 나타나는 시기에는 대인관계에 특별히 주의하세요.

3. 직업적 발전
• 적합한 분야: 사주 특성과 관련된 직업 분야를 고려하세요.
• 발전 방향: 특정 분야의 특성을 활용한 발전 방향을 모색하세요.

4. 운세 활용
• 긍정적 시기: 긍정적인 기운이 나타나는 시기에는 적극적으로 활동하세요.
• 주의 시기: 도전적인 기운이 나타나는 시기에는 신중하게 대응하세요.

【미래 전망】
당신의 사주를 종합적으로 분석한 결과, 사주의 긍정적 면모를 잘 활용하면 특정 분야에서 큰 성공을 거둘 수 있을 것으로 보입니다. 
특히 특정 시기의 기운이 강하게 나타나는 시기에는 중요한 기회가 있을 수 있으니 미리 준비하시기 바랍니다.

이상의 분석은 20년 역술가의 경험을 바탕으로 한 전문적인 해석입니다. 
당신의 사주 특성을 잘 파악하고 긍정적 면모를 최대한 활용하여 행복하고 성공적인 인생을 살아가시기 바랍니다.
"""
    
    return {
        "title": "종합 리포트",
        "content": analysis_text.strip()
    }

def analyze_sibiunseong(pillars_char: Dict[str, str]) -> Dict[str, str]:
    """십이운성을 전문적으로 분석합니다."""
    sibiunseong_data = get_cached_data('sibiunseong')
    
    if not sibiunseong_data:
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
    
    # 각 시기별 상세 분석
    for period, unseong_name in sibiunseong_raw.items():
        # 영어 키를 한글로 변환
        korean_period = period_mapping.get(period, period)
        unseong_info = sibiunseong_data.get(unseong_name, {})
        
        # 전문적인 분석 텍스트 생성
        period_analysis = f"""
당신의 {korean_period} 시기는 '{unseong_name}'의 기운입니다.

【{unseong_name}의 기본 성향】
• 핵심 키워드: {unseong_info.get('keyword', '')}
• 상세 설명: {unseong_info.get('description', '')}

【{korean_period} 시기별 영향】
이 시기에는 {unseong_name}의 기운이 강하게 나타나며, {unseong_info.get('keyword', '')}와 관련된 일들이 많이 발생할 수 있습니다. 
특히 {unseong_info.get('description', '')}의 특징이 두드러지게 나타나므로, 이 시기의 특성을 잘 활용하시기 바랍니다.

【전문가 조언】
{korean_period} 시기의 {unseong_name} 기운을 고려할 때, {unseong_info.get('keyword', '')}와 관련된 활동이나 계획을 세우는 것이 좋습니다. 
이 시기의 특성을 잘 파악하고 적극적으로 활용하면 더욱 좋은 결과를 얻을 수 있습니다.
"""
        analysis[korean_period] = period_analysis.strip()
    
    # 종합 분석
    comprehensive_parts = []
    for period, unseong_name in sibiunseong_raw.items():
        korean_period = period_mapping.get(period, period)
        unseong_info = sibiunseong_data.get(unseong_name, {})
        comprehensive_parts.append(f"{korean_period}: {unseong_name} - {unseong_info.get('keyword', '')}")
    
    comprehensive_analysis = f"""
【십이운성 종합 분석】

당신의 사주에서 나타나는 십이운성의 조합은 다음과 같습니다:
{', '.join(comprehensive_parts)}

이러한 십이운성 조합은 당신의 인생에서 다음과 같은 특징을 나타냅니다:

1. 인생의 흐름: 각 시기별 운성의 변화에 따라 인생의 전반적인 흐름이 결정됩니다.
2. 성장 단계: 십이운성은 인생의 성장 단계를 나타내며, 각 시기의 특성을 잘 파악하는 것이 중요합니다.
3. 기회와 도전: 각 운성의 특성에 따라 기회가 되는 시기와 도전이 필요한 시기가 구분됩니다.
4. 준비와 대응: 각 시기의 특성을 미리 파악하고 적절한 준비와 대응을 하는 것이 성공의 열쇠입니다.

【전문가 조언】
당신의 십이운성 조합을 고려할 때, 각 시기의 특성을 잘 파악하고 그에 맞는 적절한 대응을 하는 것이 중요합니다. 
특히 긍정적인 기운이 나타나는 시기에는 적극적으로 활동하고, 도전적인 시기에는 신중하게 대응하시기 바랍니다.

【시기별 권장사항】
• 연간: 장기적인 계획과 목표 설정에 적합한 시기
• 월간: 중기적인 활동과 발전에 집중할 시기  
• 일간: 일상적인 활동과 단기 계획에 적합한 시기
• 시간: 즉각적인 행동과 결정에 영향을 주는 시기
"""
    
    analysis['종합'] = comprehensive_analysis.strip()
    return analysis

def analyze_sipsung_by_period(sipsung_result: Dict[str, str]) -> Dict[str, str]:
    """십성 분석 결과를 시기별로 전문적으로 분석합니다."""
    sipsung_data = get_cached_data('sipsung')
    
    if not sipsung_data:
        return {"error": "십성 데이터를 불러올 수 없습니다."}
    
    analysis = {}
    periods = ['year', 'month', 'day', 'hour']
    period_names = ['연간', '월간', '일간', '시간']
    
    # 각 시기별 상세 분석
    for i, period in enumerate(periods):
        if period in sipsung_result:
            sipsung_name = sipsung_result[period]
            sipsung_info = sipsung_data.get(sipsung_name, {})
            
            # 전문적인 분석 텍스트 생성
            period_analysis = f"""
당신의 {period_names[i]} 십성은 '{sipsung_name}'입니다.

【{sipsung_name}의 기본 성향】
• 핵심 키워드: {sipsung_info.get('keyword', '')}
• 긍정적 특징: {sipsung_info.get('positive', '')}
• 주의사항: {sipsung_info.get('negative', '')}

【{period_names[i]} 시기별 영향】
이 시기에는 {sipsung_name}의 기운이 강하게 나타나며, {sipsung_info.get('keyword', '')}와 관련된 일들이 많이 발생할 수 있습니다. 
특히 {sipsung_info.get('positive', '')}의 면모가 두드러지게 나타나므로, 이 부분을 잘 활용하시기 바랍니다.
"""
            analysis[period_names[i]] = period_analysis.strip()
    
    # 종합 분석
    comprehensive_parts = []
    for i, period in enumerate(periods):
        if period in sipsung_result:
            sipsung_name = sipsung_result[period]
            sipsung_info = sipsung_data.get(sipsung_name, {})
            comprehensive_parts.append(f"{period_names[i]}: {sipsung_name} - {sipsung_info.get('keyword', '')}")
    
    comprehensive_analysis = f"""
【십성 종합 분석】

당신의 사주에서 나타나는 십성의 조합은 다음과 같습니다:
{', '.join(comprehensive_parts)}

이러한 십성 조합은 당신의 인생에서 다음과 같은 특징을 나타냅니다:

1. 성격적 특징: 각 십성의 긍정적 면모들이 조화를 이루어 독특한 성격을 형성합니다.
2. 대인관계: 십성의 조합에 따라 특정 유형의 사람들과 잘 어울리거나 갈등할 수 있습니다.
3. 직업적 성향: 십성의 특성에 따라 적합한 직업이나 활동 분야가 결정됩니다.
4. 운세의 흐름: 각 시기별 십성의 변화에 따라 운세의 흐름이 달라집니다.

【전문가 조언】
당신의 십성 조합을 고려할 때, 각 시기의 특성을 잘 파악하고 긍정적 면모를 최대한 활용하는 것이 중요합니다. 
특히 주의사항에 해당하는 부분들은 미리 대비하여 부정적 영향을 최소화하시기 바랍니다.
"""
    
    analysis['종합'] = comprehensive_analysis.strip()
    return analysis

def get_ilju_analysis_data(ilju_key: str) -> Dict[str, Any]:
    """일주 분석 데이터를 전문적으로 가져옵니다."""
    ilju_data = get_cached_data('ilju')
    
    if not ilju_data:
        return {
            "title": "일주 분석",
            "description": "일주 분석 데이터를 불러올 수 없습니다.",
            "personality": {"pros": [], "cons": []},
            "animal": {"name": "", "characteristics": []}
        }
    
    ilju_info = ilju_data.get(ilju_key, {
        "title": "일주 분석",
        "description": "해당 일주에 대한 데이터는 아직 준비되지 않았습니다.",
        "personality": {"pros": [], "cons": []},
        "animal": {"name": "", "characteristics": []}
    })
    
    # 전문적인 분석 텍스트 생성
    if ilju_info.get("title") != "일주 분석":
        detailed_analysis = f"""
【{ilju_info.get('title', '일주 분석')}】

{ilju_info.get('description', '')}

【성격적 특징】
• 강점: {', '.join(ilju_info.get('personality', {}).get('pros', []))}
• 주의사항: {', '.join(ilju_info.get('personality', {}).get('cons', []))}

【동물적 특성】
• 상징 동물: {ilju_info.get('animal', {}).get('name', '')}
• 동물적 특징: {', '.join(ilju_info.get('animal', {}).get('characteristics', []))}

【전문가 해석】
이 일주는 {ilju_info.get('description', '')}의 특성을 가지고 있습니다. 
특히 {', '.join(ilju_info.get('personality', {}).get('pros', []))}의 면모가 두드러지게 나타나며, 
이는 당신의 인생에서 큰 강점이 될 수 있습니다.

【인생에서의 영향】
1. 성격 형성: 이 일주의 특성은 당신의 기본 성격을 형성하는 중요한 요소입니다.
2. 대인관계: 일주의 특성에 따라 특정 유형의 사람들과 잘 어울리거나 갈등할 수 있습니다.
3. 직업적 성향: 일주의 특성은 적합한 직업이나 활동 분야를 결정하는 중요한 요소입니다.
4. 운세의 기반: 일주는 전체 운세의 기반이 되며, 다른 운세 요소들과 조화를 이룹니다.

【전문가 조언】
당신의 일주 특성을 잘 파악하고 긍정적 면모를 최대한 활용하는 것이 중요합니다. 
특히 주의사항에 해당하는 부분들은 미리 대비하여 부정적 영향을 최소화하시기 바랍니다.
"""
        
        return {
            "title": ilju_info.get('title', '일주 분석'),
            "description": detailed_analysis.strip(),
            "personality": ilju_info.get('personality', {"pros": [], "cons": []}),
            "animal": ilju_info.get('animal', {"name": "", "characteristics": []})
        }
    
    return ilju_info
