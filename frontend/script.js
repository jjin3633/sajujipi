/* 통합된 JavaScript 파일 - 자동 생성됨 */
'use strict';

// 전역 네임스페이스
window.SajuApp = window.SajuApp || {};


/* ========== config.js ========== */
// 전역 설정
window.SajuApp.CONFIG = {
    API_URL: 'https://sajujipi-backend.onrender.com/analysis',
    LOADING_MESSAGE: '분석 중입니다... 잠시만 기다려주세요.',
    ERROR_MESSAGE: '분석 중 오류가 발생했습니다.',
    PLACEHOLDER_IMAGE: 'https://via.placeholder.com/400x300'
};

/* ========== utils.js ========== */
// 유틸리티 함수들
window.SajuApp.Utils = {
    // 안전한 DOM 요소 가져오기
    getElement: (id) => {
        const element = document.getElementById(id);
        if (!element) {
            console.error(`Element ${id} not found`);
        }
        return element;
    },
    
    // HTML 생성 헬퍼
    createHTML: (tag, content, className = '') => {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (typeof content === 'string') {
            element.innerHTML = content;
        } else if (content) {
            element.appendChild(content);
        }
        return element;
    },
    
    // 안전한 데이터 접근
    safeGet: (obj, path, defaultValue = '') => {
        return path.split('.').reduce((current, key) => {
            return current && current[key] !== undefined ? current[key] : defaultValue;
        }, obj);
    },
    
    // 날짜 포맷팅
    formatDate: (year, month, day, hour, minute) => {
        return `${year}년 ${month}월 ${day}일 ${hour}시 ${minute}분`;
    },
    
    // 로딩 표시
    showLoading: (element) => {
        if (!element) return;
        element.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>분석 중입니다... 잠시만 기다려주세요.</p>
            </div>
        `;
    },
    
    // 에러 표시
    showError: (element, error) => {
        if (!element) return;
        element.innerHTML = `
            <div class="error-message">
                <p>❌ ${error.message || '분석 중 오류가 발생했습니다.'}</p>
                <p class="error-detail">${error.detail || '잠시 후 다시 시도해주세요.'}</p>
            </div>
        `;
    },
    
    // 섹션 표시/숨기기
    toggleSection: (sectionId, show = true) => {
        const section = window.SajuApp.Utils.getElement(sectionId);
        if (section) {
            section.style.display = show ? 'block' : 'none';
        }
    },
    
    // 스크롤 애니메이션
    scrollToElement: (elementId, offset = 100) => {
        const element = window.SajuApp.Utils.getElement(elementId);
        if (element) {
            const y = element.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top: y, behavior: 'smooth' });
        }
    }
};

/* ========== api.js ========== */
// API 통신 모듈
window.SajuApp.SajuAPI = class {
    static async analyze(birthData) {
        try {
            const response = await fetch(CONFIG.API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    year: parseInt(birthData.year),
                    month: parseInt(birthData.month),
                    day: parseInt(birthData.day),
                    hour: parseInt(birthData.hour),
                    minute: parseInt(birthData.minute)
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.message || '분석 실패');
            }

            return data.analysis_result || data.result;
            
        } catch (error) {
            console.error('API 호출 오류:', error);
            throw {
                message: '서버 연결 오류',
                detail: error.message
            };
        }
    }
    
    static async checkHealth() {
        try {
            const response = await fetch(CONFIG.API_URL.replace('/analysis', '/health'));
            return response.ok;
        } catch {
            return false;
        }
    }
}

/* ========== form-validator.js ========== */
// 폼 유효성 검사 모듈
window.SajuApp.FormValidator = class {
    validate(birthData) {
        // 모든 필드가 입력되었는지 확인
        if (!birthData.year || !birthData.month || !birthData.day || !birthData.hour || !birthData.minute) {
            return {
                isValid: false,
                message: '모든 생년월일 정보를 입력해주세요.'
            };
        }
        
        // 숫자 형식 검사
        const year = parseInt(birthData.year);
        const month = parseInt(birthData.month);
        const day = parseInt(birthData.day);
        const hour = parseInt(birthData.hour);
        const minute = parseInt(birthData.minute);
        
        if (isNaN(year) || isNaN(month) || isNaN(day) || isNaN(hour) || isNaN(minute)) {
            return {
                isValid: false,
                message: '올바른 숫자 형식으로 입력해주세요.'
            };
        }
        
        // 연도 범위 검사 (1900년 ~ 현재 연도)
        const currentYear = new Date().getFullYear();
        if (year < 1900 || year > currentYear) {
            return {
                isValid: false,
                message: `연도는 1900년부터 ${currentYear}년 사이로 입력해주세요.`
            };
        }
        
        // 월 범위 검사
        if (month < 1 || month > 12) {
            return {
                isValid: false,
                message: '월은 1부터 12 사이로 입력해주세요.'
            };
        }
        
        // 일 범위 검사
        const maxDays = this.getDaysInMonth(year, month);
        if (day < 1 || day > maxDays) {
            return {
                isValid: false,
                message: `${month}월은 1일부터 ${maxDays}일까지입니다.`
            };
        }
        
        // 시간 범위 검사
        if (hour < 0 || hour > 23) {
            return {
                isValid: false,
                message: '시간은 0부터 23 사이로 입력해주세요.'
            };
        }
        
        // 분 범위 검사
        if (minute < 0 || minute > 59) {
            return {
                isValid: false,
                message: '분은 0부터 59 사이로 입력해주세요.'
            };
        }
        
        return { isValid: true };
    }
    
    getDaysInMonth(year, month) {
        return new Date(year, month, 0).getDate();
    }
}

/* ========== display/base-display.js ========== */
// 기본 디스플레이 클래스
window.SajuApp.BaseDisplay = class {
    constructor(sectionId) {
        this.section = window.SajuApp.Utils.getElement(sectionId);
    }
    
    clear() {
        if (this.section) {
            this.section.innerHTML = '';
        }
    }
    
    show() {
        window.SajuApp.Utils.toggleSection(this.section?.id, true);
    }
    
    hide() {
        window.SajuApp.Utils.toggleSection(this.section?.id, false);
    }
    
    createCard(title, content, className = '') {
        return window.SajuApp.Utils.createHTML('div', `
            <div class="card ${className}">
                <h3 class="card-title">${title}</h3>
                <div class="card-content">${content}</div>
            </div>
        `);
    }
    
    createImageCard(title, content, imageUrl) {
        return window.SajuApp.Utils.createHTML('div', `
            <div class="card image-card">
                <h3 class="card-title">${title}</h3>
                ${imageUrl ? `<img src="${imageUrl}" alt="${title}" class="card-image">` : ''}
                <div class="card-content">${content}</div>
            </div>
        `);
    }
    
    formatContent(content) {
        if (!content) return '';
        
        // 줄바꿈 처리
        return content
            .replace(/【([^】]+)】/g, '<h4 class="section-title">$1</h4>')
            .replace(/▣\s*(.+)/g, '<h5 class="subsection-title">▣ $1</h5>')
            .replace(/•\s*(.+)/g, '<li>$1</li>')
            .replace(/(\n|^)(\d+)\.\s*(.+)/g, '$1<div class="numbered-item"><span class="number">$2.</span>$3</div>')
            .replace(/\n/g, '<br>');
    }
}

/* ========== display/ilju-display.js ========== */
// 일주 분석 디스플레이
window.SajuApp.IljuDisplay = class extends BaseDisplay {
    constructor() {
        super('ilju-analysis');
    }
    
    display(data) {
        this.clear();
        
        const iljuData = window.SajuApp.Utils.safeGet(data, 'comprehensive_report.ilju_analysis', null);
        
        if (!iljuData) {
            this.section.innerHTML = '<p class="no-data">일주 분석 데이터가 없습니다.</p>';
            return;
        }
        
        const content = this.formatContent(iljuData.content || '');
        const card = this.createImageCard(
            iljuData.title || '일주 분석',
            content,
            iljuData.illustration_url
        );
        
        this.section.appendChild(card);
        this.show();
    }
}

/* ========== display/sipsung-display.js ========== */
// 십성 분석 디스플레이
window.SajuApp.SipsungDisplay = class extends BaseDisplay {
    constructor() {
        super('sipsung-analysis');
    }
    
    renderContent(data) {
        const sipsung = data.sipsung_analysis || {};
        return `
            ${this.createSection('십성 분석', sipsung.title || '십성 분석')}
            ${sipsung.content ? this.formatContent(sipsung.content) : ''}
            ${sipsung.comprehensive ? this.createSubSection('종합 분석', sipsung.comprehensive) : ''}
        `;
    }
}

/* ========== display/sibiunseong-display.js ========== */
// 십이운성 분석 디스플레이
window.SajuApp.SibiunseongDisplay = class extends BaseDisplay {
    constructor() {
        super('sibiunseong-analysis');
    }
    
    renderContent(data) {
        const sibiunseong = data.sibiunseong_analysis || {};
        return `
            ${this.createSection('십이운성 분석', sibiunseong.title || '십이운성 분석')}
            ${sibiunseong.content ? this.formatContent(sibiunseong.content) : ''}
            ${sibiunseong.comprehensive ? this.createSubSection('종합 분석', sibiunseong.comprehensive) : ''}
            ${sibiunseong.illustration_url ? this.createImage(sibiunseong.illustration_url, '십이운성 일러스트') : ''}
        `;
    }
}

/* ========== display/career-display.js ========== */
// 직업운 분석 디스플레이
window.SajuApp.CareerDisplay = class extends BaseDisplay {
    constructor() {
        super('career-analysis');
    }
    
    renderContent(data) {
        const career = data.career_luck_analysis || {};
        return `
            ${this.createSection('직업운 분석', career.title || '직업운 분석')}
            ${career.description ? this.createSubSection('설명', career.description) : ''}
            ${career.suitable_jobs ? this.createListSection('적합한 직업', career.suitable_jobs) : ''}
            ${career.business_vs_job ? this.createSubSection('사업 vs 직장', career.business_vs_job) : ''}
            ${career.advice ? this.createSubSection('조언', career.advice) : ''}
            ${career.caution_people ? this.createSubSection('주의할 사람', career.caution_people) : ''}
            ${career.avatar_url ? this.createImage(career.avatar_url, '직업 아바타') : ''}
        `;
    }
    
    createListSection(title, items) {
        if (!items || items.length === 0) return '';
        return `
            <div class="sub-section">
                <h4>${title}</h4>
                <ul class="job-list">
                    ${items.map(job => `<li>${job}</li>`).join('')}
                </ul>
            </div>
        `;
    }
}

/* ========== display/love-display.js ========== */
// 연애운 & 결혼운 분석 디스플레이
window.SajuApp.LoveDisplay = class extends BaseDisplay {
    constructor() {
        super('love-analysis');
    }
    
    renderContent(data) {
        const love = data.love_and_marriage_analysis || {};
        return `
            ${this.createSection('연애운 & 결혼운 분석', love.title || '연애운 & 결혼운 분석')}
            ${love.description ? this.createSubSection('설명', love.description) : ''}
            ${love.overall_tendency ? this.createSubSection('전체적 경향', love.overall_tendency) : ''}
            ${love.ideal_partner ? this.createSubSection('인연 상대', love.ideal_partner) : ''}
            ${love.improvement_points ? this.createSubSection('개선점', love.improvement_points) : ''}
            ${love.flow_analysis ? this.createSubSection('흐름 분석', love.flow_analysis) : ''}
            ${love.timing_location ? this.createSubSection('시기/장소', love.timing_location) : ''}
            ${love.portrait_url ? this.createImage(love.portrait_url, '인연 상대 초상화') : ''}
        `;
    }
}

/* ========== display/wealth-display.js ========== */
// 재물운 분석 디스플레이
window.SajuApp.WealthDisplay = class extends BaseDisplay {
    constructor() {
        super('wealth-analysis');
    }
    
    renderContent(data) {
        const wealth = data.wealth_luck_analysis || {};
        return `
            ${this.createSection('재물운 분석', wealth.title || '재물운 분석')}
            ${wealth.description ? this.createSubSection('설명', wealth.description) : ''}
            ${wealth.overall_flow ? this.createSubSection('전체 흐름', wealth.overall_flow) : ''}
            ${wealth.wealth_characteristics ? this.createSubSection('재물운 특징', wealth.wealth_characteristics) : ''}
            ${wealth.people_analysis ? this.createSubSection('사람 분석', wealth.people_analysis) : ''}
            ${wealth.business_investment_advice ? this.createSubSection('사업/투자 조언', wealth.business_investment_advice) : ''}
        `;
    }
}

/* ========== display/health-display.js ========== */
// 건강운 분석 디스플레이
window.SajuApp.HealthDisplay = class extends BaseDisplay {
    constructor() {
        super('health-analysis');
    }
    
    renderContent(data) {
        const health = data.health_luck_analysis || {};
        return `
            ${this.createSection('건강운 분석', health.title || '건강운 분석')}
            ${health.description ? this.createSubSection('설명', health.description) : ''}
            ${health.body_constitution ? this.createSubSection('체질', health.body_constitution) : ''}
            ${health.vulnerable_areas ? this.createSubSection('위험 부위', health.vulnerable_areas) : ''}
            ${health.suitable_exercise ? this.createSubSection('적합한 운동', health.suitable_exercise) : ''}
            ${health.period_analysis ? this.createSubSection('시기별 분석', health.period_analysis) : ''}
            ${health.management_advice ? this.createSubSection('관리 조언', health.management_advice) : ''}
        `;
    }
}

/* ========== display/daeun-display.js ========== */
// 대운 분석 디스플레이
window.SajuApp.DaeunDisplay = class extends BaseDisplay {
    constructor() {
        super('daeun-analysis');
    }
    
    renderContent(data) {
        const daeun = data.daeun_analysis || {};
        return `
            ${this.createSection('대운 분석', daeun.title || '대운 분석')}
            ${daeun.content ? this.formatContent(daeun.content) : ''}
            ${this.renderDaeunPeriods(daeun.daeun_periods)}
            ${this.renderSeunPeriods(daeun.seun_periods)}
            ${this.renderChangePoints(daeun.change_points)}
            ${daeun.future_outlook ? this.createSubSection('미래 전망', daeun.future_outlook) : ''}
        `;
    }
    
    renderDaeunPeriods(periods) {
        if (!periods || periods.length === 0) return '';
        return `
            <div class="sub-section">
                <h4>90년 대운</h4>
                <div class="daeun-grid">
                    ${periods.map(period => `
                        <div class="daeun-item ${period.status}">
                            <h5>${period.title}</h5>
                            <p>${period.description}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    renderSeunPeriods(periods) {
        if (!periods || periods.length === 0) return '';
        return `
            <div class="sub-section">
                <h4>5년 세운</h4>
                <div class="seun-grid">
                    ${periods.map(period => `
                        <div class="seun-item ${period.status}">
                            <h5>${period.year}년</h5>
                            <p>${period.description}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    renderChangePoints(points) {
        if (!points || points.length === 0) return '';
        return `
            <div class="sub-section">
                <h4>곧 맞딱뜨릴 삼재</h4>
                ${points.map(point => `
                    <div class="change-point">
                        <h5>${point.title}</h5>
                        <p>${point.description}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

/* ========== display/comprehensive-display.js ========== */
// 종합 리포트 디스플레이
window.SajuApp.ComprehensiveDisplay = class extends BaseDisplay {
    constructor() {
        super('comprehensive-report');
    }
    
    renderContent(data) {
        const report = data.comprehensive_report || {};
        return `
            ${this.createSection('종합 리포트', '종합 리포트')}
            ${report.final_summary ? this.renderFinalSummary(report.final_summary) : ''}
            ${report.sibisinsal_analysis ? this.renderSibisinsal(report.sibisinsal_analysis) : ''}
            ${report.guin_analysis ? this.renderGuin(report.guin_analysis) : ''}
            ${report.career_analysis ? this.renderCareerSummary(report.career_analysis) : ''}
            ${report.daeun_analysis ? this.renderDaeunSummary(report.daeun_analysis) : ''}
        `;
    }
    
    renderFinalSummary(summary) {
        if (!summary || !summary.content) return '';
        return `
            <div class="final-summary">
                ${this.formatContent(summary.content)}
            </div>
        `;
    }
    
    renderSibisinsal(analysis) {
        if (!analysis) return '';
        return `
            <div class="sub-section">
                <h3>${analysis.title || '십이신살 분석'}</h3>
                ${this.formatContent(analysis.content || '')}
                ${this.renderPeriods(analysis.periods)}
            </div>
        `;
    }
    
    renderGuin(analysis) {
        if (!analysis) return '';
        return `
            <div class="sub-section">
                <h3>${analysis.title || '귀인 분석'}</h3>
                ${this.formatContent(analysis.content || '')}
                ${this.renderPeriods(analysis.periods)}
                ${analysis.overall ? this.createSubSection('종합 분석', analysis.overall) : ''}
            </div>
        `;
    }
    
    renderCareerSummary(analysis) {
        if (!analysis) return '';
        return `
            <div class="sub-section">
                <h3>${analysis.title || '직업운 분석'}</h3>
                ${this.formatContent(analysis.content || '')}
            </div>
        `;
    }
    
    renderDaeunSummary(analysis) {
        if (!analysis) return '';
        return `
            <div class="sub-section">
                <h3>${analysis.title || '대운 분석'}</h3>
                ${this.formatContent(analysis.content || '')}
            </div>
        `;
    }
    
    renderPeriods(periods) {
        if (!periods || periods.length === 0) return '';
        return `
            <div class="period-list">
                ${periods.map(period => `
                    <div class="period-item">
                        <h5>${period.title}</h5>
                        <p>${period.description}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

/* ========== display/index.js ========== */
// 디스플레이 모듈 통합
window.SajuApp.DisplayManager = class {
    constructor() {
        this.displays = {
            ilju: new window.SajuApp.IljuDisplay(),
            sipsung: new window.SajuApp.SipsungDisplay(),
            sibiunseong: new window.SajuApp.SibiunseongDisplay(),
            career: new window.SajuApp.CareerDisplay(),
            love: new window.SajuApp.LoveDisplay(),
            wealth: new window.SajuApp.WealthDisplay(),
            health: new window.SajuApp.HealthDisplay(),
            daeun: new window.SajuApp.DaeunDisplay(),
            comprehensive: new window.SajuApp.ComprehensiveDisplay()
        };
    }
    
    displayAll(data) {
        // 모든 섹션 표시
        Object.values(this.displays).forEach(display => {
            display.display(data);
        });
    }
    
    clearAll() {
        // 모든 섹션 초기화
        Object.values(this.displays).forEach(display => {
            display.clear();
        });
    }
    
    hideAll() {
        // 모든 섹션 숨기기
        Object.values(this.displays).forEach(display => {
            display.hide();
        });
    }
}

/* ========== main.js ========== */
// 메인 애플리케이션
class SajuApp {
    constructor() {
        this.displayManager = new window.SajuApp.DisplayManager();
        this.validator = new window.SajuApp.FormValidator();
        this.init();
    }
    
    init() {
        // 분석 버튼 이벤트 리스너
        const analyzeBtn = window.SajuApp.Utils.getElement('analyze-btn');
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
        const isHealthy = await window.SajuApp.SajuAPI.checkHealth();
        if (!isHealthy) {
            console.warn('API 서버가 응답하지 않습니다.');
        }
    }
    
    async analyze() {
        // 입력값 가져오기
        const birthData = {
            year: window.SajuApp.Utils.getElement('year')?.value,
            month: window.SajuApp.Utils.getElement('month')?.value,
            day: window.SajuApp.Utils.getElement('day')?.value,
            hour: window.SajuApp.Utils.getElement('hour')?.value,
            minute: window.SajuApp.Utils.getElement('minute')?.value
        };
        
        // 유효성 검사
        const validation = this.validator.validate(birthData);
        if (!validation.isValid) {
            alert(validation.message);
            return;
        }
        
        // 상태 표시
        const statusDiv = window.SajuApp.Utils.getElement('status');
        window.SajuApp.Utils.showLoading(statusDiv);
        
        // 이전 결과 초기화
        this.displayManager.clearAll();
        
        try {
            // API 호출
            const result = await window.SajuApp.SajuAPI.analyze(birthData);
            
            // 결과 표시
            statusDiv.innerHTML = '';
            this.displayManager.displayAll(result);
            
            // 첫 번째 섹션으로 스크롤
            setTimeout(() => {
                window.SajuApp.Utils.scrollToElement('ilju-analysis');
            }, 300);
            
        } catch (error) {
            window.SajuApp.Utils.showError(statusDiv, error);
            this.displayManager.hideAll();
        }
    }
}

// 앱 시작
document.addEventListener('DOMContentLoaded', () => {
    window.sajuApp = new SajuApp();
});
