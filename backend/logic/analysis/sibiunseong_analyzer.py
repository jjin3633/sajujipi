# 십이운성 분석 모듈
from ..saju_calculator import SajuCalculator

class SibiunseongAnalyzer:
    """십이운성 분석을 담당하는 클래스"""
    
    # 십이운성 테이블
    SIBIUNSEONG_TABLE = {
        "갑": {"자": "목욕", "축": "관대", "인": "건록", "묘": "제왕", "진": "쇠", "사": "병", "오": "사", "미": "묘", "신": "절", "유": "태", "술": "양", "해": "장생"},
        "을": {"자": "병", "축": "쇠", "인": "제왕", "묘": "건록", "진": "관대", "사": "목욕", "오": "장생", "미": "양", "신": "태", "유": "절", "술": "묘", "해": "사"},
        "병": {"자": "태", "축": "양", "인": "장생", "묘": "목욕", "진": "관대", "사": "건록", "오": "제왕", "미": "쇠", "신": "병", "유": "사", "술": "묘", "해": "절"},
        "정": {"자": "절", "축": "묘", "인": "사", "묘": "병", "진": "쇠", "사": "제왕", "오": "건록", "미": "관대", "신": "목욕", "유": "장생", "술": "양", "해": "태"},
        "무": {"자": "태", "축": "양", "인": "장생", "묘": "목욕", "진": "관대", "사": "건록", "오": "제왕", "미": "쇠", "신": "병", "유": "사", "술": "묘", "해": "절"},
        "기": {"자": "절", "축": "묘", "인": "사", "묘": "병", "진": "쇠", "사": "제왕", "오": "건록", "미": "관대", "신": "목욕", "유": "장생", "술": "양", "해": "태"},
        "경": {"자": "사", "축": "묘", "인": "절", "묘": "태", "진": "양", "사": "장생", "오": "목욕", "미": "관대", "신": "건록", "유": "제왕", "술": "쇠", "해": "병"},
        "신": {"자": "장생", "축": "양", "인": "태", "묘": "절", "진": "묘", "사": "사", "오": "병", "미": "쇠", "신": "제왕", "유": "건록", "술": "관대", "해": "목욕"},
        "임": {"자": "제왕", "축": "관대", "인": "목욕", "묘": "장생", "진": "양", "사": "태", "오": "절", "미": "묘", "신": "사", "유": "병", "술": "쇠", "해": "건록"},
        "계": {"자": "건록", "축": "쇠", "인": "병", "묘": "사", "진": "묘", "사": "절", "오": "태", "미": "양", "신": "장생", "유": "목욕", "술": "관대", "해": "제왕"}
    }
    
    # 십이운성 설명
    SIBIUNSEONG_INFO = {
        "장생": {"keyword": "시작, 탄생, 희망", "description": "새로운 시작과 희망찬 에너지가 넘치는 시기"},
        "목욕": {"keyword": "정화, 변화, 준비", "description": "기존의 것을 정리하고 새로운 변화를 준비하는 시기"},
        "관대": {"keyword": "성장, 발전, 확장", "description": "능력이 확장되고 사회적 인정을 받는 시기"},
        "건록": {"keyword": "전성기, 자수성가, 안정", "description": "가장 안정적이고 실력을 발휘하는 전성기"},
        "제왕": {"keyword": "절정, 카리스마, 고독", "description": "권력과 성공의 정점이지만 고독할 수 있는 시기"},
        "쇠": {"keyword": "쇠퇴, 변화 필요, 전환", "description": "기존 방식이 통하지 않아 새로운 전환이 필요한 시기"},
        "병": {"keyword": "변화, 이동, 내면 성찰", "description": "외부보다 내면에 집중하며 성찰이 필요한 시기"},
        "사": {"keyword": "종료, 마무리, 정리", "description": "한 사이클의 마무리와 정리가 필요한 시기"},
        "묘": {"keyword": "저장, 안정, 내면 집중", "description": "에너지를 저장하고 내적 성장에 집중하는 시기"},
        "절": {"keyword": "단절, 새출발, 독립", "description": "과거와 단절하고 새로운 독립적인 길을 가는 시기"},
        "태": {"keyword": "잉태, 준비, 가능성", "description": "새로운 가능성을 품고 준비하는 시기"},
        "양": {"keyword": "성장, 보육, 학습", "description": "보호받으며 성장하고 학습하는 시기"}
    }
    
    def __init__(self):
        self.calculator = SajuCalculator()
    
    def analyze(self, saju_pillars):
        """십이운성 분석 수행"""
        try:
            # 십이운성 계산
            sibiunseong_result = self._calculate_sibiunseong(saju_pillars)
            
            return {
                'title': '십이운성 분석',
                'content': self._generate_analysis_content(sibiunseong_result),
                'comprehensive': self._generate_comprehensive_analysis(sibiunseong_result),
                'illustration_url': self._generate_illustration(),
                'period_analysis': sibiunseong_result
            }
        except Exception as e:
            print(f"십이운성 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _calculate_sibiunseong(self, saju_pillars):
        """십이운성 계산"""
        ilgan = saju_pillars.get('day', '')[:1]  # 일간 추출
        
        if ilgan not in self.SIBIUNSEONG_TABLE:
            return {}
        
        result = {}
        positions = ['year', 'month', 'day', 'hour']
        position_names = {'year': '연주', 'month': '월주', 'day': '일주', 'hour': '시주'}
        
        for pos in positions:
            jiji = saju_pillars.get(pos, '')[1:2] if len(saju_pillars.get(pos, '')) > 1 else ''
            if jiji and jiji in self.SIBIUNSEONG_TABLE[ilgan]:
                unseong = self.SIBIUNSEONG_TABLE[ilgan][jiji]
                result[position_names[pos]] = {
                    'unseong': unseong,
                    'info': self.SIBIUNSEONG_INFO.get(unseong, {})
                }
        
        return result
    
    def _generate_analysis_content(self, sibiunseong_result):
        """십이운성 분석 내용 생성"""
        content = f"【십이운성 분석】{chr(10) * 2}"
        content += f"당신의 사주에서 나타나는 십이운성의 조합은 다음과 같습니다:{chr(10)}"
        
        for position, data in sibiunseong_result.items():
            unseong = data['unseong']
            info = data['info']
            content += f"▣ {position}: {unseong} - {info.get('keyword', '')}{chr(10)}"
        
        content += f"{chr(10)}이러한 십이운성 조합은 당신의 인생에서 다음과 같은 특징을 나타냅니다:{chr(10) * 2}"
        
        # 각 운성의 특성 분석
        for position, data in sibiunseong_result.items():
            unseong = data['unseong']
            info = data['info']
            content += f"{position} ({unseong}): {info.get('description', '')}{chr(10)}"
        
        content += f"{chr(10)}【인생의 흐름】{chr(10)}"
        content += self._analyze_life_flow(sibiunseong_result)
        
        return content
    
    def _analyze_life_flow(self, sibiunseong_result):
        """인생 흐름 분석"""
        # 주요 운성 파악
        strong_unseong = []
        weak_unseong = []
        
        strong_types = ['건록', '제왕', '관대', '장생']
        weak_types = ['사', '병', '쇠', '절']
        
        for position, data in sibiunseong_result.items():
            unseong = data['unseong']
            if unseong in strong_types:
                strong_unseong.append(f"{position}({unseong})")
            elif unseong in weak_types:
                weak_unseong.append(f"{position}({unseong})")
        
        flow_text = ""
        if strong_unseong:
            flow_text += f"강한 운성: {', '.join(strong_unseong)}이(가) 있어 해당 시기에 큰 성과를 이룰 수 있습니다.{chr(10)}"
        if weak_unseong:
            flow_text += f"주의 운성: {', '.join(weak_unseong)}이(가) 있어 해당 시기에는 신중한 대응이 필요합니다.{chr(10)}"
        
        return flow_text
    
    def _generate_comprehensive_analysis(self, sibiunseong_result):
        """종합 분석 생성"""
        content = f"【종합 분석】{chr(10) * 2}"
        
        # 전체적인 운성 균형 분석
        unseong_types = [data['unseong'] for data in sibiunseong_result.values()]
        
        if '건록' in unseong_types or '제왕' in unseong_types:
            content += "당신의 사주에는 강한 운성이 있어 큰 성공을 이룰 잠재력이 있습니다. "
        if '장생' in unseong_types:
            content += "새로운 시작에 유리한 운성이 있어 도전적인 일에 적합합니다. "
        if '병' in unseong_types or '사' in unseong_types:
            content += "변화와 전환의 운성이 있어 유연한 대응이 필요합니다. "
        
        content += f"{chr(10) * 2}당신의 십이운성 조합을 고려할 때, 각 시기의 특성을 잘 파악하고 그에 맞는 적절한 대응을 하는 것이 중요합니다.{chr(10)}"
        content += f"특히 긍정적인 기운이 나타나는 시기에는 적극적으로 활동하고, 도전적인 시기에는 신중하게 대응하시기 바랍니다.{chr(10) * 2}"
        
        content += f"【시기별 권장사항】{chr(10)}"
        for position, data in sibiunseong_result.items():
            unseong = data['unseong']
            advice = self._get_unseong_advice(unseong)
            content += f"• {position}: {advice}{chr(10)}"
        
        return content
    
    def _get_unseong_advice(self, unseong):
        """운성별 조언"""
        advice_map = {
            "장생": "새로운 도전과 시작에 적합한 시기",
            "목욕": "기존 방식을 정리하고 변화를 준비할 시기",
            "관대": "적극적인 활동과 확장에 유리한 시기",
            "건록": "안정적인 성과를 거둘 수 있는 최적의 시기",
            "제왕": "리더십을 발휘하되 겸손을 잃지 말아야 할 시기",
            "쇠": "새로운 방향을 모색하고 전환을 준비할 시기",
            "병": "내면을 돌아보고 재충전이 필요한 시기",
            "사": "한 사이클을 마무리하고 정리할 시기",
            "묘": "에너지를 축적하고 준비하는 시기",
            "절": "과거와 결별하고 독립적인 길을 갈 시기",
            "태": "새로운 가능성을 탐색하고 계획할 시기",
            "양": "배우고 성장하며 기초를 다질 시기"
        }
        return advice_map.get(unseong, "상황에 맞게 유연하게 대응할 시기")
    
    def _generate_illustration(self):
        """십이운성 일러스트 URL 생성"""
        return "https://via.placeholder.com/400x300/E8F5E9/2E7D32?text=십이운성+일러스트"
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '십이운성 분석',
            'content': '십이운성 분석 데이터를 준비 중입니다.',
            'comprehensive': '종합 분석을 준비 중입니다.',
            'illustration_url': self._generate_illustration()
        }