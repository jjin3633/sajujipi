# 일주 분석 모듈
import json
import os

class IljuAnalyzer:
    """일주 분석을 담당하는 클래스"""
    
    def __init__(self):
        # 데이터 파일 경로 수정
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ilju_data.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self.ilju_data = json.load(f)
        except FileNotFoundError:
            print(f"오류: ilju_data.json 파일을 찾을 수 없습니다. 경로: {data_path}")
            self.ilju_data = {}
        except json.JSONDecodeError:
            print(f"오류: ilju_data.json 파일 파싱 실패.")
            self.ilju_data = {}

    def analyze(self, day_pillar):
        """일주 분석 수행"""
        if not isinstance(day_pillar, dict) or 'gan' not in day_pillar or 'ji' not in day_pillar:
            return self._get_default_analysis("정보 없음")

        ilju_key = f"{day_pillar['gan']}{day_pillar['ji']}"
        ilju_info = self.ilju_data.get(ilju_key)
        
        if not ilju_info:
            return self._get_default_analysis(ilju_key)
        
        return {
            'title': f"{ilju_key} 일주 ({ilju_info.get('별칭', '')})",
            'basic_info': self._format_basic_info(ilju_info),
            'personality': self._format_personality(ilju_info),
            'characteristics': self._format_characteristics(ilju_info),
            'illustration_url': self._generate_illustration_url(ilju_key)
        }
    
    def _format_basic_info(self, ilju_info):
        """기본 정보 포맷팅"""
        return {
            'animal': ilju_info.get('동물', '정보 없음'),
            'element': ilju_info.get('오행', '정보 없음'),
            'nickname': ilju_info.get('별칭', '정보 없음')
        }
    
    def _format_personality(self, ilju_info):
        """성격 분석 포맷팅"""
        return {
            'pros': ilju_info.get('성격_장점', []),
            'cons': ilju_info.get('성격_단점', []),
            'overall': ilju_info.get('성격_종합', '정보 없음')
        }
    
    def _format_characteristics(self, ilju_info):
        """특징 분석 포맷팅"""
        return {
            'career': ilju_info.get('직업_특성', '정보 없음'),
            'relationship': ilju_info.get('대인관계', '정보 없음'),
            'health': ilju_info.get('건강_특성', '정보 없음')
        }
    
    def _generate_illustration_url(self, ilju_key):
        """일러스트 URL 생성"""
        # 간단한 해시 함수로 색상 결정 (더 나은 방법으로 개선 가능)
        hash_val = sum(ord(c) for c in ilju_key)
        colors = ["FF6B6B", "4ECDC4", "45B7D1", "F7D154", "F29B82", "C7F464"]
        color = colors[hash_val % len(colors)]
        return f"https://via.placeholder.com/400x300/{color}/FFFFFF?text={ilju_key}"
    
    def _get_default_analysis(self, ilju_key):
        """기본 분석 결과 반환"""
        return {
            'title': f"{ilju_key} 일주 분석",
            'basic_info': {
                'animal': '정보 없음', 'element': '정보 없음', 'nickname': '정보 없음'
            },
            'personality': {
                'pros': [], 'cons': [], 'overall': f'{ilju_key}에 대한 상세 데이터가 준비 중입니다.'
            },
            'characteristics': {
                'career': '정보 없음', 'relationship': '정보 없음', 'health': '정보 없음'
            },
            'illustration_url': self._generate_illustration_url(ilju_key)
        }
