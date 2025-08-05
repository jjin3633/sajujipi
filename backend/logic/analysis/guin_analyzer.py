# 귀인 분석 모듈
class GuinAnalyzer:
    """귀인 분석을 담당하는 클래스"""
    
    # 천을귀인 테이블
    CHEONUL_TABLE = {
        "갑": ["축", "미"],  # 갑일간: 축,미가 천을귀인
        "을": ["자", "신"],  # 을일간: 자,신이 천을귀인
        "병": ["해", "유"],  # 병일간: 해,유가 천을귀인
        "정": ["해", "유"],  # 정일간: 해,유가 천을귀인
        "무": ["축", "미"],  # 무일간: 축,미가 천을귀인
        "기": ["자", "신"],  # 기일간: 자,신이 천을귀인
        "경": ["축", "미"],  # 경일간: 축,미가 천을귀인
        "신": ["인", "오"],  # 신일간: 인,오가 천을귀인
        "임": ["묘", "사"],  # 임일간: 묘,사가 천을귀인
        "계": ["묘", "사"]   # 계일간: 묘,사가 천을귀인
    }
    
    # 문창귀인 테이블
    MUNCHANG_TABLE = {
        "갑": "사",  # 갑일간: 사가 문창귀인
        "을": "오",  # 을일간: 오가 문창귀인
        "병": "신",  # 병일간: 신이 문창귀인
        "정": "유",  # 정일간: 유가 문창귀인
        "무": "신",  # 무일간: 신이 문창귀인
        "기": "유",  # 기일간: 유가 문창귀인
        "경": "해",  # 경일간: 해가 문창귀인
        "신": "자",  # 신일간: 자가 문창귀인
        "임": "인",  # 임일간: 인이 문창귀인
        "계": "묘"   # 계일간: 묘가 문창귀인
    }
    
    def analyze(self, saju_pillars):
        """귀인 분석 수행"""
        try:
            # 귀인 계산
            guin_result = self._calculate_guin(saju_pillars)
            
            # 시기별 분석
            periods = self._analyze_by_period(guin_result)
            
            return {
                'title': '귀인 분석',
                'content': self._generate_analysis_content(guin_result),
                'periods': periods,
                'overall': self._generate_overall_analysis(guin_result),
                'guin_found': guin_result
            }
        except Exception as e:
            print(f"귀인 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _calculate_guin(self, saju_pillars):
        """귀인 계산"""
        ilgan = saju_pillars.get('day', '')[:1]  # 일간 추출
        guin_found = {}
        
        # 천을귀인 찾기
        if ilgan in self.CHEONUL_TABLE:
            cheonul_jiji = self.CHEONUL_TABLE[ilgan]
            positions = ['year', 'month', 'day', 'hour']
            position_names = {'year': '연지', 'month': '월지', 'day': '일지', 'hour': '시지'}
            
            for pos in positions:
                jiji = saju_pillars.get(pos, '')[1:2] if len(saju_pillars.get(pos, '')) > 1 else ''
                if jiji in cheonul_jiji:
                    if '천을귀인' not in guin_found:
                        guin_found['천을귀인'] = []
                    guin_found['천을귀인'].append(position_names[pos])
        
        # 문창귀인 찾기
        if ilgan in self.MUNCHANG_TABLE:
            munchang_jiji = self.MUNCHANG_TABLE[ilgan]
            for pos in positions:
                jiji = saju_pillars.get(pos, '')[1:2] if len(saju_pillars.get(pos, '')) > 1 else ''
                if jiji == munchang_jiji:
                    if '문창귀인' not in guin_found:
                        guin_found['문창귀인'] = []
                    guin_found['문창귀인'].append(position_names[pos])
        
        return guin_found
    
    def _analyze_by_period(self, guin_result):
        """시기별 귀인 분석"""
        periods = []
        
        # 기본 시기별 귀인 설명
        period_base = {
            '초년기': {
                'base': '가족과 선생님의 도움을 받게 됩니다.',
                'detail': '특히 부모님의 사랑과 지원이 중요한 역할을 하며, 학창시절 은사의 가르침이 평생의 자산이 됩니다.'
            },
            '청년기': {
                'base': '상사나 멘토의 지도를 받게 됩니다.',
                'detail': '직장에서 만나는 선배나 상사가 중요한 조언자가 되며, 인생의 방향을 제시해줍니다.'
            },
            '중년기': {
                'base': '동료나 파트너의 협력을 받게 됩니다.',
                'detail': '함께 일하는 동료나 사업 파트너가 성공의 동반자가 되며, 시너지를 발휘합니다.'
            },
            '장년기': {
                'base': '후배나 제자의 도움을 받게 됩니다.',
                'detail': '당신이 키운 인재들이 보답하며, 새로운 활력과 기회를 가져다줍니다.'
            }
        }
        
        # 귀인 존재 여부에 따른 추가 설명
        position_to_period = {'연지': '초년기', '월지': '청년기', '일지': '중년기', '시지': '장년기'}
        
        for period_name, period_info in period_base.items():
            description = f"당신의 {period_name} 시기에는 {period_info['base']} {period_info['detail']}"
            
            # 해당 시기에 특별한 귀인이 있는지 확인
            for guin_type, positions in guin_result.items():
                for pos in positions:
                    if position_to_period.get(pos) == period_name:
                        description += f" 특히 {guin_type}의 기운으로 더욱 큰 도움을 받게 됩니다."
            
            periods.append({
                'title': period_name,
                'description': description
            })
        
        return periods
    
    def _generate_analysis_content(self, guin_result):
        """귀인 분석 내용 생성"""
        content = f"【귀인 분석】{chr(10) * 2}"
        content += f"귀인은 당신의 인생에서 중요한 도움을 주는 사람들입니다.{chr(10) * 2}"
        
        if guin_result:
            content += f"【발견된 귀인】{chr(10)}"
            for guin_type, positions in guin_result.items():
                content += f"▣ {guin_type} ({', '.join(positions)}){chr(10)}"
                if guin_type == '천을귀인':
                    content += f"   • 최고의 귀인으로 위기의 순간에 극적인 도움을 제공합니다.{chr(10)}"
                    content += f"   • 사회적 지위가 높은 사람이나 영향력 있는 인물이 됩니다.{chr(10)}"
                elif guin_type == '문창귀인':
                    content += f"   • 학업과 시험, 승진에 도움을 주는 귀인입니다.{chr(10)}"
                    content += f"   • 지적 성장과 문서 관련 일에서 행운을 가져다줍니다.{chr(10)}"
            content += chr(10)
        else:
            content += f"특별한 귀인성이 나타나지 않지만, 성실함과 인덕으로 귀인을 만들 수 있습니다.{chr(10) * 2}"
        
        content += f"【귀인과의 관계】{chr(10)}"
        content += f"1. 겸손한 태도: 귀인 앞에서는 항상 겸손한 자세를 유지하세요.{chr(10)}"
        content += f"2. 감사의 마음: 받은 도움에 대해 진심으로 감사하는 마음을 표현하세요.{chr(10)}"
        content += f"3. 보답의 자세: 나중에 다른 사람의 귀인이 되어 보답하세요.{chr(10)}"
        content += f"4. 관계 유지: 일회성이 아닌 지속적인 관계를 유지하세요.{chr(10)}"
        
        return content
    
    def _generate_overall_analysis(self, guin_result):
        """종합 분석 생성"""
        total_guin = sum(len(positions) for positions in guin_result.values())
        
        if total_guin == 0:
            return "귀인성이 직접적으로 나타나지 않지만, 당신의 성실함과 노력으로 스스로 길을 개척할 수 있습니다. 때로는 자수성가의 길이 더 큰 성취를 가져다줍니다."
        elif total_guin <= 2:
            return f"귀인 분석 결과, 당신의 인생에는 {total_guin}개의 귀인성이 나타납니다. 적절한 시기에 나타나는 귀인들이 당신의 성공을 도울 것입니다."
        else:
            return f"귀인 분석 결과, 당신의 인생에는 {total_guin}개의 강력한 귀인성이 나타납니다. 많은 사람들의 도움으로 큰 성공을 이룰 가능성이 높습니다. 귀인과의 관계를 소중히 여기세요."
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '귀인 분석',
            'content': '귀인 분석 데이터를 준비 중입니다.',
            'periods': [],
            'overall': '종합 분석을 준비 중입니다.'
        }