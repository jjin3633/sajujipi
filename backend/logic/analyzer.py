    import json
    import os
    from korean_lunar_calendar import KoreanLunarCalendar

    CHEONGAN = "갑을병정무기경신임계"
    JIJI = "자축인묘진사오미신유술해"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'ilju_data.json')

    def get_saju_details(year, month, day, hour, minute):
        calendar = KoreanLunarCalendar()
        calendar.setSolarDate(year, month, day)

        ganji_year = calendar.getGanjiString()
        
        gan_month_map = {1: '병', 2: '정', 3: '무', 4: '기', 5: '경', 6: '신', 7: '임', 8: '계', 9: '갑', 10: '을', 11: '병', 12: '정'}
        gan_month = gan_month_map.get((year % 10), '갑')
        ji_month = JIJI[calendar.lunar_month -1]
        ganji_month = f"{gan_month}{ji_month}"
        ganji_day = calendar.getGanjiString(True)

        day_gan = ganji_day[0]
        hour_index = (hour + 1) // 2 % 12
        gan_hour_start_map = {'갑': '갑', '을': '병', '병': '무', '정': '경', '무': '임', '기': '갑', '경': '병', '신': '무', '임': '경', '계': '임'}
        start_gan_index = CHEONGAN.find(gan_hour_start_map.get(day_gan))
        gan_hour = CHEONGAN[(start_gan_index + hour_index) % 10]
        ji_hour = JIJI[hour_index]
        ganji_hour = f"{gan_hour}{ji_hour}"

        ilju_key = ganji_day.split('(')[0]
        ilju_analysis_data = get_ilju_analysis_data(ilju_key)

        return {
            "year_pillar": ganji_year,
            "month_pillar": ganji_month,
            "day_pillar": ganji_day,
            "hour_pillar": ganji_hour,
            "ilju_analysis": ilju_analysis_data
        }

    def get_ilju_analysis_data(ilju_key):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                all_ilju_data = json.load(f)
            return all_ilju_data.get(ilju_key, {
                "title": f"{ilju_key} 일주 분석",
                "description": f"'{ilju_key}' 일주 데이터는 아직 준비되지 않았습니다.",
                "pros": [], "cons": [], "animal": ""
            })
        except FileNotFoundError:
            # 이 부분은 웹 서버 환경에서는 발생하지 않아야 하지만, 로컬 테스트를 위해 유지합니다.
            # 실제 서버에서는 파일이 항상 존재해야 합니다.
            return {"error": "데이터 파일을 찾을 수 없습니다: " + DATA_FILE}
        except json.JSONDecodeError:
            return {"error": "데이터 파일 형식 오류"}