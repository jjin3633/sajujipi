#!/bin/bash

# 배포 전 빌드 스크립트
echo "🚀 배포 빌드 시작..."

# 환경 변수 설정
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
export MATURIN_PEP517_ARGS="--no-build-isolation"

# Python 버전 확인
python --version

# pip 업그레이드
pip install --upgrade pip

# Rust 의존성 방지를 위한 환경 변수
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

# 의존성 설치 (Rust 의존성 완전 방지)
pip install --no-cache-dir --no-build-isolation --no-deps -r requirements.txt

# 개별 패키지 설치 (Rust 의존성 제외)
pip install --no-cache-dir fastapi==0.98.0
pip install --no-cache-dir uvicorn[standard]==0.23.2
pip install --no-cache-dir gunicorn==21.2.0
pip install --no-cache-dir requests==2.31.0
pip install --no-cache-dir python-multipart==0.0.6
pip install --no-cache-dir pydantic==1.10.13
pip install --no-cache-dir typing-extensions==4.8.0

# 빌드 완료 확인
echo "✅ 빌드 완료!" 