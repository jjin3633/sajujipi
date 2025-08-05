#!/bin/bash
set -e

# 환경 변수 설정
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
export MATURIN_PEP517_ARGS="--no-build-isolation"
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

echo "📦 Flask 기반 안전한 패키지 설치 중..."

# pip 업그레이드
pip install --upgrade pip

# 개별 패키지 설치 (Flask 기반)
echo "Installing flask==2.3.3..."
pip install --no-cache-dir flask==2.3.3

echo "Installing flask-cors==4.0.0..."
pip install --no-cache-dir flask-cors==4.0.0

echo "Installing gunicorn==21.2.0..."
pip install --no-cache-dir gunicorn==21.2.0

echo "Installing requests==2.31.0..."
pip install --no-cache-dir requests==2.31.0

echo "Installing python-multipart==0.0.6..."
pip install --no-cache-dir python-multipart==0.0.6

echo "✅ 빌드 완료!" 