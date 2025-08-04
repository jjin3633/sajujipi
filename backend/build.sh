#!/bin/bash

# Render 배포용 빌드 스크립트
# Rust 컴파일 문제 해결을 위한 환경 변수 설정

export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
export MATURIN_PEP517_ARGS="--no-build-isolation"
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

echo "🚀 빌드 시작..."

# pip 업그레이드
pip install --upgrade pip

# 기본 패키지 설치 (캐시 없이)
pip install --no-cache-dir --no-build-isolation --no-deps -r requirements.txt

# 개별 패키지 설치 (Rust 컴파일 방지)
pip install --no-cache-dir fastapi==0.95.2
pip install --no-cache-dir uvicorn[standard]==0.22.0
pip install --no-cache-dir gunicorn==20.1.0
pip install --no-cache-dir requests==2.31.0
pip install --no-cache-dir python-multipart==0.0.6
pip install --no-cache-dir pydantic==1.9.2
pip install --no-cache-dir typing-extensions==4.5.0

echo "✅ 빌드 완료!" 