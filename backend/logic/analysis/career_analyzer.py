# 직업운 분석 모듈
class CareerAnalyzer:
    """직업운 분석을 담당하는 클래스"""
    
    def analyze(self, saju_pillars, sipsung_data):
        """직업운 분석 수행"""
        try:
            # 십성 리스트 생성
            sipsung_list = list(sipsung_data.values()) if isinstance(sipsung_data, dict) else []
            
            # 직업 관련 십성 분석
            gwanseong_count = sipsung_list.count("편관") + sipsung_list.count("정관")  # 관리, 리더십
            siksang_count = sipsung_list.count("식신") + sipsung_list.count("상관")    # 창의성, 전문성
            jaeseong_count = sipsung_list.count("편재") + sipsung_list.count("정재")    # 재무, 사업
            inseong_count = sipsung_list.count("편인") + sipsung_list.count("정인")      # 학문, 연구
            bigyeop_count = sipsung_list.count("비견") + sipsung_list.count("겁재")     # 독립성, 경쟁
            
            # 직업 유형 분석
            career_analysis = self._analyze_career_type(
                gwanseong_count, siksang_count, jaeseong_count, 
                inseong_count, bigyeop_count
            )
            
            # 적합한 직업 리스트 생성
            suitable_jobs = self._get_suitable_jobs(career_analysis['type'])
            
            # 사업 vs 직장 분석
            business_vs_job = self._analyze_business_vs_job(
                gwanseong_count, siksang_count, jaeseong_count, bigyeop_count
            )
            
            # 성공 조언 생성
            advice = self._generate_career_advice(career_analysis)
            
            # 주의할 사람 분석
            caution_people = self._analyze_caution_people(sipsung_list)
            
            return {
                'title': career_analysis['type'],
                'description': career_analysis['description'],
                'suitable_jobs': suitable_jobs,
                'business_vs_job': business_vs_job,
                'advice': advice,
                'caution_people': caution_people,
                'avatar_url': self._generate_avatar_url(career_analysis['type'])
            }
        except Exception as e:
            print(f"직업운 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _analyze_career_type(self, gwanseong, siksang, jaeseong, inseong, bigyeop):
        """직업 유형 분석"""
        # 가장 강한 십성 찾기
        sipsung_counts = {
            '관성': gwanseong,
            '식상': siksang,
            '재성': jaeseong,
            '인성': inseong,
            '비겁': bigyeop
        }
        
        dominant = max(sipsung_counts.items(), key=lambda x: x[1])
        
        # 직업 유형 결정
        if gwanseong > 0 and siksang > 0:
            return {
                'type': '리더형 전문가',
                'description': '사주에 관리 능력(관성)과 창의성(식상)을 모두 갖추고 있어, 전문성을 바탕으로 한 리더십을 발휘할 수 있습니다. 팀을 이끌면서도 전문적인 성과를 낼 수 있는 능력이 뛰어납니다.'
            }
        elif gwanseong > siksang:
            return {
                'type': '관리직 전문가',
                'description': '사주에 관리 능력(관성)이 강하여, 체계적이고 안정적인 관리직이 적합합니다. 중간 관리자, 행정직, 공무원 등에서 뛰어난 성과를 낼 수 있습니다. 규칙과 절차를 중시하며, 조직을 효율적으로 운영하는 능력이 뛰어납니다.'
            }
        elif siksang > gwanseong:
            return {
                'type': '창의전문가',
                'description': '사주에 창의성과 전문성(식상)이 강하여, 독립적으로 일하는 전문가나 프리랜서로 성공할 가능성이 높습니다. 자신만의 창의적인 아이디어로 새로운 분야를 개척하는 데 유리합니다.'
            }
        elif jaeseong > 1:
            return {
                'type': '사업가형',
                'description': '사주에 재물운(재성)이 강하여, 사업이나 투자 분야에서 성공할 가능성이 높습니다. 기회를 포착하는 능력이 뛰어나며, 재무 관리에 탁월한 재능이 있습니다.'
            }
        elif inseong > 1:
            return {
                'type': '학자형',
                'description': '사주에 학문과 지식(인성)이 강하여, 연구직이나 교육 분야에서 성공할 가능성이 높습니다. 깊이 있는 탐구와 지식 전달에 탁월한 능력이 있습니다.'
            }
        elif bigyeop > 1:
            return {
                'type': '독립사업가',
                'description': '사주에 독립성과 경쟁심(비겁)이 강하여, 독립적인 사업이나 경쟁이 치열한 분야에서 성공할 가능성이 높습니다. 자신만의 길을 개척하는 능력이 뛰어납니다.'
            }
        else:
            return {
                'type': '다재다능형',
                'description': '사주에 여러 능력이 균형있게 분포되어 있어, 다양한 분야에서 능력을 발휘할 수 있습니다. 상황에 따라 유연하게 적응하며 성장할 수 있는 잠재력이 있습니다.'
            }
    
    def _get_suitable_jobs(self, career_type):
        """직업 유형별 적합한 직업 추천"""
        job_map = {
            '리더형 전문가': ['CEO', 'CTO', '팀장', '프로젝트 매니저', '컨설턴트'],
            '관리직 전문가': ['경영자', '관리자', '행정직', '공무원', '인사담당자'],
            '창의전문가': ['디자이너', '개발자', '작가', '예술가', '프리랜서'],
            '사업가형': ['사업가', '투자자', '부동산 전문가', '금융 전문가', '무역업'],
            '학자형': ['교수', '연구원', '교사', '강사', '저술가'],
            '독립사업가': ['1인 기업가', '프리랜서', '자영업자', '스타트업 창업자'],
            '다재다능형': ['기획자', '마케터', '영업직', '서비스직', '코디네이터']
        }
        return job_map.get(career_type, ['일반 사무직', '서비스업', '생산직'])
    
    def _analyze_business_vs_job(self, gwanseong, siksang, jaeseong, bigyeop):
        """사업 vs 직장 분석"""
        business_score = siksang + jaeseong + bigyeop
        job_score = gwanseong + 2
        
        if business_score > job_score:
            return '창의성과 독립성이 강하여 사업이나 프리랜서 활동이 유리합니다. 자신만의 아이템으로 성공할 가능성이 높습니다.'
        elif job_score > business_score:
            return '안정성과 조직 적응력이 뛰어나 직장에서 승진과 성장을 이룰 수 있습니다. 꾸준한 노력으로 전문가가 될 수 있습니다.'
        else:
            return '사업과 직장 모두에서 성공할 수 있는 균형잡힌 능력을 가지고 있습니다. 상황에 따라 유연하게 선택할 수 있습니다.'
    
    def _generate_career_advice(self, career_analysis):
        """직업 유형별 성공 조언"""
        advice_map = {
            '리더형 전문가': '전문성을 바탕으로 한 리더십을 발휘하세요. 팀원들의 전문성을 존중하면서도 명확한 방향을 제시하는 것이 중요합니다.',
            '관리직 전문가': '체계적인 업무 처리와 공정한 관리가 핵심입니다. 규정을 지키면서도 인간적인 배려를 잊지 마세요.',
            '창의전문가': '자신만의 독창성을 지키면서도 시장의 요구를 파악하세요. 꾸준한 자기계발이 성공의 열쇠입니다.',
            '사업가형': '기회를 포착하는 안목과 리스크 관리가 중요합니다. 신중한 투자와 과감한 실행의 균형을 맞추세요.',
            '학자형': '깊이 있는 연구와 쉬운 전달력을 모두 갖추세요. 이론과 실무를 연결하는 능력이 중요합니다.',
            '독립사업가': '자신만의 전문성을 확립하고 네트워크를 구축하세요. 고객 신뢰가 성공의 기반입니다.',
            '다재다능형': '다양한 경험을 쌓되 핵심 역량은 명확히 하세요. 상황에 맞는 유연한 대응이 강점입니다.'
        }
        
        base_advice = advice_map.get(career_analysis['type'], '끊임없는 자기계발과 성실한 태도가 중요합니다.')
        return f"{base_advice} 특히 팀워크를 중시하고 동료들과의 관계를 원만하게 유지하는 것이 장기적인 성공의 비결입니다."
    
    def _analyze_caution_people(self, sipsung_list):
        """주의해야 할 사람 유형 분석"""
        if '겁재' in sipsung_list:
            return '경쟁심이 강한 동료나 자신의 성과를 가로채려는 사람들을 주의하세요. 중요한 정보는 신중히 관리하는 것이 좋습니다.'
        elif '상관' in sipsung_list:
            return '비판적이거나 부정적인 태도를 가진 사람들을 주의하세요. 건설적인 비판과 악의적인 비난을 구분하는 지혜가 필요합니다.'
        elif sipsung_list.count('편관') > 1:
            return '권위적이거나 압박감을 주는 상사나 동료를 주의하세요. 자신의 의견을 당당하게 표현하되 예의를 지키는 것이 중요합니다.'
        else:
            return '직장에서 주의해야 할 사람은 당신의 성장을 방해하거나 부정적인 영향을 주는 사람들입니다. 긍정적인 관계에 집중하세요.'
    
    def _generate_avatar_url(self, career_type):
        """직업 유형별 아바타 URL 생성"""
        avatar_colors = {
            '리더형 전문가': '3F51B5',  # 파란색
            '관리직 전문가': '4CAF50',  # 초록색
            '창의전문가': 'FF9800',     # 주황색
            '사업가형': 'F44336',       # 빨간색
            '학자형': '9C27B0',         # 보라색
            '독립사업가': '00BCD4',     # 청록색
            '다재다능형': '795548'      # 갈색
        }
        color = avatar_colors.get(career_type, '607D8B')
        return f'https://via.placeholder.com/200x200/{color}/FFFFFF?text={career_type}'
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '직업운 분석',
            'description': '직업운 분석 데이터를 준비 중입니다.',
            'suitable_jobs': [],
            'business_vs_job': '',
            'advice': '',
            'caution_people': '',
            'avatar_url': 'https://via.placeholder.com/200x200/50C878/FFFFFF?text=직업+아바타'
        }