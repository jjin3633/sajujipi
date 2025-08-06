# 십이신살 분석 모듈
class SibisinsalAnalyzer:
    """십이신살 분석을 담당하는 클래스"""

    # 삼합(三合)을 기준으로 십이신살을 찾기 위한 테이블
    SAMHAB_TABLE = {
        '해묘미': ['겁살-신', '재살-유', '천살-술', '지살-해', '년살-자', '월살-축', '망신살-인', '장성살-묘', '반안살-진', '역마살-사', '육해살-오', '화개살-미'],
        '인오술': ['겁살-해', '재살-자', '천살-축', '지살-인', '년살-묘', '월살-진', '망신살-사', '장성살-오', '반안살-미', '역마살-신', '육해살-유', '화개살-술'],
        '사유축': ['겁살-인', '재살-묘', '천살-진', '지살-사', '년살-오', '월살-미', '망신살-신', '장성살-유', '반안살-술', '역마살-해', '육해살-자', '화개살-축'],
        '신자진': ['겁살-사', '재살-오', '천살-미', '지살-신', '년살-유', '월살-술', '망신살-해', '장성살-자', '반안살-축', '역마살-인', '육해살-묘', '화개살-진']
    }
    
    # 각 신살에 대한 설명
    SINSAL_DETAILS = {
        '지살': '변동과 이동의 시작. 새로운 환경에 적응하고 개척하는 능력이 뛰어납니다.',
        '년살': '매력과 인기의 상징 (도화살). 사람들의 시선을 끌고, 예술적 감각이 뛰어납니다.',
        '월살': '정체와 고독. 장애물이 많아 답답함을 느낄 수 있지만, 내면 성찰의 기회가 됩니다.',
        '망신살': '숨겨진 것이 드러남. 실수나 비밀이 탄로 날 수 있으니 언행에 신중해야 합니다.',
        '장성살': '권력과 리더십. 강한 추진력과 책임감으로 집단을 이끄는 힘이 있습니다.',
        '반안살': '안정과 성공. 말의 안장에 오른 것처럼 출세와 명예를 얻고 안정된 삶을 누립니다.',
        '역마살': '끊임없는 이동과 변화. 분주하게 활동하며 해외, 출장, 이사 등과 인연이 깊습니다.',
        '육해살': '심리적 고통과 장애. 피로가 누적되고 스트레스가 많아 건강 관리가 필수적입니다.',
        '화개살': '예술과 종교, 학문. 화려함을 덮는다는 의미로, 내면의 깊이가 있고 정신적 세계를 추구합니다.',
        '겁살': '상실과 빼앗김. 재물, 건강, 인간관계에서 손실을 볼 수 있으니 지키는 것이 중요합니다.',
        '재살': '수옥살이라고도 하며, 구속과 갈등을 의미합니다. 관재구설이나 시비에 휘말릴 수 있습니다.',
        '천살': '하늘의 재앙. 예상치 못한 재난이나 불가항력적인 어려움을 겪을 수 있습니다.'
    }

    def analyze(self, saju_pillars):
        """십이신살 분석 수행"""
        try:
            sinsal_result = self._calculate_sibisinsal(saju_pillars)
            periods = self._analyze_by_period(sinsal_result)
            
            return {
                'title': '십이신살 분석',
                'content': self._generate_analysis_content(sinsal_result),
                'periods': periods,
                'sibisinsal_found': sinsal_result
            }
        except Exception as e:
            print(f"십이신살 분석 중 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._get_default_analysis()

    def _get_samhab_group(self, jiji):
        """지지에 해당하는 삼합 그룹 찾기"""
        for group, members in {'해묘미':['해','묘','미'], '인오술':['인','오','술'], '사유축':['사','유','축'], '신자진':['신','자','진']}.items():
            if jiji in members:
                return group
        return None

    def _calculate_sibisinsal(self, saju_pillars):
        """연지를 기준으로 십이신살 계산"""
        year_ji = saju_pillars.get('year', {}).get('ji')
        if not year_ji:
            return {}

        samhab_group = self._get_samhab_group(year_ji)
        if not samhab_group:
            return {}
            
        found_sinsal = {}
        sinsal_map = self.SAMHAB_TABLE.get(samhab_group, [])
        position_names = {'year': '연지', 'month': '월지', 'day': '일지', 'hour': '시지'}

        for pos, pos_name in position_names.items():
            jiji = saju_pillars.get(pos, {}).get('ji')
            if not jiji:
                continue
            
            for sinsal_info in sinsal_map:
                sinsal, sinsal_jiji = sinsal_info.split('-')
                if jiji == sinsal_jiji:
                    if sinsal not in found_sinsal:
                        found_sinsal[sinsal] = []
                    if pos_name not in found_sinsal[sinsal]:
                         found_sinsal[sinsal].append(pos_name)
        
        return found_sinsal

    def _analyze_by_period(self, sinsal_result):
        """시기별 십이신살 영향 분석"""
        periods = []
        position_map = {'연지': '초년운', '월지': '청년운', '일지': '중년운', '시지': '말년운'}

        for pos_name, period_name in position_map.items():
            sinsals_in_period = [sinsal for sinsal, positions in sinsal_result.items() if pos_name in positions]
            
            description = f"당신의 {period_name}은 "
            if not sinsals_in_period:
                description += "특별한 신살의 영향 없이 평탄하게 흘러갑니다."
            else:
                sinsal_descs = [f"'{s}'의 영향" for s in sinsals_in_period]
                description += f"{', '.join(sinsal_descs)}으로 다채로운 경험을 하게 됩니다."
            
            periods.append({'title': f'{period_name} ({pos_name})', 'description': description})
        
        return periods

    def _generate_analysis_content(self, sinsal_result):
        """십이신살 종합 분석 내용 생성"""
        content = "【십이신살 분석】\n\n십이신살은 당신의 인생 각 시기에 나타나는 12가지 주요 기운을 의미합니다.\n\n"
        
        if not sinsal_result:
            content += "특별히 강하게 작용하는 신살은 없으며, 자신의 의지와 노력으로 운명을 개척해나가는 사주입니다."
        else:
            content += "【당신에게 영향을 주는 주요 신살】\n"
            for sinsal, positions in sorted(sinsal_result.items()):
                pos_str = ', '.join(positions)
                detail = self.SINSAL_DETAILS.get(sinsal, "해당 신살에 대한 정보가 없습니다.")
                content += f"- {sinsal} ({pos_str}): {detail}\n"

        content += "\n【신살 활용법】\n- 길신(장성살, 반안살 등)은 그 힘을 적극 활용하여 기회로 삼으세요.\n- 흉신(겁살, 재살 등)은 그 의미를 미리 알고 대비하여 피해를 최소화하세요.\n- 모든 신살은 양면성이 있으니, 긍정적인 면을 보고 발전의 계기로 삼는 지혜가 필요합니다."
        return content

    def _get_default_analysis(self):
        """기본 분석 결과 반환"""
        return {
            'title': '십이신살 분석',
            'content': '십이신살 분석 데이터를 준비 중입니다.',
            'periods': [],
            'sibisinsal_found': {}
        }
