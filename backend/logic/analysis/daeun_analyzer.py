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

            # 생년 추출 (saju_pillars에서 year 정보 추출, 없으면 임시로 25세 가정)
            try:
                birth_year = int(saju_pillars['year']['year'])
            except Exception:
                birth_year = current_year - 25

            # 대운 계산
            daeun_periods = self._calculate_daeun_periods(saju_pillars, birth_year, current_year)
            # 세운 계산
            seun_periods = self._generate_seun_periods(current_year)
            # 변화점 분석
            change_points = self._generate_change_points(daeun_periods, current_year - birth_year)
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

    def _calculate_daeun_periods(self, saju_pillars, birth_year, current_year):
        """대운 기간 계산 (예시: 10년 단위로 5개 구간)"""
        periods = []
        for i in range(5):
            start_age = i * 10
            end_age = start_age + 9
            year_start = birth_year + start_age
            year_end = birth_year + end_age
            status = 'future'
            if current_year >= year_end:
                status = 'past'
            elif current_year >= year_start:
                status = 'present'
            periods.append({
                'title': f'{i+1}대운 ({start_age}~{end_age}세)',
                'description': f'{year_start}~{year_end}년',
                'status': status
            })
        return periods

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
    
    def _generate_change_points(self, daeun_periods, age):
        """변화점 생성 (예시: 20대 후반 등)"""
        points = []
        for period in daeun_periods:
            if '20' in period['title']:
                points.append({
                    'title': '20대 후반',
                    'description': '첫 번째 인생 변화점입니다. 직업이나 연애에서 중요한 결정을 내려야 할 시기입니다.'
                })
        return points
    
    def _generate_analysis_content(self, daeun_periods, seun_periods):
        """대운 분석 내용 생성"""
        content = f"【대운 분석】{chr(10) * 2}"
        content += f"대운은 당신의 인생에서 10년 단위로 변화하는 운세를 나타냅니다.{chr(10)}"
        content += f"각 대운마다 다른 특성과 기회가 있으며, 이를 잘 활용하는 것이 중요합니다.{chr(10)}"
        content += f"\n대운 구간: " + ', '.join([p['title'] for p in daeun_periods])
        return content
    
    def _generate_future_outlook(self, daeun_periods, age):
        """미래 전망 생성 (예시)"""
        future = [p for p in daeun_periods if p['status'] == 'future']
        if not future:
            return '앞으로의 대운이 모두 지나갔습니다.'
        return f"앞으로 {len(future)}개의 대운이 남아 있습니다. 준비를 잘 하세요."
    
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