# 재물운 분석 모듈
class WealthAnalyzer:
    """재물운 분석을 담당하는 클래스"""
    
    def analyze(self, saju_pillars, sipsung_data):
        """재물운 분석 수행"""
        try:
            # 십성 리스트 생성
            sipsung_list = list(sipsung_data.values()) if isinstance(sipsung_data, dict) else []
            
            # 재물 관련 십성 분석
            jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")  # 재물의 별
            siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")    # 재물을 만드는 힘
            gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")  # 명예와 지위
            inseong_count = sipsung_list.count("편인") + sipsung_list.count("정인")    # 지식과 학문
            
            # 재물운 유형 분석
            wealth_type = self._analyze_wealth_type(jaeseong_count, siksang_count, gwanseong_count)
            
            # 전체 흐름 분석
            overall_flow = self._analyze_overall_flow(wealth_type)
            
            # 재물 특징 분석
            characteristics = self._analyze_characteristics(jaeseong_count, siksang_count, gwanseong_count, inseong_count)
            
            # 사람 분석
            people_analysis = self._analyze_people(sipsung_list)
            
            # 사업/투자 조언
            business_advice = self._generate_business_advice(wealth_type, jaeseong_count, siksang_count)
            
            return {
                'title': wealth_type['type'],
                'description': wealth_type['description'],
                'overall_flow': overall_flow,
                'wealth_characteristics': characteristics,
                'people_analysis': people_analysis,
                'business_investment_advice': business_advice
            }
        except Exception as e:
            print(f"재물운 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _analyze_wealth_type(self, jaeseong, siksang, gwanseong):
        """재물운 유형 분석"""
        if jaeseong == 0:
            if siksang > 0:
                return {
                    'type': '노력으로 부를 이루는 유형',
                    'description': '사주에 직접적인 재물(재성)은 뚜렷하지 않지만, 재물을 만들어내는 힘(식상)이 있습니다. 당신의 창의적인 아이디어나 꾸준한 노력이 곧 재물로 이어질 수 있습니다. 과정에 집중하면 결과는 자연히 따라올 것입니다.'
                }
            else:
                return {
                    'type': '안정을 추구하는 대기만성형',
                    'description': '사주에 재물과 관련된 기운이 강하지 않아, 큰 재물을 추구하기보다는 안정적인 수입을 통해 삶의 기반을 다지는 것이 중요합니다. 투기적인 활동보다는 성실함을 무기로 삼아야 합니다.'
                }
        elif jaeseong > 0:
            if siksang > 0:
                return {
                    'type': '타고난 사업가 유형 (식상생재)',
                    'description': '재물을 만들어내는 힘(식상)과 재물 그 자체(재성)를 모두 갖추고 있어, 사업적인 수완이 매우 뛰어납니다. 당신의 아이디어가 곧 돈이 되는 식상생재의 구조를 가지고 있어 큰 부를 이룰 잠재력이 높습니다.'
                }
            else:
                return {
                    'type': '관리와 기회의 재물 유형',
                    'description': '재물을 만들어내는 과정보다는, 이미 만들어진 재물을 관리하거나 기회를 포착하여 부를 쌓는 데 더 유리합니다. 안정적인 직장 내에서의 재무 관리나, 부동산, 유산 상속 등의 기회가 있을 수 있습니다.'
                }
        else:
            return {
                'type': '균형잡힌 재물 유형',
                'description': '재물운이 균형잡혀 있어, 극단적인 부나 가난보다는 중산층의 안정된 삶을 영위할 가능성이 높습니다. 꾸준한 노력과 현명한 재무 관리가 중요합니다.'
            }
    
    def _analyze_overall_flow(self, wealth_type):
        """전체 재물운 흐름 분석"""
        flow_map = {
            '노력으로 부를 이루는 유형': '초반에는 힘들지만 중년 이후 안정적인 재물운이 형성됩니다. 40대 이후가 재물운의 전성기가 될 것입니다.',
            '안정을 추구하는 대기만성형': '급격한 변화보다는 점진적인 성장이 특징입니다. 꾸준함이 최고의 무기가 되어 노후에 안정을 얻게 됩니다.',
            '타고난 사업가 유형 (식상생재)': '20-30대부터 재물운이 활발하게 움직이며, 여러 차례의 기회가 찾아옵니다. 기회를 잘 포착하면 큰 부를 이룰 수 있습니다.',
            '관리와 기회의 재물 유형': '안정적인 수입을 바탕으로 투자와 재테크로 재물을 늘려가는 것이 유리합니다. 부동산이나 금융 투자에 관심을 가지세요.',
            '균형잡힌 재물 유형': '극단적인 변화 없이 안정적인 재물운이 지속됩니다. 저축과 투자의 균형을 잘 맞추는 것이 중요합니다.'
        }
        return flow_map.get(wealth_type['type'], '재물운이 안정적으로 흐를 것입니다.')
    
    def _analyze_characteristics(self, jaeseong, siksang, gwanseong, inseong):
        """재물운 특징 분석"""
        characteristics = []
        
        if jaeseong > 1:
            characteristics.append('타고난 재물 감각: 돈의 흐름을 읽는 능력이 뛰어나 투자에 유리합니다.')
        if siksang > 1:
            characteristics.append('창의적 수익 창출: 새로운 아이디어로 수익을 창출하는 능력이 있습니다.')
        if gwanseong > 0:
            characteristics.append('명예를 통한 재물: 사회적 지위나 명예가 재물로 연결될 수 있습니다.')
        if inseong > 0:
            characteristics.append('지식의 자산화: 전문 지식이나 기술이 수익원이 될 수 있습니다.')
        
        if not characteristics:
            characteristics.append('안정적 재물 관리: 극단을 피하고 중도를 지키는 것이 재물운의 핵심입니다.')
        
        return ' '.join(characteristics)
    
    def _analyze_people(self, sipsung_list):
        """재물운과 관련된 사람 분석"""
        helpful_people = []
        caution_people = []
        
        if '정재' in sipsung_list or '편재' in sipsung_list:
            helpful_people.append('재무 전문가나 투자 조언자가 도움이 됩니다.')
        if '식신' in sipsung_list:
            helpful_people.append('창의적인 사업 파트너가 성공의 열쇠가 됩니다.')
        if '정관' in sipsung_list:
            helpful_people.append('신뢰할 수 있는 상사나 멘토가 재물운을 열어줍니다.')
        
        if '겁재' in sipsung_list:
            caution_people.append('재물을 빼앗으려는 경쟁자를 조심하세요.')
        if '상관' in sipsung_list:
            caution_people.append('과도한 비판으로 기회를 놓치게 하는 사람을 피하세요.')
        
        helpful_text = ' '.join(helpful_people) if helpful_people else '정직하고 성실한 사람들이 당신의 재물운을 돕습니다.'
        caution_text = ' '.join(caution_people) if caution_people else '탐욕스럽거나 무책임한 사람들을 주의하세요.'
        
        return f"도움이 되는 사람: {helpful_text} 주의할 사람: {caution_text}"
    
    def _generate_business_advice(self, wealth_type, jaeseong, siksang):
        """사업/투자 조언 생성"""
        advice_map = {
            '노력으로 부를 이루는 유형': '전문성을 기반으로 한 서비스업이나 컨설팅이 유리합니다. 자격증이나 기술 습득에 투자하세요.',
            '안정을 추구하는 대기만성형': '안정적인 직장과 함께 부업을 시작하는 것이 좋습니다. 적금, 펀드 등 안전한 재테크를 추천합니다.',
            '타고난 사업가 유형 (식상생재)': '창업이나 프랜차이즈 사업이 유리합니다. 트렌드를 읽고 새로운 시장을 개척하세요.',
            '관리와 기회의 재물 유형': '부동산 투자나 안정적인 배당주 투자가 적합합니다. 장기적 관점의 투자를 추천합니다.',
            '균형잡힌 재물 유형': '분산 투자를 통해 리스크를 관리하세요. 주식, 부동산, 예금을 적절히 배분하는 것이 좋습니다.'
        }
        
        base_advice = advice_map.get(wealth_type['type'], '자신의 성향에 맞는 투자를 선택하세요.')
        
        # 추가 조언
        if jaeseong > 1 and siksang > 1:
            base_advice += ' 특히 당신은 사업 수완이 뛰어나므로 적극적인 투자도 고려해볼 만합니다.'
        elif jaeseong == 0:
            base_advice += ' 투기보다는 저축과 안정적인 투자에 집중하는 것이 현명합니다.'
        
        return base_advice
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '재물운 분석',
            'description': '재물운 분석 데이터를 준비 중입니다.',
            'overall_flow': '',
            'wealth_characteristics': '',
            'people_analysis': '',
            'business_investment_advice': ''
        }