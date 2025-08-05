# 일주 분석 모듈
import json
import os

class IljuAnalyzer:
    """일주 분석을 담당하는 클래스"""
    
    def __init__(self):
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ilju_data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            self.ilju_data = json.load(f)
    
    def analyze(self, day_pillar):
        """일주 분석 수행"""
        ilju_key = f"{day_pillar['gan']}{day_pillar['ji']}"
        ilju_info = self.ilju_data.get(ilju_key, {})
        
        if not ilju_info:
            return self._get_default_analysis(ilju_key)
        
        return {
            'title': f"{ilju_key} 일주 분석",
            'basic_info': self._format_basic_info(ilju_info),
            'personality': self._format_personality(ilju_info),
            'characteristics': self._format_characteristics(ilju_info),
            'illustration_url': self._generate_illustration_url(ilju_key)
        }
    
    def _format_basic_info(self, ilju_info):
        """기본 정보 포맷팅"""
        return {
            'animal': ilju_info.get('동물', ''),
            'element': ilju_info.get('오행', ''),
            'nickname': ilju_info.get('별칭', '')
        }
    
    def _format_personality(self, ilju_info):
        """성격 분석 포맷팅"""
        return {
            'pros': ilju_info.get('성격_장점', []),
            'cons': ilju_info.get('성격_단점', []),
            'overall': ilju_info.get('성격_종합', '')
        }
    
    def _format_characteristics(self, ilju_info):
        """특징 분석 포맷팅"""
        return {
            'career': ilju_info.get('직업_특성', ''),
            'relationship': ilju_info.get('대인관계', ''),
            'health': ilju_info.get('건강_특성', '')
        }
    
    def _generate_illustration_url(self, ilju_key):
        """일러스트 URL 생성"""
        return f"https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text={ilju_key}+일주"
    
    def _get_default_analysis(self, ilju_key):
        """기본 분석 결과 반환"""
        return {
            'title': f"{ilju_key} 일주 분석",
            'basic_info': {
                'animal': '정보 없음',
                'element': '정보 없음',
                'nickname': '정보 없음'
            },
            'personality': {
                'pros': ['일반적으로 성실함'],
                'cons': ['때로는 고집이 셈'],
                'overall': '균형잡힌 성격'
            },
            'characteristics': {
                'career': '다양한 분야에서 활약 가능',
                'relationship': '원만한 대인관계',
                'health': '건강에 주의 필요'
            },
            'illustration_url': self._generate_illustration_url(ilju_key)
        }
    
    def generate_detailed_report(self, analysis_result):
        """상세 리포트 생성"""
        basic = analysis_result['basic_info']
        personality = analysis_result['personality']
        characteristics = analysis_result['characteristics']
        
        content = f"""【{analysis_result['title']}】

▣ 기본 정보
• 동물: {basic['animal']}
• 오행: {basic['element']}
• 별칭: {basic['nickname']}

▣ 성격 분석

【성격의 장점】
{chr(10).join(f'• {p}' for p in personality['pros'])}

【성격의 단점】
{chr(10).join(f'• {c}' for c in personality['cons'])}

【종합 평가】
{personality['overall']}

▣ 주요 특징

【직업적 특성】
{characteristics['career']}

【대인관계】
{characteristics['relationship']}

【건강 관리】
{characteristics['health']}

【전문가 조언】
당신의 일주 특성을 잘 이해하고 장점은 살리고 단점은 보완하여 
더 나은 삶을 살아가시기 바랍니다."""
        
        return {
            'title': analysis_result['title'],
            'content': content,
            'illustration_url': analysis_result['illustration_url']
        }