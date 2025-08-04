# 사주지피 백엔드 API

사주팔자 AI 분석을 위한 FastAPI 백엔드 서버입니다.

## 기능

- 사주팔자 계산 및 분석
- 일주, 십성, 십이운성 분석
- AI 이미지 생성 (배포 환경에서는 비활성화)
- RESTful API 제공

## 배포 환경 설정

### Render 배포

1. **환경 변수 설정**
   - `PORT`: 서버 포트 (자동 설정됨)

2. **빌드 명령어**
   ```bash
   pip install -r requirements.txt
   ```

3. **실행 명령어**
   ```bash
   gunicorn main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
   ```

## API 엔드포인트

- `GET /`: 서버 상태 확인
- `GET /health`: 헬스 체크
- `POST /analysis`: 사주 분석 요청

## 로컬 개발

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```

## 주의사항

- AI 이미지 생성 기능은 배포 환경에서 안정성을 위해 비활성화되어 있습니다.
- 실제 운영 시에는 AI API 키를 환경 변수로 설정해야 합니다. 