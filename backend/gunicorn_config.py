import os

# Gunicorn 설정
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 2  # Free tier에서는 workers를 적게 설정
timeout = 120  # 타임아웃을 120초로 증가
keepalive = 5
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
accesslog = '-'
errorlog = '-'
loglevel = 'info'