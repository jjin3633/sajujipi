# 분석 모듈 초기화
from .ilju_analyzer import IljuAnalyzer
from .sipsung_analyzer import SipsungAnalyzer
from .sibiunseong_analyzer import SibiunseongAnalyzer
from .sibisinsal_analyzer import SibisinsalAnalyzer
from .guin_analyzer import GuinAnalyzer
from .wealth_analyzer import WealthAnalyzer
from .love_analyzer import LoveAnalyzer
from .career_analyzer import CareerAnalyzer
from .health_analyzer import HealthAnalyzer
from .daeun_analyzer import DaeunAnalyzer

__all__ = [
    'IljuAnalyzer',
    'SipsungAnalyzer',
    'SibiunseongAnalyzer',
    'SibisinsalAnalyzer',
    'GuinAnalyzer',
    'WealthAnalyzer',
    'LoveAnalyzer',
    'CareerAnalyzer',
    'HealthAnalyzer',
    'DaeunAnalyzer'
]