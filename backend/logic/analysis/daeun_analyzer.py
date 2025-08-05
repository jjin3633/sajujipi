# 대운 분석 모듈
import datetime

class DaeunAnalyzer:
    """대운 분석을 담당하는 클래스"""
    
    # 천간 순서
    CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
    # 지지 순서
    JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
    
    def analyze(self, saju_pillars, current_year=None):
        """대운 분석 수행"""
        try:
            if current_year is None:
                current_year = datetime.datetime.now().year
            
            # 생년 추출 (간단한 예시 - 실제로는 더 복잡한 계산 필요)
            birth_year = current_year - 25  # 임시로 25세로 가정
            
            # 대운 계산
            daeun_periods = self._calculate_daeun_periods(saju_pillars, birth_year, current_year)
            
            # 세운 계산
            seun_periods = self._calculate_seun_periods(current_year)
            
            # 변화점 분석
            change_points = self._analyze_change_points(daeun_periods, current_year - birth_year)
            
            # 미래 전망
            future_outlook = self._generate_future_outlook(daeun_periods, current_year - birth_year)
            
            return {
                'title': '대운 분석',
                'content': self._generate_analysis_content(daeun_periods, seun_periods),
                'daeun_periods': daeun_periods,
                'seun_periods': seun_periods,
                'change_points': change_points,
                'future_outlook': future_outlook
            }
        except Exception as e:
            print(f"대운 분석 중 오류: {str(e)}")
            return self._get_default_analysis()
    
    def _generate_daeun_periods(self):
        """대운 기간 생성"""
        return [
            {'title': '1대운 (0~9세)', 'description': '이미 지나간 대운입니다. 이 시기의 경험이 현재에 영향을 미칩니다.', 'status': 'past'},
            {'title': '2대운 (10~19세)', 'description': '이미 지나간 대운입니다. 이 시기의 경험이 현재에 영향을 미칩니다.', 'status': 'past'},
            {'title': '3대운 (20~29세)', 'description': '현재 진행 중인 대운입니다. 이 시기는 인생의 중요한 변화점이 될 수 있습니다.', 'status': 'present'},
            {'title': '4대운 (30~39세)', 'description': '앞으로 맞이할 대운입니다. 준비를 통해 좋은 결과를 얻을 수 있습니다.', 'status': 'future'},
            {'title': '5대운 (40~49세)', 'description': '앞으로 맞이할 대운입니다. 준비를 통해 좋은 결과를 얻을 수 있습니다.', 'status': 'future'}
        ]
    
    def _generate_seun_periods(self, current_year):
        """세운 기간 생성"""
        periods = []
        for i in range(-2, 3):
            year = current_year + i
            if i < 0:
                status = 'past'
                desc = f'{abs(i)}년 전 세운입니다. 이 시기의 경험이 현재에 영향을 미칩니다.'
            elif i == 0:
                status = 'present'
                desc = '현재 진행 중인 세운입니다. 올해의 운세가 인생에 큰 영향을 미칩니다.'
            else:
                status = 'future'
                desc = f'{i}년 후 세운입니다. 준비를 통해 좋은 결과를 얻을 수 있습니다.'
            
            periods.append({
                'year': year,
                'description': desc,
                'status': status
            })
        
        return periods
    
    def _generate_change_points(self):
        """변화점 생성"""
        return [
            {
                'title': '20대 후반',
                'description': '첫 번째 인생 변화점입니다. 직업이나 연애에서 중요한 결정을 내려야 할 시기입니다.'
            }
        ]
    
    def _generate_analysis_content(self):
        """대운 분석 내용 생성"""
        content = f"【대운 분석】{chr(10) * 2}"
        content += f"대운은 당신의 인생에서 10년 단위로 변화하는 운세를 나타냅니다.{chr(10)}"
        content += f"각 대운마다 다른 특성과 기회가 있으며, 이를 잘 활용하는 것이 중요합니다.{chr(10)}"
        
        return content
    
    def _get_default_analysis(self):
        """기본 분석 결과"""
        return {
            'title': '대운 분석',
            'content': '대운 분석 데이터를 준비 중입니다.',
            'daeun_periods': [],
            'seun_periods': [],
            'change_points': [],
            'future_outlook': ''
        }