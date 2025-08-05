#!/usr/bin/env python3
"""
프론트엔드 자산을 통합하는 스크립트
CSS와 JS 파일을 하나로 합쳐서 로컬 테스트를 쉽게 만듭니다.
"""

import os
import re

def consolidate_css():
    """CSS 파일들을 하나로 통합"""
    css_dir = "frontend/css"
    output_file = "frontend/styles.css"
    
    # CSS 파일 순서 (의존성 순서대로)
    css_files = [
        "base.css",
        "layout.css", 
        "components.css",
        "analysis.css",
        "responsive.css",
        "main.css"
    ]
    
    consolidated_css = "/* 통합된 CSS 파일 - 자동 생성됨 */\n\n"
    
    for css_file in css_files:
        file_path = os.path.join(css_dir, css_file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # @import 구문 제거 (이미 통합되므로)
                content = re.sub(r'@import\s+["\'].*?["\'];?\s*\n?', '', content)
                
                # 폰트 import는 유지
                if '@import url' in content and 'fonts.googleapis.com' in content:
                    font_imports = re.findall(r'@import url\(["\'].*?fonts\.googleapis\.com.*?["\']\);', content)
                    for font_import in font_imports:
                        consolidated_css = font_import + '\n' + consolidated_css
                        content = content.replace(font_import, '')
                
                consolidated_css += f"\n/* ========== {css_file} ========== */\n"
                consolidated_css += content.strip() + "\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(consolidated_css)
    
    print(f"CSS 파일 통합 완료: {output_file}")

def consolidate_js():
    """JavaScript 파일들을 하나로 통합 (ES6 모듈을 일반 스크립트로 변환)"""
    js_dir = "frontend/js"
    output_file = "frontend/script.js"
    
    # 통합할 JS 파일들과 순서
    js_files = [
        ("config.js", None),
        ("utils.js", None),
        ("api.js", None),
        ("form-validator.js", None),
        ("display/base-display.js", None),
        ("display/ilju-display.js", None),
        ("display/sipsung-display.js", None),
        ("display/sibiunseong-display.js", None),
        ("display/career-display.js", None),
        ("display/love-display.js", None),
        ("display/wealth-display.js", None),
        ("display/health-display.js", None),
        ("display/daeun-display.js", None),
        ("display/comprehensive-display.js", None),
        ("display/index.js", None),
        ("main.js", None)
    ]
    
    consolidated_js = """/* 통합된 JavaScript 파일 - 자동 생성됨 */
'use strict';

// 전역 네임스페이스
window.SajuApp = window.SajuApp || {};

"""
    
    # 각 파일의 내용을 읽고 변환
    for js_file, _ in js_files:
        file_path = os.path.join(js_dir, js_file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # import/export 구문 제거 및 변환
                content = re.sub(r'import\s+{[^}]+}\s+from\s+["\'].*?["\'];?\s*\n?', '', content)
                content = re.sub(r'import\s+.*?\s+from\s+["\'].*?["\'];?\s*\n?', '', content)
                content = re.sub(r'export\s+class\s+', 'window.SajuApp.', content)
                content = re.sub(r'export\s+const\s+', 'window.SajuApp.', content)
                content = re.sub(r'export\s+{[^}]+};?\s*\n?', '', content)
                
                consolidated_js += f"\n/* ========== {js_file} ========== */\n"
                consolidated_js += content.strip() + "\n"
    
    # 클래스 참조 수정
    consolidated_js = consolidated_js.replace('new Utils()', 'new window.SajuApp.Utils()')
    consolidated_js = consolidated_js.replace('Utils.', 'window.SajuApp.Utils.')
    consolidated_js = consolidated_js.replace('SajuAPI.', 'window.SajuApp.SajuAPI.')
    consolidated_js = consolidated_js.replace('new BaseDisplay', 'new window.SajuApp.BaseDisplay')
    consolidated_js = consolidated_js.replace('new IljuDisplay', 'new window.SajuApp.IljuDisplay')
    consolidated_js = consolidated_js.replace('new SipsungDisplay', 'new window.SajuApp.SipsungDisplay')
    consolidated_js = consolidated_js.replace('new SibiunseongDisplay', 'new window.SajuApp.SibiunseongDisplay')
    consolidated_js = consolidated_js.replace('new CareerDisplay', 'new window.SajuApp.CareerDisplay')
    consolidated_js = consolidated_js.replace('new LoveDisplay', 'new window.SajuApp.LoveDisplay')
    consolidated_js = consolidated_js.replace('new WealthDisplay', 'new window.SajuApp.WealthDisplay')
    consolidated_js = consolidated_js.replace('new HealthDisplay', 'new window.SajuApp.HealthDisplay')
    consolidated_js = consolidated_js.replace('new DaeunDisplay', 'new window.SajuApp.DaeunDisplay')
    consolidated_js = consolidated_js.replace('new ComprehensiveDisplay', 'new window.SajuApp.ComprehensiveDisplay')
    consolidated_js = consolidated_js.replace('new FormValidator', 'new window.SajuApp.FormValidator')
    consolidated_js = consolidated_js.replace('new DisplayManager', 'new window.SajuApp.DisplayManager')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(consolidated_js)
    
    print(f"JavaScript 파일 통합 완료: {output_file}")

def update_html_for_consolidated():
    """HTML 파일을 통합된 파일을 사용하도록 업데이트"""
    html_file = "frontend/index.html"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSS 링크 변경
    content = re.sub(r'<link\s+rel="stylesheet"\s+href="css/main\.css">', 
                     '<link rel="stylesheet" href="styles.css">', content)
    
    # JS 스크립트 변경  
    content = re.sub(r'<script\s+type="module"\s+src="js/main\.js"></script>',
                     '<script src="script.js"></script>', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"HTML 파일 업데이트 완료: {html_file}")

if __name__ == "__main__":
    print("프론트엔드 자산 통합 시작...")
    consolidate_css()
    consolidate_js()
    update_html_for_consolidated()
    print("\n통합 완료! 이제 index.html을 브라우저에서 직접 열어도 작동합니다.")