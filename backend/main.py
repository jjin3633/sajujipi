from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from logic.analyzer import get_saju_details
import traceback
import os

app = FastAPI(title="사주피티 version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "사주팔자 전문가 AI 역술가입니다.", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/analysis")
async def get_analysis(request: Request):
    try:
        # 요청 데이터 파싱
        birth_data_json = await request.json()
        
        # 필수 필드 검증
        required_fields = ['year', 'month', 'day', 'hour', 'minute']
        for field in required_fields:
            if field not in birth_data_json:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # 데이터 타입 검증
        try:
            year = int(birth_data_json.get('year'))
            month = int(birth_data_json.get('month'))
            day = int(birth_data_json.get('day'))
            hour = int(birth_data_json.get('hour'))
            minute = int(birth_data_json.get('minute'))
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid data types. All fields must be integers.")
        
        # 날짜 유효성 검증
        if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23 and 0 <= minute <= 59):
            raise HTTPException(status_code=400, detail="Invalid date/time values")
        
        # 사주 분석 실행
        analysis_result = get_saju_details(year, month, day, hour, minute)
        
        # 분석 결과 검증
        if not analysis_result or "error" in analysis_result:
            raise HTTPException(status_code=500, detail="Analysis failed")
        
        return {
            "status": "success",
            "request_data": birth_data_json,
            "analysis_result": analysis_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # 로그 출력
        print(f"Error in analysis endpoint: {str(e)}")
        traceback.print_exc()
        
        # 클라이언트에게 일반적인 오류 메시지 반환
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
            }
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
