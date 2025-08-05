from flask import Flask, request, jsonify
from flask_cors import CORS
from logic.analyzer import get_saju_details
import traceback
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def read_root():
    return {"message": "사주팔자 전문가 AI 역술가입니다.", "status": "running"}

@app.route("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.route("/analysis", methods=["POST"])
def get_analysis():
    try:
        # 요청 데이터 파싱
        birth_data_json = request.get_json()
        
        if not birth_data_json:
            print("오류: JSON 데이터가 없습니다.")
            return jsonify({"status": "error", "message": "Invalid JSON data"}), 400
        
        print(f"받은 데이터: {birth_data_json}")
        
        # 필수 필드 검증
        required_fields = ['year', 'month', 'day', 'hour', 'minute']
        for field in required_fields:
            if field not in birth_data_json:
                print(f"오류: 필수 필드 누락: {field}")
                return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
        
        # 데이터 타입 검증
        try:
            year = int(birth_data_json.get('year'))
            month = int(birth_data_json.get('month'))
            day = int(birth_data_json.get('day'))
            hour = int(birth_data_json.get('hour'))
            minute = int(birth_data_json.get('minute'))
        except (ValueError, TypeError) as e:
            print(f"오류: 데이터 타입 변환 실패: {e}")
            return jsonify({"status": "error", "message": "Invalid data types. All fields must be integers."}), 400
        
        # 날짜 유효성 검증
        if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23 and 0 <= minute <= 59):
            print(f"오류: 유효하지 않은 날짜/시간: {year}-{month}-{day} {hour}:{minute}")
            return jsonify({"status": "error", "message": "Invalid date/time values"}), 400
        
        print(f"분석 시작: {year}-{month}-{day} {hour}:{minute}")
        
        # 사주 분석 실행
        analysis_result = get_saju_details(year, month, day, hour, minute)
        
        print(f"분석 결과: {analysis_result}")
        
        # 분석 결과 검증
        if not analysis_result or "error" in analysis_result:
            print(f"오류: 분석 실패 - {analysis_result}")
            return jsonify({"status": "error", "message": "Analysis failed"}), 500
        
        return jsonify({
            "status": "success",
            "request_data": birth_data_json,
            "analysis_result": analysis_result
        })
        
    except Exception as e:
        # 로그 출력
        print(f"분석 엔드포인트 오류: {str(e)}")
        traceback.print_exc()
        
        # 클라이언트에게 일반적인 오류 메시지 반환
        return jsonify({
            "status": "error",
            "message": "분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
