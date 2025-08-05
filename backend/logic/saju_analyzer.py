# 사주 분석 메인 클래스
from .saju_calculator import SajuCalculator
from .analysis import (
    IljuAnalyzer, SipsungAnalyzer, SibiunseongAnalyzer,
    SibisinsalAnalyzer, GuinAnalyzer, WealthAnalyzer,
    LoveAnalyzer, CareerAnalyzer, HealthAnalyzer, DaeunAnalyzer
)
from .report_generator import ReportGenerator

class SajuAnalyzer:
    """사주 분석을 총괄하는 메인 클래스"""
    
    def __init__(self):
        # 계산기 초기화
        self.calculator = SajuCalculator()
        
        # 분석기들 초기화
        self.ilju_analyzer = IljuAnalyzer()
        self.sipsung_analyzer = SipsungAnalyzer()
        self.sibiunseong_analyzer = SibiunseongAnalyzer()
        self.sibisinsal_analyzer = SibisinsalAnalyzer()
        self.guin_analyzer = GuinAnalyzer()
        self.wealth_analyzer = WealthAnalyzer()
        self.love_analyzer = LoveAnalyzer()
        self.career_analyzer = CareerAnalyzer()
        self.health_analyzer = HealthAnalyzer()
        self.daeun_analyzer = DaeunAnalyzer()
        
        # 리포트 생성기
        self.report_generator = ReportGenerator()
    
    def analyze(self, year, month, day, hour, minute):
        """전체 사주 분석 수행"""
        try:
            # 1. 사주 팔자 계산
            saju_pillars = self.calculator.calculate_saju_pillars(year, month, day, hour, minute)
            
            # 2. 십성 계산
            sipsung_data = self._calculate_all_sipsung(saju_pillars)
            
            # 3. 각 부문별 분석 수행
            analysis_results = {
                'saju_pillars': saju_pillars,
                'sipsung_raw': sipsung_data,
                'ilju_analysis': self.ilju_analyzer.analyze(saju_pillars['day']),
                'sipsung_analysis': self.sipsung_analyzer.analyze(sipsung_data),
                'sibiunseong_analysis': self.sibiunseong_analyzer.analyze(saju_pillars),
                'sibisinsal_analysis': self.sibisinsal_analyzer.analyze(saju_pillars),
                'guin_analysis': self.guin_analyzer.analyze(saju_pillars),
                'wealth_analysis': self.wealth_analyzer.analyze(saju_pillars, sipsung_data),
                'love_analysis': self.love_analyzer.analyze(saju_pillars, sipsung_data),
                'career_analysis': self.career_analyzer.analyze(saju_pillars, sipsung_data),
                'health_analysis': self.health_analyzer.analyze(saju_pillars),
                'daeun_analysis': self.daeun_analyzer.analyze(year, month, day, saju_pillars)
            }
            
            # 4. 종합 리포트 생성
            comprehensive_report = self.report_generator.generate_comprehensive_report(
                analysis_results, year, month, day, hour, minute
            )
            
            return {
                **analysis_results,
                'comprehensive_report': comprehensive_report
            }
            
        except Exception as e:
            print(f"사주 분석 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def _calculate_all_sipsung(self, saju_pillars):
        """모든 기둥의 십성 계산"""
        day_gan = saju_pillars['day']['gan']
        
        return {
            'year_gan': self.calculator.calculate_sipsung(day_gan, saju_pillars['year']['gan']),
            'year_ji': self._calculate_ji_sipsung(day_gan, saju_pillars['year']['ji']),
            'month_gan': self.calculator.calculate_sipsung(day_gan, saju_pillars['month']['gan']),
            'month_ji': self._calculate_ji_sipsung(day_gan, saju_pillars['month']['ji']),
            'day_gan': '일간',
            'day_ji': self._calculate_ji_sipsung(day_gan, saju_pillars['day']['ji']),
            'hour_gan': self.calculator.calculate_sipsung(day_gan, saju_pillars['hour']['gan']),
            'hour_ji': self._calculate_ji_sipsung(day_gan, saju_pillars['hour']['ji'])
        }
    
    def _calculate_ji_sipsung(self, day_gan, ji):
        """지지의 십성 계산 (지장간 기준)"""
        # 지장간 매핑 (간단화된 버전)
        ji_to_gan = {
            '자': '계', '축': '계', '인': '갑', '묘': '을',
            '진': '무', '사': '병', '오': '정', '미': '기',
            '신': '경', '유': '신', '술': '무', '해': '임'
        }
        
        gan = ji_to_gan.get(ji, '')
        if gan:
            return self.calculator.calculate_sipsung(day_gan, gan)
        return "알 수 없음"

# 기존 analyzer.py와의 호환성을 위한 함수
def get_saju_details(year, month, day, hour, minute):
    """기존 인터페이스와의 호환성을 위한 wrapper 함수"""
    analyzer = SajuAnalyzer()
    return analyzer.analyze(year, month, day, hour, minute)