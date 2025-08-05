# 건강운 분석 모듈
class HealthAnalyzer:
    """건강운 분석을 담당하는 클래스"""
    
    # 오행 데이터
    OHENG_GAN = {
        "갑": "목", "을": "목", "병": "화", "정": "화",
        "무": "토", "기": "토", "경": "금", "신": "금",
        "임": "수", "계": "수"
    }
    
    OHENG_JIJI = {
        "자": "수", "축": "토", "인": "목", "묘": "목",
        "진": "토", "사": "화", "오": "화", "미": "토",
        "신": "금", "유": "금", "술": "토", "해": "수"
    }
    
    def analyze(self, saju_pillars, sipsung_data):
        """건강운 분석 수행"""
        try:
            # 십성 리스트 생성
            sipsung_list = list(sipsung_data.values()) if isinstance(sipsung_data, dict) else []
            
            # 건강 관련 십성 분석
            siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")
            gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")
            jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")
            
            # 건강 스타일 분석
            health_analysis = self._analyze_health_style(
                siksang_count, gwanseong_count, jaeseong_count
            )
            
            # 오행 분석
            oheng_analysis = self._analyze_oheng_health(saju_pillars)
            
            # 적합한 운동 분석
            suitable_exercise = self._get_suitable_exercise(health_analysis['style'])
            
            # 관리 조언 생성
            management_advice = self._generate_management_advice(
                health_analysis, oheng_analysis
            )
            
            return {
                'title': health_analysis['style'],
                'description': health_analysis['description'],
                'body_constitution': health_analysis['description'],
                'vulnerable_areas': ', '.join(health_analysis['weak_points']),
                'suitable_exercise': suitable_exercise,
                'period_analysis': self._generate_period_analysis(),
                'management_advice': management_advice
            }
        except Exception as e:
            print(f"건강운 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _analyze_health_style(self, siksang_count, gwanseong_count, jaeseong_count):
        """건강 스타일 분석"""
        if siksang_count > 2:
            return {
                'style': '활발한 신진대사형',
                'description': '사주에 소화와 신진대사를 나타내는 식상이 강하여, 활발한 신진대사를 가지고 있습니다. 하지만 과식이나 불규칙한 식사로 소화불량이 생길 수 있으니 주의해야 합니다. 규칙적인 식사와 적절한 운동이 중요합니다.',
                'weak_points': ['소화기', '위장', '대사'],
                'strong_points': ['활력', '에너지', '회복력']
            }
        elif siksang_count == 0:
            return {
                'style': '안정적 체질형',
                'description': '사주에 식상이 부족하여 안정적인 체질을 가지고 있습니다. 소화가 느리고 식욕이 부족할 수 있으니, 소화가 잘 되는 음식을 섭취하고 규칙적인 식사가 중요합니다. 천천히 꾸준히 관리하는 것이 좋습니다.',
                'weak_points': ['소화기', '식욕', '대사'],
                'strong_points': ['안정성', '지속력', '균형감']
            }
        elif gwanseong_count > 2:
            return {
                'style': '강한 골격형',
                'description': '사주에 관절과 뼈를 나타내는 관성이 강하여, 튼튼한 골격을 가지고 있습니다. 하지만 과도한 운동이나 무리한 활동으로 관절에 부담이 갈 수 있으니 주의해야 합니다. 적절한 스트레칭과 관절 관리가 중요합니다.',
                'weak_points': ['관절', '뼈', '인대'],
                'strong_points': ['골격', '지구력', '체력']
            }
        elif gwanseong_count == 0:
            return {
                'style': '유연한 체질형',
                'description': '사주에 관성이 부족하여 유연한 체질을 가지고 있습니다. 관절이 약하거나 골다공증이 생길 수 있으니, 칼슘 섭취와 가벼운 운동이 중요합니다. 요가나 스트레칭 같은 유연성 운동이 도움이 됩니다.',
                'weak_points': ['뼈', '관절', '골격'],
                'strong_points': ['유연성', '민첩성', '회복력']
            }
        elif jaeseong_count > 2:
            return {
                'style': '순환계 활발형',
                'description': '사주에 순환계를 나타내는 재성이 강하여, 활발한 혈액순환을 가지고 있습니다. 하지만 스트레스나 과로로 혈압이 올라갈 수 있으니 주의해야 합니다. 규칙적인 생활과 스트레스 관리가 중요합니다.',
                'weak_points': ['혈압', '순환계', '피부'],
                'strong_points': ['혈액순환', '활력', '에너지']
            }
        elif jaeseong_count == 0:
            return {
                'style': '안정적 순환형',
                'description': '사주에 재성이 부족하여 안정적인 순환계를 가지고 있습니다. 빈혈이나 혈액순환이 느릴 수 있으니, 철분 섭취와 가벼운 운동이 중요합니다. 따뜻한 음식과 규칙적인 생활이 도움이 됩니다.',
                'weak_points': ['빈혈', '혈액순환', '체온'],
                'strong_points': ['안정성', '지속력', '균형감']
            }
        else:
            return {
                'style': '균형잡힌 건강형',
                'description': '사주에 건강 관련 기운이 균형잡혀 있어, 전반적으로 건강한 체질을 가지고 있습니다. 하지만 나이에 따라 주의해야 할 부분이 있으니, 정기적인 건강검진과 예방 관리가 중요합니다.',
                'weak_points': ['나이별 변화', '예방 관리'],
                'strong_points': ['균형감', '적응력', '회복력']
            }
    
    def _analyze_oheng_health(self, saju_pillars):
        """오행 기반 건강 분석"""
        # 오행별 개수 계산
        oheng_count = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
        
        # 천간 분석
        for position in ['year', 'month', 'day', 'hour']:
            gan = saju_pillars.get(position, '')[:1]  # 첫 글자가 천간
            if gan in self.OHENG_GAN:
                oheng = self.OHENG_GAN[gan]
                oheng_count[oheng] += 1
        
        # 지지 분석
        for position in ['year', 'month', 'day', 'hour']:
            ji = saju_pillars.get(position, '')[1:2] if len(saju_pillars.get(position, '')) > 1 else ''
            if ji in self.OHENG_JIJI:
                oheng = self.OHENG_JIJI[ji]
                oheng_count[oheng] += 1
        
        # 가장 많은 오행과 가장 적은 오행 찾기
        max_oheng = max(oheng_count.items(), key=lambda x: x[1])
        min_oheng = min(oheng_count.items(), key=lambda x: x[1])
        
        return {
            'dominant': max_oheng[0],
            'weak': min_oheng[0],
            'balance': oheng_count
        }
    
    def _get_suitable_exercise(self, health_style):
        """건강 스타일에 맞는 운동 추천"""
        exercise_map = {
            '활발한 신진대사형': '유산소 운동과 근력 운동을 균형있게 하는 것이 좋습니다. 러닝, 수영, 자전거 타기 등 활동적인 운동이 적합합니다.',
            '안정적 체질형': '가벼운 산책, 요가, 태극권 등 부담없는 운동부터 시작하세요. 천천히 운동 강도를 높여가는 것이 중요합니다.',
            '강한 골격형': '웨이트 트레이닝, 등산, 구기 종목 등 근력과 지구력을 기르는 운동이 적합합니다. 운동 전후 스트레칭을 잊지 마세요.',
            '유연한 체질형': '요가, 필라테스, 수영 등 유연성을 기르는 운동이 좋습니다. 관절에 무리가 가지 않는 운동을 선택하세요.',
            '순환계 활발형': '규칙적인 유산소 운동이 중요합니다. 빠르게 걷기, 조깅, 에어로빅 등이 도움이 됩니다.',
            '안정적 순환형': '걷기, 가벼운 조깅, 실내 자전거 등 순환을 돕는 운동을 꾸준히 하세요.',
            '균형잡힌 건강형': '다양한 운동을 골고루 즐기되, 자신의 체력에 맞게 조절하세요. 주 3-4회 규칙적인 운동이 이상적입니다.'
        }
        return exercise_map.get(health_style, '자신의 체력에 맞는 운동을 선택하여 꾸준히 하는 것이 중요합니다.')
    
    def _generate_period_analysis(self):
        """시기별 건강운 분석"""
        return '건강운은 나이와 시기에 따라 변화합니다. 청년기에는 활력이 넘치지만 무리하기 쉽고, 중년기에는 성인병 예방에 신경써야 하며, 노년기에는 꾸준한 건강 관리가 중요합니다.'
    
    def _generate_management_advice(self, health_analysis, oheng_analysis):
        """건강 관리 조언 생성"""
        # 오행별 건강 조언
        oheng_advice = {
            '목': '간과 담낭 건강에 주의하세요. 신 맛 음식과 푸른색 채소가 도움이 됩니다.',
            '화': '심장과 소장 건강에 주의하세요. 쓴 맛 음식과 붉은색 음식이 도움이 됩니다.',
            '토': '비장과 위장 건강에 주의하세요. 단 맛 음식과 노란색 음식이 도움이 됩니다.',
            '금': '폐와 대장 건강에 주의하세요. 매운 맛 음식과 흰색 음식이 도움이 됩니다.',
            '수': '신장과 방광 건강에 주의하세요. 짠 맛 음식과 검은색 음식이 도움이 됩니다.'
        }
        
        weak_oheng = oheng_analysis.get('weak', '수')
        base_advice = oheng_advice.get(weak_oheng, '')
        
        # 건강 스타일별 추가 조언
        style_specific = f" 또한 {health_analysis['style']}의 특성상 {', '.join(health_analysis['weak_points'])}에 특별히 주의가 필요합니다."
        
        return base_advice + style_specific
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '건강운 분석',
            'description': '건강운 분석 데이터를 준비 중입니다.',
            'body_constitution': '',
            'vulnerable_areas': '',
            'suitable_exercise': '',
            'period_analysis': '',
            'management_advice': ''
        }