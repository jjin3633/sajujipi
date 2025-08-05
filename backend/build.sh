#!/bin/bash
set -e

# Python 버전 강제 설정
echo "🔧 Python 버전 설정 중..."
export PYTHON_VERSION=3.9.18

# 환경 변수 설정
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
export MATURIN_PEP517_ARGS="--no-build-isolation"
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

echo "📦 Python 3.9.18 호환 패키지 설치 중..."

# pip 업그레이드
pip install --upgrade pip

# 개별 패키지 설치 (Python 3.9.18 호환 버전)
echo "Installing fastapi==0.68.2..."
pip install --no-cache-dir fastapi==0.68.2

echo "Installing uvicorn[standard]==0.15.0..."
pip install --no-cache-dir uvicorn[standard]==0.15.0

echo "Installing gunicorn==20.1.0..."
pip install --no-cache-dir gunicorn==20.1.0

echo "Installing requests==2.28.2..."
pip install --no-cache-dir requests==2.28.2

echo "Installing python-multipart==0.0.6..."
pip install --no-cache-dir python-multipart==0.0.6

echo "Installing pydantic==1.8.2..."
pip install --no-cache-dir pydantic==1.8.2

echo "Installing typing-extensions==3.10.0.2..."
pip install --no-cache-dir typing-extensions==3.10.0.2

echo "✅ 빌드 완료!" 