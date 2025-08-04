from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logic.analyzer import get_saju_details
# Pydantic BaseModel은 더 이상 사용하지 않습니다.

app = FastAPI()

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
async def get_analysis(request: Request):
    # Request 객체로부터 JSON 데이터를 직접 받습니다.
    birth_data_json = await request.json()
    
    # 분석 함수로 데이터를 전달합니다.
    analysis_result = get_saju_details(
        birth_data_json.get('year'),
        birth_data_json.get('month'),
        birth_data_json.get('day'),
        birth_data_json.get('hour'),
        birth_data_json.get('minute')
    )

    return {
        "request_data": birth_data_json,
        "analysis_result": analysis_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)