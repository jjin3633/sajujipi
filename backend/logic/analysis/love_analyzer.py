# 연애운 분석 모듈
class LoveAnalyzer:
    """연애운 & 결혼운 분석을 담당하는 클래스"""
    
    # 오행 데이터
    OHENG_GAN = {
        "갑": "목", "을": "목", "병": "화", "정": "화",
        "무": "토", "기": "토", "경": "금", "신": "금",
        "임": "수", "계": "수"
    }
    
    def analyze(self, saju_pillars, sipsung_data):
        """연애운 분석 수행"""
        try:
            # 십성 리스트 생성
            sipsung_list = list(sipsung_data.values()) if isinstance(sipsung_data, dict) else []
            
            # 연애 관련 십성 분석
            gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")  # 배우자, 연인
            jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")    # 재물, 매력
            siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")    # 표현력, 매력
            inseong_count = sipsung_list.count("편인") + sipsung_list.count("정인")    # 정신적 교감
            
            # 일간 오행 분석 (남녀 구분)
            day_gan = saju_pillars.get('day', '')[:1] if saju_pillars.get('day', '') else ''
            
            # 연애 스타일 분석
            love_style = self._analyze_love_style(gwanseong_count, jaeseong_count, siksang_count)
            
            # 전체적 경향 분석
            overall_tendency = self._analyze_overall_tendency(love_style, gwanseong_count, jaeseong_count)
            
            # 이상형 분석
            ideal_partner = self._analyze_ideal_partner(sipsung_list, day_gan)
            
            # 개선점 분석
            improvement_points = self._analyze_improvement_points(gwanseong_count, jaeseong_count, siksang_count)
            
            # 시기별 흐름 분석
            flow_analysis = self._analyze_love_flow(gwanseong_count, jaeseong_count)
            
            # 인연 시기와 장소
            timing_location = self._analyze_timing_location(saju_pillars, sipsung_list)
            
            # 초상화 URL 생성
            portrait_url = self._generate_portrait_url(love_style['type'])
            
            return {
                'title': love_style['type'],
                'description': love_style['description'],
                'overall_tendency': overall_tendency,
                'ideal_partner': ideal_partner,
                'improvement_points': improvement_points,
                'flow_analysis': flow_analysis,
                'timing_location': timing_location,
                'portrait_url': portrait_url
            }
        except Exception as e:
            print(f"연애운 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _analyze_love_style(self, gwanseong, jaeseong, siksang):
        """연애 스타일 분석"""
        if gwanseong == 0 and jaeseong == 0:
            return {
                'type': '자유로운 연애 스타일',
                'description': '사주에 배우자(관성)와 매력(재성)이 부족하여, 연애에 얽매이지 않고 자유로운 관계를 추구합니다. 친구 같은 편안한 관계를 선호하며, 결혼보다는 연애 자체를 즐기는 스타일입니다.'
            }
        elif gwanseong > 0 and jaeseong == 0:
            return {
                'type': '전통적인 연애 스타일',
                'description': '사주에 배우자(관성)는 있지만 매력(재성)이 부족하여, 전통적이고 안정적인 연애를 선호합니다. 진지한 관계를 추구하며, 결혼을 염두에 둔 연애를 하는 스타일입니다.'
            }
        elif gwanseong == 0 and jaeseong > 0:
            return {
                'type': '매력적인 연애 스타일',
                'description': '사주에 매력(재성)은 있지만 배우자(관성)가 부족하여, 이성에게 인기는 많지만 깊은 관계로 발전하기 어려울 수 있습니다. 다양한 연애 경험을 통해 진정한 사랑을 찾아가는 스타일입니다.'
            }
        elif gwanseong > 0 and jaeseong > 0:
            return {
                'type': '열정적인 연애 스타일',
                'description': '사주에 배우자(관성)와 매력(재성)을 모두 갖추고 있어, 열정적이고 활발한 연애를 즐기는 스타일입니다. 상대방을 사로잡는 매력이 뛰어나며, 깊이 있는 관계로 발전할 가능성이 높습니다.'
            }
        elif siksang > 1:
            return {
                'type': '로맨틱한 연애 스타일',
                'description': '사주에 표현력(식상)이 강하여, 로맨틱하고 감성적인 연애를 추구합니다. 예술적 감각과 표현력으로 상대방을 매료시키며, 드라마 같은 연애를 꿈꿉니다.'
            }
        else:
            return {
                'type': '신중한 연애 스타일',
                'description': '사주의 연애운이 균형잡혀 있어, 신중하고 안정적인 연애를 추구합니다. 천천히 상대방을 알아가며, 확신이 들 때까지 기다리는 스타일입니다.'
            }
    
    def _analyze_overall_tendency(self, love_style, gwanseong, jaeseong):
        """전체적 연애 경향 분석"""
        tendency_map = {
            '자유로운 연애 스타일': '독립적이고 자유로운 연애관을 가지고 있어, 구속받지 않는 관계를 선호합니다.',
            '전통적인 연애 스타일': '안정적이고 진지한 연애를 추구하며, 가족의 의견도 중요하게 생각합니다.',
            '매력적인 연애 스타일': '이성에게 인기가 많고 매력적이지만, 진정한 사랑을 찾는 데 시간이 필요합니다.',
            '열정적인 연애 스타일': '사랑에 빠지면 온 마음을 다해 사랑하며, 상대방과 깊은 유대감을 형성합니다.',
            '로맨틱한 연애 스타일': '감성적이고 로맨틱한 분위기를 중시하며, 특별한 추억을 만들어가는 것을 좋아합니다.',
            '신중한 연애 스타일': '천천히 관계를 발전시키며, 신뢰를 바탕으로 한 안정적인 연애를 추구합니다.'
        }
        
        base_tendency = tendency_map.get(love_style['type'], '자신만의 독특한 연애 스타일을 가지고 있습니다.')
        
        # 추가 분석
        if gwanseong > 1:
            base_tendency += ' 특히 결혼 운이 강하여 안정적인 가정을 이룰 가능성이 높습니다.'
        elif jaeseong > 1:
            base_tendency += ' 이성에게 매력적으로 어필하는 능력이 뛰어납니다.'
        
        return base_tendency
    
    def _analyze_ideal_partner(self, sipsung_list, day_gan):
        """이상형 분석"""
        ideal_traits = []
        
        # 십성별 이상형 특징
        if '정관' in sipsung_list:
            ideal_traits.append('책임감 있고 든든한 사람')
        if '편관' in sipsung_list:
            ideal_traits.append('카리스마 있고 추진력 있는 사람')
        if '정재' in sipsung_list:
            ideal_traits.append('경제적으로 안정적인 사람')
        if '편재' in sipsung_list:
            ideal_traits.append('사업 수완이 있고 활발한 사람')
        if '식신' in sipsung_list:
            ideal_traits.append('유머 감각이 있고 여유로운 사람')
        if '상관' in sipsung_list:
            ideal_traits.append('예리하고 지적인 사람')
        if '정인' in sipsung_list:
            ideal_traits.append('지적이고 품격 있는 사람')
        if '편인' in sipsung_list:
            ideal_traits.append('창의적이고 독특한 사람')
        
        if not ideal_traits:
            ideal_traits.append('성실하고 믿음직한 사람')
        
        # 오행별 이상형 추가
        if day_gan in self.OHENG_GAN:
            oheng = self.OHENG_GAN[day_gan]
            oheng_map = {
                '목': '따뜻하고 포용력 있는',
                '화': '밝고 열정적인',
                '토': '안정적이고 신뢰할 수 있는',
                '금': '원칙적이고 깔끔한',
                '수': '지혜롭고 유연한'
            }
            ideal_traits.insert(0, oheng_map.get(oheng, '조화로운'))
        
        return f"당신의 이상형은 {', '.join(ideal_traits[:3])} 사람입니다. 특히 당신의 부족한 부분을 채워주고 함께 성장할 수 있는 동반자가 최고의 인연이 될 것입니다."
    
    def _analyze_improvement_points(self, gwanseong, jaeseong, siksang):
        """연애 개선점 분석"""
        improvements = []
        
        if gwanseong == 0:
            improvements.append('결혼에 대한 구체적인 계획을 세우는 것이 도움이 됩니다.')
        if jaeseong == 0:
            improvements.append('자신의 매력을 개발하고 표현하는 방법을 익히세요.')
        if siksang == 0:
            improvements.append('감정 표현을 더 적극적으로 하는 연습이 필요합니다.')
        
        if gwanseong > 2:
            improvements.append('상대방을 너무 구속하지 않도록 주의하세요.')
        if jaeseong > 2:
            improvements.append('외모나 조건보다 내면을 보는 안목을 기르세요.')
        
        if not improvements:
            improvements.append('상대방을 이해하려는 노력과 진심을 다한 대화가 중요합니다.')
        
        return ' '.join(improvements[:2])
    
    def _analyze_love_flow(self, gwanseong, jaeseong):
        """시기별 애정운 흐름 분석"""
        if gwanseong > jaeseong:
            return '20대 후반에서 30대 초반에 결혼 운이 강하게 나타납니다. 이 시기를 놓치지 않는 것이 중요하며, 40대 이후에는 안정적인 부부 관계를 유지할 수 있습니다.'
        elif jaeseong > gwanseong:
            return '젊은 시절부터 이성에게 인기가 많지만, 진정한 인연은 30대 중반 이후에 만날 가능성이 높습니다. 다양한 경험을 통해 성숙해진 후 최고의 파트너를 만나게 됩니다.'
        else:
            return '애정운은 인생의 각 시기마다 다른 특성을 보입니다. 20대는 자유로운 연애, 30대는 진지한 만남, 40대 이후는 깊은 신뢰를 바탕으로 한 관계가 중심이 됩니다.'
    
    def _analyze_timing_location(self, saju_pillars, sipsung_list):
        """인연의 시기와 장소 분석"""
        # 계절 분석
        spring_energy = sipsung_list.count('식신') + sipsung_list.count('상관')
        summer_energy = sipsung_list.count('정재') + sipsung_list.count('편재')
        autumn_energy = sipsung_list.count('정관') + sipsung_list.count('편관')
        winter_energy = sipsung_list.count('정인') + sipsung_list.count('편인')
        
        seasons = []
        if spring_energy > 0:
            seasons.append('봄')
        if summer_energy > 0:
            seasons.append('여름')
        if autumn_energy > 0:
            seasons.append('가을')
        if winter_energy > 0:
            seasons.append('겨울')
        
        if not seasons:
            seasons = ['봄', '가을']
        
        # 장소 분석
        locations = []
        if '식신' in sipsung_list:
            locations.append('맛집이나 카페')
        if '정인' in sipsung_list or '편인' in sipsung_list:
            locations.append('도서관이나 문화센터')
        if '정관' in sipsung_list:
            locations.append('직장이나 공식적인 모임')
        if '편재' in sipsung_list:
            locations.append('사교 모임이나 파티')
        
        if not locations:
            locations.append('일상적인 생활 공간')
        
        return f"연애운이 높은 시기는 {', '.join(seasons[:2])}이며, {', '.join(locations[:2])} 같은 곳에서 좋은 인연을 만날 수 있습니다."
    
    def _generate_portrait_url(self, love_style):
        """연애 스타일별 초상화 URL 생성"""
        portrait_colors = {
            '자유로운 연애 스타일': 'E3F2FD',   # 연한 파란색
            '전통적인 연애 스타일': 'F3E5F5',   # 연한 보라색
            '매력적인 연애 스타일': 'FFE0EC',   # 연한 분홍색
            '열정적인 연애 스타일': 'FFCDD2',   # 진한 분홍색
            '로맨틱한 연애 스타일': 'FCE4EC',   # 로즈색
            '신중한 연애 스타일': 'E8F5E9'      # 연한 초록색
        }
        color = portrait_colors.get(love_style, 'FFE0EC')
        return f'https://via.placeholder.com/300x400/{color}/C2185B?text={love_style}'
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '연애운 & 결혼운 분석',
            'description': '연애운 분석 데이터를 준비 중입니다.',
            'overall_tendency': '',
            'ideal_partner': '',
            'improvement_points': '',
            'flow_analysis': '',
            'timing_location': '',
            'portrait_url': 'https://via.placeholder.com/300x400/FFE0EC/C2185B?text=인연+상대'
        }