# 건강운 분석 모듈
class HealthAnalyzer:
    """건강운 분석을 담당하는 클래스"""
    
    OHENG_GAN = {
        "갑": "목", "을": "목", "병": "화", "정": "화", "무": "토", 
        "기": "토", "경": "금", "신": "금", "임": "수", "계": "수"
    }
    OHENG_JIJI = {
        "자": "수", "축": "토", "인": "목", "묘": "목", "진": "토", "사": "화", 
        "오": "화", "미": "토", "신": "금", "유": "금", "술": "토", "해": "수"
    }

    def analyze(self, saju_pillars, sipsung_data):
        """건강운 분석 수행"""
        try:
            oheng_analysis = self._analyze_oheng_health(saju_pillars)
            health_style = self._get_health_style(oheng_analysis)
            
            return {
                'title': f"{health_style['name']} ({health_style['keyword']})",
                'description': health_style['description'],
                'body_constitution': self._generate_body_constitution_info(oheng_analysis),
                'vulnerable_areas': ", ".join(health_style['vulnerable_areas']),
                'suitable_exercise': self._get_suitable_exercise(health_style['name']),
                'period_analysis': self._generate_period_analysis(oheng_analysis),
                'management_advice': self._generate_management_advice(health_style, oheng_analysis)
            }
        except Exception as e:
            print(f"건강운 분석 중 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._get_default_analysis()

    def _analyze_oheng_health(self, saju_pillars):
        """오행 기반 건강 분석"""
        oheng_count = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
        
        for position in ['year', 'month', 'day', 'hour']:
            pillar = saju_pillars.get(position, {})
            gan = pillar.get('gan')
            jiji = pillar.get('ji')
            
            if gan and gan in self.OHENG_GAN:
                oheng_count[self.OHENG_GAN[gan]] += 1
            if jiji and jiji in self.OHENG_JIJI:
                oheng_count[self.OHENG_JIJI[jiji]] += 1
        
        dominant = max(oheng_count, key=oheng_count.get) if any(oheng_count.values()) else None
        weak = min(oheng_count, key=oheng_count.get) if any(oheng_count.values()) else None
        
        return {'balance': oheng_count, 'dominant': dominant, 'weak': weak}

    def _get_health_style(self, oheng_analysis):
        """오행 균형에 따른 건강 스타일 결정"""
        dominant = oheng_analysis['dominant']
        styles = {
            '목': {'name': '에너제틱 목(木)형', 'keyword': '활동과 성장', 
                   'description': '생명력과 성장의 기운이 강해 활력이 넘칩니다. 하지만 과도한 에너지로 간과 담에 부담이 갈 수 있으니, 스트레스 관리가 중요합니다.', 
                   'vulnerable_areas': ['간', '담낭', '근육', '눈']},
            '화': {'name': '열정적인 화(火)형', 'keyword': '열정과 순환', 
                   'description': '불처럼 뜨거운 열정을 지녔지만, 심장과 혈관 계통에 과부하가 걸리기 쉽습니다. 흥분을 가라앉히는 명상과 충분한 수분 섭취가 필요합니다.', 
                   'vulnerable_areas': ['심장', '소장', '혈관', '혀']},
            '토': {'name': '안정적인 토(土)형', 'keyword': '소화와 균형', 
                   'description': '중심을 잡는 흙의 기운으로 안정적이지만, 소화기 계통이 약할 수 있습니다. 규칙적인 식사와 소화가 잘되는 음식이 건강의 핵심입니다.', 
                   'vulnerable_areas': ['위', '비장', '췌장', '입']},
            '금': {'name': '정제된 금(金)형', 'keyword': '호흡과 질서', 
                   'description': '날카롭고 정제된 기운으로 호흡기가 예민할 수 있습니다. 건조한 환경을 피하고, 맑은 공기를 마시는 것이 중요합니다.', 
                   'vulnerable_areas': ['폐', '대장', '코', '피부']},
            '수': {'name': '지혜로운 수(水)형', 'keyword': '흐름과 저장', 
                   'description': '물처럼 흐르는 유연함과 지혜를 가졌지만, 신장과 방광 기능이 약해지기 쉽습니다. 몸을 따뜻하게 하고 충분한 휴식을 취하는 것이 좋습니다.', 
                   'vulnerable_areas': ['신장', '방광', '뼈', '귀']}
        }
        return styles.get(dominant, styles['토']) # 기본값은 토(土)형

    def _generate_body_constitution_info(self, oheng_analysis):
        """체질 정보 생성"""
        dominant_oheng = oheng_analysis['dominant']
        weak_oheng = oheng_analysis['weak']
        return f"가장 강한 기운은 '{dominant_oheng}'이며, 가장 약한 기운은 '{weak_oheng}'입니다. 강한 기운은 장점이 되지만 과해지면 병이 될 수 있고, 약한 기운은 보완이 필요한 지점입니다."

    def _get_suitable_exercise(self, style_name):
        """건강 스타일에 맞는 운동 추천"""
        exercise_map = {
            '에너제틱 목(木)형': '조깅, 등산 등 야외 유산소 운동',
            '열정적인 화(火)형': '수영, 요가 등 차분한 운동',
            '안정적인 토(土)형': '필라테스, 걷기 등 코어 강화 운동',
            '정제된 금(金)형': '심호흡을 동반한 스트레칭, 태극권',
            '지혜로운 수(水)형': '아쿠아로빅, 가벼운 근력 운동'
        }
        return exercise_map.get(style_name, "자신에게 맞는 꾸준한 운동이 중요합니다.")

    def _generate_period_analysis(self, oheng_analysis):
        """시기별 건강운 분석"""
        weak_oheng = oheng_analysis['weak']
        period_advice = {
            '목': '봄철, 특히 아침에 컨디션 난조를 겪을 수 있으니 주의하세요.',
            '화': '여름철, 더운 날씨에 심장에 부담이 갈 수 있습니다.',
            '토': '환절기에 소화 기능이 떨어지기 쉬우니 식중독에 유의하세요.',
            '금': '가을철, 건조한 날씨에 호흡기 질환을 조심해야 합니다.',
            '수': '겨울철, 추위로 인해 신장 및 방광 기능이 약해질 수 있습니다.'
        }
        return f"일반적으로, {period_advice.get(weak_oheng, '규칙적인 생활 습관으로 건강을 유지하는 것이 중요합니다.')}"

    def _generate_management_advice(self, health_style, oheng_analysis):
        """종합 건강 관리 조언 생성"""
        weak_oheng = oheng_analysis['weak']
        oheng_food = {
            '목': '신 맛 (레몬, 키위), 푸른색 채소 (시금치, 브로콜리)',
            '화': '쓴 맛 (도라지, 더덕), 붉은색 음식 (토마토, 비트)',
            '토': '단 맛 (고구마, 단호박), 노란색 음식 (옥수수, 파프리카)',
            '금': '매운 맛 (마늘, 생강), 흰색 음식 (무, 양파)',
            '수': '짠 맛 (해조류), 검은색 음식 (검은콩, 흑미)'
        }
        advice = f"'{health_style['name']}'인 당신은 '{health_style['keyword']}'을 중심으로 건강을 관리해야 합니다. "
        advice += f"특히 취약한 '{', '.join(health_style['vulnerable_areas'])}'에 신경을 쓰고, '{self._get_suitable_exercise(health_style['name'])}'으로 신체를 단련하세요. "
        advice += f"식단에서는 약한 기운인 '{weak_oheng}'을 보완하기 위해 '{oheng_food.get(weak_oheng)}'을 섭취하는 것이 좋습니다."
        return advice

    def _get_default_analysis(self):
        """기본 분석 결과 반환"""
        return {
            'title': '건강운 분석',
            'description': '건강운 분석 데이터를 준비 중입니다.',
            'body_constitution': '체질 정보를 준비 중입니다.',
            'vulnerable_areas': '취약 부위를 분석 중입니다.',
            'suitable_exercise': '추천 운동을 준비 중입니다.',
            'period_analysis': '시기별 분석을 준비 중입니다.',
            'management_advice': '건강 관리 조언을 준비 중입니다.'
        }
