// 메인 애플리케이션
import { Utils } from './utils.js';
import { SajuAPI } from './api.js';
import { DisplayManager } from './display/index.js';
import { FormValidator } from './form-validator.js';

class SajuApp {
    constructor() {
        this.displayManager = new DisplayManager();
        this.validator = new FormValidator();
        this.init();
    }
    
    init() {
        // 분석 버튼 이벤트 리스너
        const analyzeBtn = Utils.getElement('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.analyze());
        }
        
        // 엔터키 이벤트
        document.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.target.matches('input')) {
                this.analyze();
            }
        });
        
        // 초기 로드 시 API 상태 체크
        this.checkAPIStatus();
    }
    
    async checkAPIStatus() {
        const isHealthy = await SajuAPI.checkHealth();
        if (!isHealthy) {
            console.warn('API 서버가 응답하지 않습니다.');
        }
    }
    
    async analyze() {
        // 입력값 가져오기
        const birthData = {
            year: Utils.getElement('year')?.value,
            month: Utils.getElement('month')?.value,
            day: Utils.getElement('day')?.value,
            hour: Utils.getElement('hour')?.value,
            minute: Utils.getElement('minute')?.value
        };
        
        // 유효성 검사
        const validation = this.validator.validate(birthData);
        if (!validation.isValid) {
            alert(validation.message);
            return;
        }
        
        // 상태 표시
        const statusDiv = Utils.getElement('status');
        Utils.showLoading(statusDiv);
        
        // 이전 결과 초기화
        this.displayManager.clearAll();
        
        try {
            // API 호출
            const result = await SajuAPI.analyze(birthData);
            
            // 결과 표시
            statusDiv.innerHTML = '';
            this.displayManager.displayAll(result);
            
            // 첫 번째 섹션으로 스크롤
            setTimeout(() => {
                Utils.scrollToElement('ilju-analysis');
            }, 300);
            
        } catch (error) {
            Utils.showError(statusDiv, error);
            this.displayManager.hideAll();
        }
    }
}

// 앱 시작
document.addEventListener('DOMContentLoaded', () => {
    window.sajuApp = new SajuApp();
});