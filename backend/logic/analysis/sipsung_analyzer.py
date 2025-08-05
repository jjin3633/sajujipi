# 십성 분석 모듈
from ..saju_calculator import SajuCalculator

class SipsungAnalyzer:
    """십성 분석을 담당하는 클래스"""
    
    def __init__(self):
        self.calculator = SajuCalculator()
    
    def analyze(self, sipsung_data):
        """십성 분석 수행"""
        try:
            # 십성 개수 계산
            sipsung_counts = self._count_sipsung(sipsung_data)
            
            # 십성 분석 내용 생성
            analysis_content = self._generate_analysis_content(sipsung_counts)
            
            # 시기별 십성 분석
            period_analysis = self._analyze_by_period(sipsung_data)
            
            return {
                'title': '십성 분석',
                'sipsung_counts': sipsung_counts,
                'content': analysis_content,
                'comprehensive': self._generate_comprehensive_analysis(sipsung_counts),
                'period_analysis': period_analysis
            }
        except Exception as e:
            print(f"십성 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _count_sipsung(self, sipsung_data):
        """십성 개수 집계"""
        counts = {}
        for position, sipsung in sipsung_data.items():
            if sipsung and sipsung != '미확인':
                counts[sipsung] = counts.get(sipsung, 0) + 1
        return counts
    
    def _generate_analysis_content(self, sipsung_counts):
        """십성 분석 내용 생성"""
        content = f"【십성 분석】{chr(10) * 2}"
        content += f"당신의 사주에서 나타나는 십성의 조합은 다음과 같습니다:{chr(10)}"
        
        for sipsung, count in sipsung_counts.items():
            content += f"▣ {sipsung}: {count}개{chr(10)}"
        
        content += f"{chr(10)}이러한 십성 조합은 당신의 인생에서 다음과 같은 특징을 나타냅니다:{chr(10) * 2}"
        
        # 주요 특징 분석
        dominant_sipsung = max(sipsung_counts.items(), key=lambda x: x[1])[0] if sipsung_counts else None
        
        if dominant_sipsung:
            content += f"1. 주요 십성: {dominant_sipsung}이(가) 가장 강하게 나타납니다.{chr(10)}"
            content += f"2. 성격적 특징: {self._get_sipsung_character(dominant_sipsung)}{chr(10)}"
            content += f"3. 직업적 성향: {self._get_sipsung_career(dominant_sipsung)}{chr(10)}"
            content += f"4. 대인관계: {self._get_sipsung_relationship(dominant_sipsung)}{chr(10)}"
        
        return content
    
    def _generate_comprehensive_analysis(self, sipsung_counts):
        """종합 분석 생성"""
        content = f"【종합 분석】{chr(10) * 2}"
        
        if not sipsung_counts:
            return content + "십성 데이터가 부족하여 종합 분석이 어렵습니다."
        
        # 십성 균형 분석
        total_count = sum(sipsung_counts.values())
        balance_analysis = self._analyze_balance(sipsung_counts, total_count)
        
        content += f"{balance_analysis}{chr(10) * 2}"
        content += f"【전문가 조언】{chr(10)}"
        content += "당신의 십성 조합을 고려할 때, 각 시기의 특성을 잘 파악하고 긍정적 면모를 최대한 활용하는 것이 중요합니다. "
        content += "특히 주의사항에 해당하는 부분들은 미리 대비하여 부정적 영향을 최소화하시기 바랍니다."
        
        return content
    
    def _analyze_balance(self, sipsung_counts, total_count):
        """십성 균형 분석"""
        if total_count == 0:
            return "십성 데이터가 없습니다."
        
        # 각 십성의 비율 계산
        ratios = {k: v/total_count for k, v in sipsung_counts.items()}
        
        # 가장 많은 십성과 가장 적은 십성 찾기
        max_sipsung = max(ratios.items(), key=lambda x: x[1])
        min_sipsung = min(ratios.items(), key=lambda x: x[1])
        
        analysis = f"십성 균형도 분석:{chr(10)}"
        analysis += f"▣ 가장 강한 십성: {max_sipsung[0]} ({max_sipsung[1]*100:.1f}%){chr(10)}"
        analysis += f"▣ 가장 약한 십성: {min_sipsung[0]} ({min_sipsung[1]*100:.1f}%){chr(10) * 2}"
        
        # 균형 평가
        if max_sipsung[1] > 0.4:
            analysis += f"{max_sipsung[0]}이(가) 매우 강하게 나타나므로, 이와 관련된 특성이 두드러집니다.{chr(10)}"
        elif max_sipsung[1] < 0.2:
            analysis += f"십성이 비교적 균형있게 분포되어 있어 다재다능한 성향을 보입니다.{chr(10)}"
        
        return analysis
    
    def _get_sipsung_character(self, sipsung):
        """십성별 성격 특징"""
        characters = {
            '비견': '독립적이고 자존심이 강하며 경쟁심이 많습니다',
            '겁재': '적극적이고 도전적이며 모험을 즐깁니다',
            '식신': '창의적이고 표현력이 뛰어나며 여유로운 성격입니다',
            '상관': '예리하고 비판적이며 완벽주의 성향이 있습니다',
            '정재': '안정적이고 계획적이며 실용적인 성격입니다',
            '편재': '유연하고 적응력이 뛰어나며 기회포착에 능합니다',
            '정관': '책임감이 강하고 원칙적이며 리더십이 있습니다',
            '편관': '추진력이 강하고 결단력이 있으며 행동파입니다',
            '정인': '지적이고 학구적이며 전통을 중시합니다',
            '편인': '독창적이고 직관적이며 예술적 감각이 뛰어납니다'
        }
        return characters.get(sipsung, '독특한 개성을 가지고 있습니다')
    
    def _get_sipsung_career(self, sipsung):
        """십성별 직업 성향"""
        careers = {
            '비견': '독립사업, 프리랜서, 전문직에 적합합니다',
            '겁재': '영업, 무역, 스포츠 분야에 적합합니다',
            '식신': '예술, 요리, 교육 분야에 적합합니다',
            '상관': '기술직, 연구직, 비평가에 적합합니다',
            '정재': '금융, 회계, 행정 분야에 적합합니다',
            '편재': '사업, 투자, 컨설팅 분야에 적합합니다',
            '정관': '공무원, 관리직, 법조계에 적합합니다',
            '편관': '군인, 경찰, 경영자에 적합합니다',
            '정인': '교수, 연구원, 종교인에 적합합니다',
            '편인': '디자이너, 작가, 발명가에 적합합니다'
        }
        return careers.get(sipsung, '다양한 분야에서 능력을 발휘할 수 있습니다')
    
    def _get_sipsung_relationship(self, sipsung):
        """십성별 대인관계 특성"""
        relationships = {
            '비견': '동료와의 경쟁 관계가 많지만 의리가 있습니다',
            '겁재': '활발한 인맥을 형성하며 리더 역할을 합니다',
            '식신': '부드럽고 원만한 대인관계를 유지합니다',
            '상관': '까다로운 면이 있지만 진실된 관계를 추구합니다',
            '정재': '신뢰를 바탕으로 한 안정적인 관계를 형성합니다',
            '편재': '폭넓은 인간관계를 가지며 적응력이 뛰어납니다',
            '정관': '상하관계가 분명하며 책임감 있는 관계를 맺습니다',
            '편관': '카리스마가 있어 사람들을 이끄는 힘이 있습니다',
            '정인': '스승이나 멘토 역할을 하며 존경받습니다',
            '편인': '독특한 개성으로 특별한 인연을 맺습니다'
        }
        return relationships.get(sipsung, '자신만의 독특한 대인관계를 형성합니다')
    
    def _analyze_by_period(self, sipsung_data):
        """시기별 십성 분석"""
        periods = ['year', 'month', 'day', 'hour']
        period_names = {'year': '연주', 'month': '월주', 'day': '일주', 'hour': '시주'}
        
        analysis = {}
        for period in periods:
            if period in sipsung_data:
                sipsung = sipsung_data[period]
                if sipsung and sipsung != '미확인':
                    analysis[period_names[period]] = {
                        'sipsung': sipsung,
                        'character': self._get_sipsung_character(sipsung),
                        'impact': self._get_period_impact(period, sipsung)
                    }
        
        return analysis
    
    def _get_period_impact(self, period, sipsung):
        """시기별 십성의 영향 분석"""
        period_map = {
            'year': '조상과 사회적 기반',
            'month': '부모와 성장 환경',
            'day': '본인의 핵심 성격',
            'hour': '자녀와 미래 가능성'
        }
        
        impact_map = {
            '비견': '독립적이고 자기주장이 강한',
            '겁재': '경쟁적이고 도전적인',
            '식신': '창의적이고 여유로운',
            '상관': '비판적이고 개혁적인',
            '정재': '안정적이고 보수적인',
            '편재': '유연하고 기회주의적인',
            '정관': '책임감 있고 규율적인',
            '편관': '추진력 있고 결단력 있는',
            '정인': '학구적이고 전통적인',
            '편인': '직관적이고 독창적인'
        }
        
        base = period_map.get(period, '인생')
        character = impact_map.get(sipsung, '독특한')
        
        return f"{base}에서 {character} 특성이 나타납니다."
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '십성 분석',
            'content': '십성 분석 데이터를 준비 중입니다.',
            'sipsung_counts': {},
            'comprehensive': '종합 분석을 준비 중입니다.',
            'period_analysis': {}
        }