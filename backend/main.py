    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from logic.analyzer import get_saju_details

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class BirthData(BaseModel):
        year: int
        month: int
        day: int
        hour: int
        minute: int

    @app.get("/")
    def read_root():
        return {"message": "사주팔자 전문가 AI 역술가입니다."}

    @app.post("/analysis")
    def get_analysis(birth_data: BirthData):
        analysis_result = get_saju_details(
            birth_data.year,
            birth_data.month,
            birth_data.day,
            birth_data.hour,
            birth_data.minute
        )
        return {
            "request_data": birth_data.dict(),
            "analysis_result": analysis_result
        }

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)