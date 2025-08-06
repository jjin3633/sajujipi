# 연애운 분석 모듈
class LoveAnalyzer:
    """연애운 & 결혼운 분석을 담당하는 클래스"""

    OHENG_RELATIONS = {
        '목': {'birth': '화', 'control': '토'}, '화': {'birth': '토', 'control': '금'},
        '토': {'birth': '금', 'control': '수'}, '금': {'birth': '수', 'control': '목'},
        '수': {'birth': '목', 'control': '화'}
    }
    OHENG_GAN = {"갑": "목", "을": "목", "병": "화", "정": "화", "무": "토", "기": "토", "경": "금", "신": "금", "임": "수", "계": "수"}

    def analyze(self, saju_pillars, sipsung_data, gender='여자'):
        """연애운 분석 수행 (성별에 따라 재성/관성 해석을 달리함)"""
        try:
            day_gan = saju_pillars.get('day', {}).get('gan')
            if not day_gan: return self._get_default_analysis()

            day_oheng = self.OHENG_GAN.get(day_gan)
            love_style = self._analyze_love_style(sipsung_data, day_oheng, gender)
            
            return {
                'title': f"{love_style['type']} ({love_style['keyword']})",
                'description': love_style['description'],
                'overall_tendency': self._analyze_overall_tendency(sipsung_data),
                'ideal_partner': self._analyze_ideal_partner(day_oheng, sipsung_data),
                'improvement_points': self._analyze_improvement_points(sipsung_data, gender),
                'flow_analysis': self._analyze_love_flow(sipsung_data, gender),
                'timing_location': self._analyze_timing_location(saju_pillars),
                'portrait_url': self._generate_portrait_url(love_style['type'])
            }
        except Exception as e:
            print(f"연애운 분석 중 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._get_default_analysis()

    def _analyze_love_style(self, sipsung_data, day_oheng, gender):
        """성별과 십성을 고려한 연애 스타일 분석"""
        sipsungs = list(sipsung_data.values())
        jaeseong = sipsungs.count('정재') + sipsungs.count('편재')
        gwanseong = sipsungs.count('정관') + sipsungs.count('편관')
        siksang = sipsungs.count('식신') + sipsungs.count('상관')

        # 여성: 관성(남자) 유무, 남성: 재성(여자) 유무가 중요
        target_sipsung = gwanseong if gender == '여자' else jaeseong

        if target_sipsung == 0 and siksang > 2:
            return {'type': '자유로운 예술가형', 'keyword': '표현과 자유', 'description': '틀에 얽매이지 않고 자유로운 연애를 추구합니다. 자신의 감정과 표현을 중시하며, 친구처럼 편안한 관계를 선호합니다.'}
        elif target_sipsung > 0 and siksang > 1:
            return {'type': '적극적인 로맨티스트형', 'keyword': '열정과 표현', 'description': '자신의 매력을 잘 알고 적극적으로 표현합니다. 연애를 주도하며, 드라마틱하고 열정적인 사랑을 만들어갑니다.'}
        elif target_sipsung > 1 and jaeseong > 1:
             return {'type': '인기 많은 사교형', 'keyword': '매력과 인기', 'description': '뛰어난 매력과 사교성으로 이성에게 인기가 많습니다. 다양한 만남 속에서 진정한 인연을 찾아나갑니다.'}
        elif target_sipsung > 0:
            return {'type': '안정적인 동반자형', 'keyword': '신뢰와 안정', 'description': '연애를 가볍게 생각하지 않으며, 결혼을 전제로 한 진지하고 안정적인 관계를 추구합니다.'}
        else:
            return {'type': '신중한 탐색가형', 'keyword': '신중과 관찰', 'description': '연애에 신중하며, 상대를 충분히 관찰하고 알아가는 시간이 필요합니다. 한번 마음을 열면 깊은 관계를 맺습니다.'}

    def _analyze_overall_tendency(self, sipsung_data):
        sipsungs = list(sipsung_data.values())
        if '상관' in sipsungs and '정관' not in sipsungs:
            return "기존의 틀을 깨는 혁신적인 연애관을 가지고 있어, 연인에게 새로운 영감을 주지만 때로는 갈등의 원인이 되기도 합니다."
        if '정인' in sipsungs and '정재' in sipsungs:
            return "현실과 이상 사이에서 균형을 잘 잡으며, 안정적이면서도 정신적인 교감을 중시하는 성숙한 연애를 합니다."
        return "상대방과 함께 성장하며, 서로에게 긍정적인 영향을 주는 관계를 만들어나가는 것을 중요하게 생각합니다."

    def _analyze_ideal_partner(self, day_oheng, sipsung_data):
        birth_oheng = self.OHENG_RELATIONS[day_oheng]['birth']
        control_oheng = self.OHENG_RELATIONS[day_oheng]['control']
        partner_desc = f"당신을 성장시키는 '{birth_oheng}'의 기운을 가진 사람, 또는 당신이 조화롭게 이끌 수 있는 '{control_oheng}'의 기운을 가진 사람이 좋은 인연입니다. "
        
        if '정인' in sipsung_data.values() or '편인' in sipsung_data.values():
            partner_desc += "지적으로 통하고, 기댈 수 있는 포근한 사람이 이상적입니다."
        else:
            partner_desc += "활동적이고, 함께 즐거운 경험을 만들어갈 수 있는 사람이 잘 맞습니다."
        return partner_desc

    def _analyze_improvement_points(self, sipsung_data, gender):
        sipsungs = list(sipsung_data.values())
        jaeseong = sipsungs.count('정재') + sipsungs.count('편재')
        gwanseong = sipsungs.count('정관') + sipsungs.count('편관')

        if gender == '여자' and gwanseong == 0:
            return "인연은 예상치 못한 곳에서 찾아옵니다. 마음을 열고 새로운 만남에 좀 더 적극적으로 나서보세요."
        if gender == '남자' and jaeseong == 0:
            return "자신의 매력을 너무 과소평가하지 마세요. 작은 관심 표현이 큰 변화를 가져올 수 있습니다."
        if '겁재' in sipsungs or '비견' in sipsungs:
             return "지나친 자존심이나 경쟁심이 연애의 걸림돌이 될 수 있습니다. 때로는 져주는 미덕이 필요합니다."
        return "자신의 감정을 솔직하게 표현하고, 상대방의 이야기를 경청하는 자세가 관계 발전의 핵심입니다."

    def _analyze_love_flow(self, sipsung_data, gender):
        # 대운의 흐름과 결합해야 정확하지만, 여기서는 단순화된 분석 제공
        sipsungs = list(sipsung_data.values())
        target_sipsung = '관' if gender == '여자' else '재'
        
        if f'정{target_sipsung}' in sipsungs or f'편{target_sipsung}' in sipsungs:
            return f"사주에 이성의 기운({target_sipsung}성)이 뚜렷하여, 인생 전반에 걸쳐 연애의 기회가 꾸준히 찾아옵니다. 20대 후반~30대에 결혼으로 이어질 좋은 인연을 만날 가능성이 높습니다."
        return "연애운이 특정 시기에 집중되기보다는, 자신의 노력과 준비에 따라 언제든 좋은 인연을 만날 수 있는 사주입니다. 마음의 준비가 되었을 때가 최고의 타이밍입니다."
    
    def _analyze_timing_location(self, saju_pillars):
        month_ji = saju_pillars.get('month', {}).get('ji')
        seasons = {'인묘진': '봄', '사오미': '여름', '신유술': '가을', '해자축': '겨울'}
        season = next((s for k, s in seasons.items() if month_ji in k), "계절")

        locations = {'인묘진': '도서관, 공원', '사오미': '공연장, 파티', '신유술': '전시회, 동호회', '해자축': '조용한 카페, 여행지'}
        location = next((l for k, l in locations.items() if month_ji in k), "일상적인 공간")
        
        return f"인연은 특히 '{season}'에 강하게 들어오며, '{location}'과 같은 장소에서 시작될 가능성이 높습니다."

    def _generate_portrait_url(self, style_type):
        color_map = {'예술가': 'E3F2FD', '로맨티스트': 'FFE0EC', '사교': 'FFCDD2', '동반자': 'E8F5E9', '탐색가': 'F3E5F5'}
        keyword = style_type.split(' ')[1][:-1]
        color = next((c for k, c in color_map.items() if k in keyword), 'E0E0E0')
        return f'https://via.placeholder.com/300x400/{color}/333333?text={keyword}'

    def _get_default_analysis(self):
        """기본 분석 결과 반환"""
        return {
            'title': '연애운 & 결혼운 분석',
            'description': '연애운 분석 데이터를 준비 중입니다.',
            'overall_tendency': '전체적인 경향을 분석 중입니다.',
            'ideal_partner': '이상적인 파트너를 분석 중입니다.',
            'improvement_points': '개선점을 분석 중입니다.',
            'flow_analysis': '시기별 흐름을 분석 중입니다.',
            'timing_location': '인연의 시기와 장소를 분석 중입니다.',
            'portrait_url': 'https://via.placeholder.com/300x400/E0E0E0/333333?text=인연'
        }
