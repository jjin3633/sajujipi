# 사주지피 프로젝트 구조

## 📁 프로젝트 구조

```
sajujipi-main/
├── frontend/                    # 프론트엔드
│   ├── index.html              # 메인 HTML
│   ├── css/                    # CSS 모듈
│   │   ├── main.css           # 메인 CSS (모든 스타일 통합)
│   │   ├── base.css           # 기본 스타일 및 변수
│   │   ├── layout.css         # 레이아웃 스타일
│   │   ├── components.css     # 컴포넌트 스타일
│   │   ├── analysis.css       # 분석 결과 전용 스타일
│   │   └── responsive.css     # 반응형 디자인
│   └── js/                     # JavaScript 모듈
│       ├── main.js            # 메인 애플리케이션
│       ├── config.js          # 설정
│       ├── utils.js           # 유틸리티 함수
│       ├── api.js             # API 통신
│       ├── form-validator.js  # 폼 유효성 검사
│       └── display/           # 디스플레이 모듈
│           ├── index.js       # 디스플레이 매니저
│           ├── base-display.js # 기본 디스플레이 클래스
│           ├── ilju-display.js # 일주 분석 디스플레이
│           └── ...            # 기타 분석 디스플레이
│
├── backend/                     # 백엔드
│   ├── main.py                 # Flask 앱 진입점
│   ├── logic/                  # 비즈니스 로직
│   │   ├── saju_analyzer.py   # 메인 분석기
│   │   ├── saju_calculator.py # 사주 계산기
│   │   ├── report_generator.py # 리포트 생성기
│   │   └── analysis/          # 분석 모듈
│   │       ├── __init__.py
│   │       ├── ilju_analyzer.py
│   │       ├── sipsung_analyzer.py
│   │       ├── sibiunseong_analyzer.py
│   │       └── ...
│   └── data/                   # 데이터 파일
│       ├── ilju_data.json
│       ├── ganji_data.json
│       ├── sipsung_data.json
│       └── ...
│
├── README.md                   # 프로젝트 설명
├── requirements.txt            # Python 의존성
└── PROJECT_STRUCTURE.md        # 이 파일

```

## 🔧 주요 개선사항

### 1. 백엔드 구조 개선
- **모듈화**: 각 분석 기능을 독립적인 모듈로 분리
- **계층 분리**: 계산 로직, 분석 로직, 리포트 생성을 별도 계층으로 구성
- **확장성**: 새로운 분석 기능 추가가 용이한 구조

### 2. 프론트엔드 구조 개선
- **ES6 모듈**: 최신 JavaScript 모듈 시스템 사용
- **컴포넌트 기반**: 각 분석 섹션을 독립적인 컴포넌트로 관리
- **관심사 분리**: API 통신, UI 표시, 유틸리티를 별도 모듈로 분리

### 3. CSS 최적화
- **CSS 변수**: 일관된 디자인 시스템을 위한 CSS 커스텀 프로퍼티
- **모듈화**: 기능별로 CSS 파일 분리
- **반응형**: 모바일부터 데스크톱까지 완벽 지원
- **다크모드**: 시스템 설정에 따른 다크모드 지원

### 4. 코드 품질
- **재사용성**: 공통 기능을 베이스 클래스로 추상화
- **유지보수성**: 명확한 폴더 구조와 네이밍 컨벤션
- **확장성**: 새로운 기능 추가가 용이한 아키텍처

## 🚀 장점

1. **성능 향상**
   - 모듈 지연 로딩으로 초기 로드 시간 단축
   - CSS 최적화로 렌더링 성능 개선

2. **개발 효율성**
   - 명확한 구조로 코드 찾기 쉬움
   - 기능별 독립 개발 가능

3. **유지보수**
   - 버그 수정 시 영향 범위 최소화
   - 테스트 작성 용이

4. **확장성**
   - 새로운 분석 기능 추가 용이
   - 다국어 지원 등 추가 기능 구현 쉬움