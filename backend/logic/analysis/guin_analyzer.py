# 귀인 분석 모듈
class GuinAnalyzer:
    """귀인 분석을 담당하는 클래스"""
    
    # 천을귀인 테이블
    CHEONUL_TABLE = {
        "갑": ["축", "미"],
        "을": ["자", "신"],
        "병": ["해", "유"],
        "정": ["해", "유"],
        "무": ["축", "미"],
        "기": ["자", "신"],
        "경": ["축", "미"],
        "신": ["인", "오"],
        "임": ["묘", "사"],
        "계": ["묘", "사"]
    }
    
    # 문창귀인 테이블
    MUNCHANG_TABLE = {
        "갑": "사", "을": "오", "병": "신", "정": "유",
        "무": "신", "기": "유", "경": "해", "신": "자",
        "임": "인", "계": "묘"
    }
    
    def analyze(self, saju_pillars):
        """귀인 분석 수행"""
        try:
            guin_result = self._calculate_guin(saju_pillars)
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
            import traceback
            traceback.print_exc()
            return self._get_default_analysis()
    
    def _calculate_guin(self, saju_pillars):
        """사주 내 귀인 계산"""
        ilgan = saju_pillars.get('day', {}).get('gan')
        if not ilgan:
            return {}

        guin_found = {}
        positions = ['year', 'month', 'day', 'hour']
        position_names = {'year': '연지', 'month': '월지', 'day': '일지', 'hour': '시지'}

        # 천을귀인 찾기
        if ilgan in self.CHEONUL_TABLE:
            cheonul_jiji_list = self.CHEONUL_TABLE[ilgan]
            for pos in positions:
                jiji = saju_pillars.get(pos, {}).get('ji')
                if jiji in cheonul_jiji_list:
                    if '천을귀인' not in guin_found:
                        guin_found['천을귀인'] = []
                    if position_names[pos] not in guin_found['천을귀인']:
                        guin_found['천을귀인'].append(position_names[pos])
        
        # 문창귀인 찾기
        if ilgan in self.MUNCHANG_TABLE:
            munchang_jiji = self.MUNCHANG_TABLE[ilgan]
            for pos in positions:
                jiji = saju_pillars.get(pos, {}).get('ji')
                if jiji == munchang_jiji:
                    if '문창귀인' not in guin_found:
                        guin_found['문창귀인'] = []
                    if position_names[pos] not in guin_found['문창귀인']:
                        guin_found['문창귀인'].append(position_names[pos])
        
        return guin_found
    
    def _analyze_by_period(self, guin_result):
        """시기별 귀인 분석"""
        periods = []
        period_base = {
            '초년운 (연지)': '가족과 스승의 도움으로 기반을 다지는 시기입니다. 부모님의 사랑과 좋은 스승의 가르침이 인생의 큰 자산이 됩니다.',
            '청년운 (월지)': '사회생활을 시작하며 상사, 동료, 친구의 도움을 받습니다. 좋은 인간관계가 성공의 발판이 됩니다.',
            '중년운 (일지)': '배우자의 헌신적인 지지와 안정된 가정 생활이 사회적 성공의 원동력이 됩니다. 자신을 믿고 지지해주는 사람이 곁에 있습니다.',
            '말년운 (시지)': '자녀나 후배, 부하 직원의 도움으로 편안하고 안정된 노후를 보냅니다. 과거에 베푼 덕이 돌아오는 시기입니다.'
        }
        
        position_to_period_title = {'연지': '초년운 (연지)', '월지': '청년운 (월지)', '일지': '중년운 (일지)', '시지': '말년운 (시지)'}

        for title, base_desc in period_base.items():
            special_guin = []
            for guin_type, positions in guin_result.items():
                for pos_name in positions:
                    if position_to_period_title.get(pos_name) == title:
                        special_guin.append(guin_type)
            
            description = base_desc
            if special_guin:
                description += f" 특히, 이 시기에는 '{', '.join(special_guin)}'의 영향으로 더욱 강력한 귀인의 도움을 기대할 수 있습니다."

            periods.append({
                'title': title,
                'description': description
            })
        
        return periods
    
    def _generate_analysis_content(self, guin_result):
        """귀인 분석 내용 생성"""
        content = "【귀인 분석】\n\n귀인은 인생의 결정적인 순간에 나타나 도움을 주는 소중한 인연입니다.\n\n"
        
        if not guin_result:
            content += "사주에 특별히 드러나는 귀인은 없지만, 당신의 성실함과 노력이 스스로 귀인이 되어 길을 열어줄 것입니다. 인복은 스스로 만들어가는 것입니다."
        else:
            content += "【당신의 수호천사, 귀인】\n"
            if '천을귀인' in guin_result:
                content += f"- 천을귀인 ({', '.join(guin_result['천을귀인'])}): 가장 길한 귀인으로, 재앙을 막고 복을 불러옵니다. 사회적으로 명망 있는 인물의 도움을 받거나, 위기의 순간에 기적처럼 길이 열립니다.\n"
            if '문창귀인' in guin_result:
                content += f"- 문창귀인 ({', '.join(guin_result['문창귀인'])}): 지혜와 학문, 예술적 재능을 상징합니다. 시험 합격, 승진, 창의적인 분야에서 큰 성공을 거두도록 돕습니다.\n"
        
        content += "\n【귀인을 만나는 법】\n1. 먼저 베푸세요: 조건 없는 선행이 귀인을 부릅니다.\n2. 긍정적인 태도: 밝고 긍정적인 사람에게는 좋은 인연이 모입니다.\n3. 끊임없는 자기계발: 스스로의 가치를 높이는 것이 최고의 준비입니다."
        return content
    
    def _generate_overall_analysis(self, guin_result):
        """종합 분석 생성"""
        total_guin = sum(len(positions) for positions in guin_result.values())
        
        if total_guin == 0:
            return "사주에 귀인이 드러나지 않아도 실망할 필요 없습니다. 스스로의 노력으로 성공을 일구는 자수성가형 인물이며, 그 과정에서 얻는 성취감이 더욱 값질 것입니다."
        elif total_guin <= 2:
            return f"인생의 여정에서 {total_guin}번의 중요한 도움을 받을 귀인이 예비되어 있습니다. 이 인연을 소중히 여기고 기회를 잘 활용한다면 인생이 한 단계 도약할 것입니다."
        else:
            return f"강력한 귀인의 가호를 받는 당신은 인복이 매우 뛰어납니다. 주변에 항상 좋은 사람들이 함께하며, 위기 속에서도 기회를 만들어내는 힘이 있습니다. 받은 도움을 다시 나누며 선한 영향력을 펼치세요."
            
    def _get_default_analysis(self):
        """기본 분석 결과 반환"""
        return {
            'title': '귀인 분석',
            'content': '귀인 분석 데이터를 준비 중입니다. 잠시 후 다시 시도해주세요.',
            'periods': [],
            'overall': '종합 분석을 준비 중입니다.',
            'guin_found': {}
        }
