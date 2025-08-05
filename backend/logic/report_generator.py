# 리포트 생성 모듈
class ReportGenerator:
    """종합 리포트를 생성하는 클래스"""
    
    def generate_comprehensive_report(self, analysis_results):
        """종합 리포트 생성"""
        try:
            final_summary = self._generate_final_summary(analysis_results)
            
            return {
                'final_summary': final_summary,
                'sibisinsal_analysis': analysis_results.get('sibisinsal_analysis', {}),
                'guin_analysis': analysis_results.get('guin_analysis', {}),
                'career_analysis': self._format_career_analysis(analysis_results.get('career_luck_analysis', {})),
                'daeun_analysis': self._format_daeun_analysis(analysis_results.get('daeun_analysis', {}))
            }
        except Exception as e:
            print(f"리포트 생성 중 오류: {str(e)}")
            return self._get_default_report()
    
    def _generate_final_summary(self, analysis_results):
        """최종 요약 생성"""
        saju_pillars = analysis_results.get('saju_pillars', {})
        ilju = saju_pillars.get('day', '미확인')
        
        content = f"""【종합 리포트】

20년 역술가의 관점에서 당신의 사주를 종합적으로 분석한 결과입니다.

【사주 기본 정보】
• 일주: {ilju}
• 사주 구성: {saju_pillars.get('year', '')}년 {saju_pillars.get('month', '')}월 {saju_pillars.get('day', '')}일 {saju_pillars.get('hour', '')}시

【핵심 분석 요약】

1. 성격적 특징
당신의 사주는 {ilju}일주의 특성을 기본으로 하여 독특한 성격을 형성합니다.

2. 대인관계 분석
사주에서 나타나는 십성과 운성의 조합을 보면, 특정 유형의 사람들과 잘 어울리며, 특정 시기에는 대인관계에서 특별한 변화가 있을 수 있습니다.

3. 직업적 성향
일주의 특성과 십성의 조합을 고려할 때, 특정 분야의 직업이나 활동이 적합합니다.

4. 운세의 흐름
십이운성의 조합을 보면, 특정 시기의 기운이 강하게 나타나는 시기가 있으며, 이 시기에는 중요한 변화가 있을 수 있습니다.

【전문가 권장사항】

1. 성격 개발
• 강점 활용: 사주의 긍정적 면모를 최대한 활용하세요.
• 약점 보완: 주의사항에 해당하는 부분들을 미리 대비하여 부정적 영향을 최소화하세요.

2. 대인관계 관리
• 적합한 관계: 특정 유형의 사람들과의 관계를 중시하세요.
• 갈등 해결: 특정 시기의 기운이 나타나는 시기에는 대인관계에 특별히 주의하세요.

3. 직업적 발전
• 적합한 분야: 사주 특성과 관련된 직업 분야를 고려하세요.
• 발전 방향: 특정 분야의 특성을 활용한 발전 방향을 모색하세요.

4. 운세 활용
• 긍정적 시기: 긍정적인 기운이 나타나는 시기에는 적극적으로 활동하세요.
• 주의 시기: 도전적인 기운이 나타나는 시기에는 신중하게 대응하세요.

【미래 전망】
당신의 사주를 종합적으로 분석한 결과, 사주의 긍정적 면모를 잘 활용하면 특정 분야에서 큰 성공을 거둘 수 있을 것으로 보입니다. 
특히 특정 시기의 기운이 강하게 나타나는 시기에는 중요한 기회가 있을 수 있으니 미리 준비하시기 바랍니다.

이상의 분석은 20년 역술가의 경험을 바탕으로 한 전문적인 해석입니다. 
당신의 사주 특성을 잘 파악하고 긍정적 면모를 최대한 활용하여 행복하고 성공적인 인생을 살아가시기 바랍니다."""
        
        return {
            'content': content,
            'title': '종합 리포트'
        }
    
    def _format_career_analysis(self, career_data):
        """직업운 분석 포맷"""
        content = f"""【직업운 분석】

직업운은 당신의 직업과 관련된 운세를 나타냅니다.

【나와 잘맞는 직업/직장】

{', '.join(career_data.get('suitable_jobs', []))}

【사업 vs 직장 나에겐 뭐가 맞을까 분석】

{career_data.get('business_vs_job', '사업과 직장 비교 분석입니다.')}

【성공적인 직장생활을 위한 조언】

{career_data.get('advice', '직장생활을 위한 조언입니다.')}

【주의해야 할 사람 분석】

{career_data.get('caution_people', '직장에서 주의해야 할 사람 분석입니다.')}

【전문가 해석】
직업운의 조합을 통해 당신의 적합한 직업과 성공 가능성을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 적합한 직업: 당신에게 잘 맞는 직업이나 활동 분야를 나타냅니다.
2. 사업 vs 직장: 사업과 직장 중 어느 것이 더 적합한지 나타냅니다.
3. 성공 요인: 직장에서 성공하기 위한 중요한 요소들을 나타냅니다.
4. 주의사항: 직장에서 주의해야 할 사람이나 상황을 나타냅니다.

【전문가 조언】
직업운의 특성을 잘 파악하고 적절한 직업 선택과 발전을 하는 것이 중요합니다."""
        
        return {
            'title': '직업운 분석',
            'content': content,
            'suitable_jobs': career_data.get('suitable_jobs', []),
            'business_vs_job': career_data.get('business_vs_job', ''),
            'advice': career_data.get('advice', ''),
            'caution_people': career_data.get('caution_people', '')
        }
    
    def _format_daeun_analysis(self, daeun_data):
        """대운 분석 포맷"""
        content = f"""【대운 분석】

대운은 당신의 인생에서 10년 단위로 변화하는 운세를 나타냅니다.

【90세까지의 대운】

{self._format_daeun_periods(daeun_data.get('daeun_periods', []))}

【향후 5년간의 연운과 삼재】

{self._format_seun_periods(daeun_data.get('seun_periods', []))}

【향후 5년 동안의 연운】

대운 분석을 위해서는 원래 날짜 정보가 필요합니다.

【곧 맞딱뜨릴 삼재】

{self._format_change_points(daeun_data.get('change_points', []))}

【전문가 해석】
대운의 조합을 통해 당신의 인생 흐름과 중요한 변화점을 종합적으로 분석할 수 있습니다.

【인생에서의 영향】
1. 대운: 10년 단위로 변화하는 운세가 인생에 큰 영향을 미칩니다.
2. 세운: 1년 단위로 변화하는 운세가 당해의 운세를 결정합니다.
3. 변화점: 인생에서 중요한 변화가 일어나는 시기를 나타냅니다.
4. 미래 전망: 앞으로의 인생 흐름을 예측할 수 있습니다.

【전문가 조언】
대운의 특성을 잘 파악하고 적절한 준비와 대응을 하는 것이 중요합니다."""
        
        return {
            'title': '대운 분석',
            'content': content,
            'daeun_periods': daeun_data.get('daeun_periods', []),
            'seun_periods': daeun_data.get('seun_periods', []),
            'change_points': daeun_data.get('change_points', []),
            'future_outlook': daeun_data.get('future_outlook', '')
        }
    
    def _format_daeun_periods(self, periods):
        """대운 기간 포맷"""
        if not periods:
            return "대운 데이터가 없습니다."
        
        result = []
        for period in periods:
            status = "과거" if period.get('status') == 'past' else "현재" if period.get('status') == 'present' else "미래"
            result.append(f"{period.get('title', '')}\n{status}: {period.get('description', '')}")
        
        return chr(10).join(result)
    
    def _format_seun_periods(self, periods):
        """세운 기간 포맷"""
        if not periods:
            return "세운 데이터가 없습니다."
        
        result = []
        for period in periods:
            status = "과거" if period.get('status') == 'past' else "현재" if period.get('status') == 'present' else "미래"
            result.append(f"{period.get('year', '')}년\n{status}: {period.get('description', '')}")
        
        return chr(10).join(result)
    
    def _format_change_points(self, points):
        """변화점 포맷"""
        if not points:
            return "변화점 데이터가 없습니다."
        
        result = []
        for point in points:
            result.append(f"{point.get('title', '')}\n{point.get('description', '')}")
        
        return chr(10).join(result)
    
    def _get_default_report(self):
        """기본 리포트"""
        return {
            'final_summary': {
                'content': '종합 리포트를 준비 중입니다.',
                'title': '종합 리포트'
            },
            'sibisinsal_analysis': {},
            'guin_analysis': {},
            'career_analysis': {},
            'daeun_analysis': {}
        }