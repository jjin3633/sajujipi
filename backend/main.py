from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

# CORS 설정 (개발 시 모든 출처 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "사주팔자 전문가 AI 역술가입니다."}

@app.post("/analysis")
def get_analysis(birth_date: dict):
    # 실제 분석 로직은 여기에 추가될 것입니다.
    # 지금은 테스트를 위해 입력값을 그대로 반환합니다.
    year = birth_date.get('year')
    month = birth_date.get('month')
    day = birth_date.get('day')
    hour = birth_date.get('hour')
    minute = birth_date.get('minute')

    # 간단한 일주 분석 예시 (실제 로직으로 대체 필요)
    # 여기서는 갑술일주로 고정합니다.
    ilju_analysis = {
        "title": "갑술(甲戌) 일주 분석: 황야에 선 거목(巨木)",
        "description": "당신의 삶의 근본이자 본질을 나타내는 일주는 갑술(甲戌)입니다. 이는 마치 가을의 마른 대지, 혹은 황량한 산 위에 홀로 우뚝 솟은 거대한 소나무와 같은 형상입니다.",
        "pros": ["강한 책임감과 리더십", "정직함과 신용", "뛰어난 재물 관리 능력"],
        "cons": ["고집과 독선", "내면의 고독감", "다혈질적인 면모"],
        "animal": "푸른 개 (靑犬)"
    }

    return {
        "request_data": {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute
        },
        "analysis_result": ilju_analysis
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
