#!/bin/bash

# 배포 전 빌드 스크립트
echo "🚀 배포 빌드 시작..."

# 환경 변수 설정
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1

# Python 버전 확인
python --version

# pip 업그레이드
pip install --upgrade pip

# 의존성 설치 (Rust 의존성 방지)
pip install --no-cache-dir --no-build-isolation -r requirements.txt

# 빌드 완료 확인
echo "✅ 빌드 완료!" 