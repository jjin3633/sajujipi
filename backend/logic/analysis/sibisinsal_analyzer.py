# 십이신살 분석 모듈
class SibisinsalAnalyzer:
    """십이신살 분석을 담당하는 클래스"""
    
    # 십이신살 데이터
    SIBISINSAL_DATA = {
        "역마살": {"keyword": "이동, 변화, 활동", "description": "활발한 이동과 변화가 많은 운", "effect": "해외 출장이나 이사가 많고, 변화를 즐기는 성향"},
        "도화살": {"keyword": "매력, 인기, 이성", "description": "이성에게 인기가 많고 매력적인 운", "effect": "대인관계가 원만하고 사교성이 뛰어남"},
        "화개살": {"keyword": "예술, 종교, 학문", "description": "예술적 재능과 정신적 깊이가 있는 운", "effect": "예술이나 종교, 철학 분야에 재능을 보임"},
        "천을귀인": {"keyword": "귀인, 도움, 행운", "description": "귀인의 도움을 받는 행운의 운", "effect": "어려울 때마다 도움을 주는 사람이 나타남"},
        "천의성": {"keyword": "의료, 치유, 봉사", "description": "의료나 치유 분야에 재능이 있는 운", "effect": "의료, 한의학, 상담 분야에 적성을 보임"},
        "문창귀인": {"keyword": "학문, 문서, 시험", "description": "학업과 시험에서 좋은 성과를 거두는 운", "effect": "학업 성취도가 높고 시험운이 좋음"},
        "장성살": {"keyword": "군인, 경찰, 무술", "description": "강직하고 용맹한 기질을 나타내는 운", "effect": "정의감이 강하고 보호 본능이 뛰어남"},
        "괴강살": {"keyword": "고집, 독립, 강직", "description": "독립적이고 강직한 성격을 나타내는 운", "effect": "자기 주관이 뚜렷하고 독립심이 강함"},
        "백호살": {"keyword": "사고, 주의, 신중", "description": "사고나 부상에 주의가 필요한 운", "effect": "신체적 활동 시 각별한 주의가 필요함"},
        "육해살": {"keyword": "건강, 주의, 관리", "description": "건강 관리에 특별히 신경써야 하는 운", "effect": "규칙적인 생활과 건강 관리가 중요함"}
    }
    
    # 일지별 신살 계산 테이블 (간략화된 버전)
    SINSAL_TABLE = {
        "자": ["역마살", "도화살"],
        "축": ["천을귀인", "화개살"],
        "인": ["역마살", "문창귀인"],
        "묘": ["도화살", "장성살"],
        "진": ["천의성", "괴강살"],
        "사": ["역마살", "천을귀인"],
        "오": ["도화살", "백호살"],
        "미": ["화개살", "육해살"],
        "신": ["역마살", "문창귀인"],
        "유": ["도화살", "천의성"],
        "술": ["괴강살", "장성살"],
        "해": ["역마살", "천을귀인"]
    }
    
    def analyze(self, saju_pillars):
        """십이신살 분석 수행"""
        try:
            # 십이신살 계산
            sibisinsal_result = self._calculate_sibisinsal(saju_pillars)
            
            # 시기별 영향 분석
            periods = self._analyze_by_period(sibisinsal_result)
            
            return {
                'title': '십이신살 분석',
                'content': self._generate_analysis_content(sibisinsal_result),
                'periods': periods,
                'sibisinsal_found': sibisinsal_result
            }
        except Exception as e:
            print(f"십이신살 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _calculate_sibisinsal(self, saju_pillars):
        """십이신살 계산"""
        found_sinsal = {}
        
        # 각 지지에서 신살 찾기
        positions = ['year', 'month', 'day', 'hour']
        position_names = {'year': '연지', 'month': '월지', 'day': '일지', 'hour': '시지'}
        
        for pos in positions:
            jiji = saju_pillars.get(pos, '')[1:2] if len(saju_pillars.get(pos, '')) > 1 else ''
            if jiji and jiji in self.SINSAL_TABLE:
                sinsal_list = self.SINSAL_TABLE[jiji]
                for sinsal in sinsal_list:
                    if sinsal not in found_sinsal:
                        found_sinsal[sinsal] = []
                    found_sinsal[sinsal].append(position_names[pos])
        
        return found_sinsal
    
    def _analyze_by_period(self, sibisinsal_result):
        """시기별 십이신살 분석"""
        periods = []
        
        # 초년기 (연지 영향)
        early_sinsal = self._get_period_sinsal(sibisinsal_result, '연지')
        early_desc = "당신의 초년기는 " + self._generate_period_description(early_sinsal, '초년기')
        periods.append({
            'title': '초년기',
            'description': early_desc
        })
        
        # 청년기 (월지 영향)
        youth_sinsal = self._get_period_sinsal(sibisinsal_result, '월지')
        youth_desc = "당신의 청년기는 " + self._generate_period_description(youth_sinsal, '청년기')
        periods.append({
            'title': '청년기',
            'description': youth_desc
        })
        
        # 중년기 (일지 영향)
        middle_sinsal = self._get_period_sinsal(sibisinsal_result, '일지')
        middle_desc = "당신의 중년기는 " + self._generate_period_description(middle_sinsal, '중년기')
        periods.append({
            'title': '중년기',
            'description': middle_desc
        })
        
        # 장년기 (시지 영향)
        late_sinsal = self._get_period_sinsal(sibisinsal_result, '시지')
        late_desc = "당신의 장년기는 " + self._generate_period_description(late_sinsal, '장년기')
        periods.append({
            'title': '장년기',
            'description': late_desc
        })
        
        return periods
    
    def _get_period_sinsal(self, sibisinsal_result, position):
        """특정 시기의 신살 추출"""
        period_sinsal = []
        for sinsal, positions in sibisinsal_result.items():
            if position in positions:
                period_sinsal.append(sinsal)
        return period_sinsal
    
    def _generate_period_description(self, sinsal_list, period):
        """시기별 신살 설명 생성"""
        if not sinsal_list:
            return f"{period}에 특별한 신살의 영향이 없어 평탄한 시기를 보낼 것입니다."
        
        descriptions = []
        for sinsal in sinsal_list:
            if sinsal in self.SIBISINSAL_DATA:
                data = self.SIBISINSAL_DATA[sinsal]
                descriptions.append(f"{sinsal}의 영향으로 {data['effect']}")
        
        base_desc = {
            '초년기': "기본적인 인성과 성격이 형성되는 시기입니다. ",
            '청년기': "사회 진출과 인간관계 형성이 중요한 시기입니다. ",
            '중년기': "가정과 직장에서의 안정이 중요한 시기입니다. ",
            '장년기': "인생의 후반부를 준비하는 시기입니다. "
        }
        
        return base_desc.get(period, "") + " ".join(descriptions)
    
    def _generate_analysis_content(self, sibisinsal_result):
        """십이신살 분석 내용 생성"""
        content = f"【십이신살 분석】{chr(10) * 2}"
        content += f"십이신살은 당신의 운명에 영향을 미치는 특별한 신살들입니다.{chr(10) * 2}"
        
        if sibisinsal_result:
            content += f"【발견된 신살】{chr(10)}"
            for sinsal, positions in sibisinsal_result.items():
                if sinsal in self.SIBISINSAL_DATA:
                    data = self.SIBISINSAL_DATA[sinsal]
                    content += f"▣ {sinsal} ({', '.join(positions)}){chr(10)}"
                    content += f"   • 키워드: {data['keyword']}{chr(10)}"
                    content += f"   • 설명: {data['description']}{chr(10)}"
                    content += f"   • 영향: {data['effect']}{chr(10) * 2}"
        else:
            content += "특별한 신살이 발견되지 않았습니다. 평탄한 운명을 가지고 있습니다.{chr(10)}"
        
        content += f"【신살의 활용법】{chr(10)}"
        content += f"1. 길신 활용: 좋은 신살의 기운을 최대한 활용하여 성공을 이루세요.{chr(10)}"
        content += f"2. 흉신 대비: 주의가 필요한 신살은 미리 파악하여 대비하세요.{chr(10)}"
        content += f"3. 균형 유지: 모든 신살은 양면성이 있으므로 균형잡힌 시각이 중요합니다.{chr(10)}"
        
        return content
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '십이신살 분석',
            'content': '십이신살 분석 데이터를 준비 중입니다.',
            'periods': []
        }