# 십이운성 분석 모듈
class SibiunseongAnalyzer:
    """십이운성 분석을 담당하는 클래스"""
    
    SIBIUNSEONG_TABLE = {
        "갑": {"해": "장생", "자": "목욕", "축": "관대", "인": "건록", "묘": "제왕", "진": "쇠", "사": "병", "오": "사", "미": "묘", "신": "절", "유": "태", "술": "양"},
        "을": {"오": "장생", "사": "목욕", "진": "관대", "묘": "건록", "인": "제왕", "축": "쇠", "자": "병", "해": "사", "술": "묘", "유": "절", "신": "태", "미": "양"},
        "병": {"인": "장생", "묘": "목욕", "진": "관대", "사": "건록", "오": "제왕", "미": "쇠", "신": "병", "유": "사", "술": "묘", "해": "절", "자": "태", "축": "양"},
        "정": {"유": "장생", "신": "목욕", "술": "관대", "해": "건록", "자": "제왕", "축": "쇠", "인": "병", "묘": "사", "진": "묘", "사": "절", "오": "태", "미": "양"},
        "무": {"인": "장생", "묘": "목욕", "진": "관대", "사": "건록", "오": "제왕", "미": "쇠", "신": "병", "유": "사", "술": "묘", "해": "절", "자": "태", "축": "양"},
        "기": {"유": "장생", "신": "목욕", "술": "관대", "해": "건록", "자": "제왕", "축": "쇠", "인": "병", "묘": "사", "진": "묘", "사": "절", "오": "태", "미": "양"},
        "경": {"사": "장생", "오": "목욕", "미": "관대", "신": "건록", "유": "제왕", "술": "쇠", "해": "병", "자": "사", "축": "묘", "인": "절", "묘": "태", "진": "양"},
        "신": {"자": "장생", "해": "목욕", "술": "관대", "유": "건록", "신": "제왕", "미": "쇠", "오": "병", "사": "사", "진": "묘", "묘": "절", "인": "태", "축": "양"},
        "임": {"신": "장생", "유": "목욕", "술": "관대", "해": "건록", "자": "제왕", "축": "쇠", "인": "병", "묘": "사", "진": "묘", "사": "절", "오": "태", "미": "양"},
        "계": {"묘": "장생", "인": "목욕", "축": "관대", "자": "건록", "해": "제왕", "술": "쇠", "유": "병", "신": "사", "미": "묘", "오": "절", "사": "태", "진": "양"}
    }
    
    SIBIUNSEONG_INFO = {
        "장생": "새로운 시작, 순수함, 발전 가능성", "목욕": "매력, 인기, 변화, 구설수",
        "관대": "성숙, 독립, 사회 진출", "건록": "자수성가, 안정, 경제적 독립",
        "제왕": "최고조, 권력, 카리스마, 고독", "쇠": "안정, 지혜, 쇠퇴의 시작",
        "병": "이동, 변화, 내면 성찰", "사": "정지, 생각, 전문성",
        "묘": "저장, 안정, 내면 세계", "절": "단절, 새로운 시작, 불안정",
        "태": "잉태, 희망, 잠재력", "양": "성장, 양육, 교육"
    }

    def analyze(self, saju_pillars):
        """십이운성 분석 수행"""
        try:
            sibiunseong_result = self._calculate_sibiunseong(saju_pillars)
            
            return {
                'title': '십이운성 분석',
                'content': self._generate_analysis_content(sibiunseong_result),
                'comprehensive': self._generate_comprehensive_analysis(sibiunseong_result),
                'illustration_url': "https://via.placeholder.com/400x300/E8F5E9/2E7D32?text=십이운성",
                'period_analysis': sibiunseong_result
            }
        except Exception as e:
            print(f"십이운성 분석 중 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._get_default_analysis()

    def _calculate_sibiunseong(self, saju_pillars):
        """일간을 기준으로 각 지지의 십이운성 계산"""
        day_gan = saju_pillars.get('day', {}).get('gan')
        if not day_gan:
            return {}
            
        result = {}
        position_names = {'year': '연주', 'month': '월주', 'day': '일주', 'hour': '시주'}
        
        for pos, pos_name in position_names.items():
            jiji = saju_pillars.get(pos, {}).get('ji')
            if jiji:
                unseong = self.SIBIUNSEONG_TABLE.get(day_gan, {}).get(jiji, "정보 없음")
                result[pos_name] = {
                    'unseong': unseong,
                    'info': self.SIBIUNSEONG_INFO.get(unseong, "정보 없음")
                }
        return result

    def _generate_analysis_content(self, result):
        """십이운성 분석 내용 생성"""
        content = "【십이운성 분석】\n\n십이운성은 천간의 기운이 각 지지를 만나 겪는 12단계의 에너지 변화입니다. 이를 통해 인생의 시기별 흐름을 알 수 있습니다.\n\n"
        content += "【나의 인생 시계】\n"
        for pos_name, data in result.items():
            content += f"- {pos_name} ({data['unseong']}): {data['info']}\n"
        return content

    def _generate_comprehensive_analysis(self, result):
        """종합 분석 생성"""
        comp_text = "【종합 분석】\n"
        
        # 시기별 분석
        period_map = {'연주': '초년', '월주': '청년', '일주': '중년', '시주': '말년'}
        for pos_name, data in result.items():
            period = period_map.get(pos_name)
            unseong = data['unseong']
            if period:
                comp_text += f"당신의 {period}은 '{unseong}'의 기운이 강하게 작용합니다. "

        # 강점과 약점 분석
        strengths = [d['unseong'] for d in result.values() if d['unseong'] in ['장생', '건록', '제왕', '관대']]
        weaknesses = [d['unseong'] for d in result.values() if d['unseong'] in ['병', '사', '묘', '절']]

        if strengths:
            comp_text += f"\n특히 '{', '.join(strengths)}'의 강한 에너지로 해당 시기에 큰 발전을 이룰 잠재력이 있습니다. "
        if weaknesses:
            comp_text += f"\n반면, '{', '.join(weaknesses)}'의 시기에는 안정을 취하고 내실을 다지는 지혜가 필요합니다. "
        
        comp_text += "\n인생의 각 단계마다 다른 에너지가 주어지니, 때에 맞춰 나아가고 물러설 줄 아는 것이 성공의 열쇠입니다."
        return comp_text

    def _get_default_analysis(self):
        """기본 분석 결과 반환"""
        return {
            'title': '십이운성 분석',
            'content': '십이운성 분석 데이터를 준비 중입니다.',
            'comprehensive': '종합 분석을 준비 중입니다.',
            'illustration_url': 'https://via.placeholder.com/400x300/E8F5E9/2E7D32?text=십이운성',
            'period_analysis': {}
        }
