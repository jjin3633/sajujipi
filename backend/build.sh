#!/bin/bash
set -e

# 환경 변수 설정
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
export MATURIN_PEP517_ARGS="--no-build-isolation"
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

echo "📦 Python 3.13 호환 패키지 설치 중..."

# pip 업그레이드
pip install --upgrade pip

# 개별 패키지 설치 (Python 3.13 호환 버전)
echo "Installing fastapi==0.104.1..."
pip install --no-cache-dir fastapi==0.104.1

echo "Installing uvicorn==0.24.0..."
pip install --no-cache-dir uvicorn==0.24.0

echo "Installing gunicorn==21.2.0..."
pip install --no-cache-dir gunicorn==21.2.0

echo "Installing requests==2.31.0..."
pip install --no-cache-dir requests==2.31.0

echo "Installing python-multipart==0.0.6..."
pip install --no-cache-dir python-multipart==0.0.6

echo "Installing pydantic==2.5.0..."
pip install --no-cache-dir pydantic==2.5.0

echo "Installing typing-extensions==4.8.0..."
pip install --no-cache-dir typing-extensions==4.8.0

echo "✅ 빌드 완료!" 