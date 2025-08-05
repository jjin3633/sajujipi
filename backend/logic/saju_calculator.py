# 사주 기본 계산 모듈
from datetime import datetime
import json
import os

class SajuCalculator:
    """사주팔자 기본 계산을 담당하는 클래스"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self._load_data()
    
    def _load_data(self):
        """필요한 데이터 파일들을 로드"""
        # 천간 지지 데이터
        with open(os.path.join(self.data_dir, 'ganji_data.json'), 'r', encoding='utf-8') as f:
            self.ganji_data = json.load(f)
        
        # 만세력 데이터
        with open(os.path.join(self.data_dir, 'calendar_data.json'), 'r', encoding='utf-8') as f:
            self.calendar_data = json.load(f)
        
        # 십성 데이터
        with open(os.path.join(self.data_dir, 'sipsung_data.json'), 'r', encoding='utf-8') as f:
            self.sipsung_data = json.load(f)
    
    def calculate_saju_pillars(self, year, month, day, hour, minute):
        """사주 팔자를 계산하여 반환"""
        try:
            # 양력을 음력으로 변환
            lunar_date = self._solar_to_lunar(year, month, day)
            
            # 연주 계산
            year_pillar = self._calculate_year_pillar(lunar_date['year'])
            
            # 월주 계산
            month_pillar = self._calculate_month_pillar(lunar_date['year'], lunar_date['month'])
            
            # 일주 계산
            day_pillar = self._calculate_day_pillar(year, month, day)
            
            # 시주 계산
            hour_pillar = self._calculate_hour_pillar(day_pillar['gan'], hour)
            
            return {
                'year': year_pillar,
                'month': month_pillar,
                'day': day_pillar,
                'hour': hour_pillar,
                'lunar_date': lunar_date
            }
        except Exception as e:
            print(f"사주 계산 오류: {str(e)}")
            raise
    
    def _solar_to_lunar(self, year, month, day):
        """양력을 음력으로 변환"""
        # 실제 변환 로직 구현 필요
        # 여기서는 간단한 예시만 제공
        return {
            'year': year,
            'month': month,
            'day': day,
            'is_leap': False
        }
    
    def _calculate_year_pillar(self, year):
        """연주 계산"""
        gan_cycle = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
        ji_cycle = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
        
        # 60갑자 계산
        gan_index = (year - 4) % 10
        ji_index = (year - 4) % 12
        
        return {
            'gan': gan_cycle[gan_index],
            'ji': ji_cycle[ji_index]
        }
    
    def _calculate_month_pillar(self, year, month):
        """월주 계산"""
        # 월간 계산 (년간에 따라 결정)
        month_gan_table = {
            '갑': ['병', '정', '무', '기', '경', '신', '임', '계', '갑', '을', '병', '정'],
            '을': ['무', '기', '경', '신', '임', '계', '갑', '을', '병', '정', '무', '기'],
            '병': ['경', '신', '임', '계', '갑', '을', '병', '정', '무', '기', '경', '신'],
            '정': ['임', '계', '갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'],
            '무': ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계', '갑', '을'],
            '기': ['병', '정', '무', '기', '경', '신', '임', '계', '갑', '을', '병', '정'],
            '경': ['무', '기', '경', '신', '임', '계', '갑', '을', '병', '정', '무', '기'],
            '신': ['경', '신', '임', '계', '갑', '을', '병', '정', '무', '기', '경', '신'],
            '임': ['임', '계', '갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'],
            '계': ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계', '갑', '을']
        }
        
        year_gan = self._calculate_year_pillar(year)['gan']
        month_ji = ['인', '묘', '진', '사', '오', '미', '신', '유', '술', '해', '자', '축'][month - 1]
        
        return {
            'gan': month_gan_table[year_gan][month - 1],
            'ji': month_ji
        }
    
    def _calculate_day_pillar(self, year, month, day):
        """일주 계산"""
        # 만세력 데이터에서 일주 찾기
        date_key = f"{year}-{month:02d}-{day:02d}"
        if date_key in self.calendar_data:
            return self.calendar_data[date_key]
        
        # 기본 계산 로직 (실제로는 더 복잡함)
        gan_cycle = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
        ji_cycle = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
        
        # 간단한 예시 계산
        days_from_base = (datetime(year, month, day) - datetime(1900, 1, 1)).days
        gan_index = days_from_base % 10
        ji_index = days_from_base % 12
        
        return {
            'gan': gan_cycle[gan_index],
            'ji': ji_cycle[ji_index]
        }
    
    def _calculate_hour_pillar(self, day_gan, hour):
        """시주 계산"""
        # 시간을 지지로 변환
        hour_ji_map = {
            (23, 1): '자', (1, 3): '축', (3, 5): '인', (5, 7): '묘',
            (7, 9): '진', (9, 11): '사', (11, 13): '오', (13, 15): '미',
            (15, 17): '신', (17, 19): '유', (19, 21): '술', (21, 23): '해'
        }
        
        hour_ji = '자'  # 기본값
        for (start, end), ji in hour_ji_map.items():
            if start <= hour < end or (start == 23 and hour >= 23) or (start == 23 and hour < 1):
                hour_ji = ji
                break
        
        # 시간 천간 계산 (일간에 따라 결정)
        hour_gan_table = {
            '갑': ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계', '갑', '을'],
            '을': ['병', '정', '무', '기', '경', '신', '임', '계', '갑', '을', '병', '정'],
            '병': ['무', '기', '경', '신', '임', '계', '갑', '을', '병', '정', '무', '기'],
            '정': ['경', '신', '임', '계', '갑', '을', '병', '정', '무', '기', '경', '신'],
            '무': ['임', '계', '갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'],
            '기': ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계', '갑', '을'],
            '경': ['병', '정', '무', '기', '경', '신', '임', '계', '갑', '을', '병', '정'],
            '신': ['무', '기', '경', '신', '임', '계', '갑', '을', '병', '정', '무', '기'],
            '임': ['경', '신', '임', '계', '갑', '을', '병', '정', '무', '기', '경', '신'],
            '계': ['임', '계', '갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
        }
        
        ji_index = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해'].index(hour_ji)
        hour_gan = hour_gan_table[day_gan][ji_index]
        
        return {
            'gan': hour_gan,
            'ji': hour_ji
        }
    
    def calculate_sipsung(self, day_gan, target_gan):
        """십성 계산"""
        sipsung_map = self.sipsung_data.get(day_gan, {})
        return sipsung_map.get(target_gan, "알 수 없음")