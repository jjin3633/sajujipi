/* 통합된 JavaScript 파일 - 자동 생성됨 */
'use strict';

// 전역 네임스페이스 및 설정
window.SajuApp = {
    CONFIG: {
        API_URL: 'https://sajujipi-backend.onrender.com/analysis',
        LOADING_MESSAGE: '분석 중입니다... 잠시만 기다려주세요.',
        ERROR_MESSAGE: '분석 중 오류가 발생했습니다.',
        PLACEHOLDER_IMAGE: 'https://via.placeholder.com/400x300/E0E0E0/FFFFFF?text=No+Image'
    }
};

const { CONFIG, Utils, SajuAPI, FormValidator, BaseDisplay, DisplayManager } = (() => {
    // 유틸리티 함수
    const Utils = {
        getElement: id => document.getElementById(id),
        createHTML: (tag, content, className = '') => {
            const el = document.createElement(tag);
            if (className) el.className = className;
            if (typeof content === 'string') el.innerHTML = content;
            else if (content) el.appendChild(content);
            return el;
        },
        safeGet: (obj, path, def = '') => path.split('.').reduce((c, k) => (c && c[k] != null) ? c[k] : def, obj),
        showSkeleton: (show = true) => {
            const skeleton = Utils.getElement('skeleton-container');
            if (skeleton) skeleton.style.display = show ? 'block' : 'none';
        },
        showError: (element, error) => {
            if (!element) return;
            element.innerHTML = `<div class="error-message"><p>❌ ${error.message || CONFIG.ERROR_MESSAGE}</p><p class="error-detail">${error.detail || '잠시 후 다시 시도해주세요.'}</p></div>`;
        },
        scrollToElement: (elementId, offset = 100) => {
            const el = Utils.getElement(elementId);
            if (el) {
                const y = el.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: y, behavior: 'smooth' });
            }
        }
    };

    // API 통신
    const SajuAPI = class {
        static async analyze(birthData) {
            try {
                const res = await fetch(CONFIG.API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(Object.fromEntries(Object.entries(birthData).map(([k, v]) => [k, parseInt(v)])))
                });
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                const data = await res.json();
                if (data.status === 'error') throw new Error(data.message);
                return data.analysis_result || data.result;
            } catch (error) {
                console.error('API 호출 오류:', error);
                throw { message: '서버 연결 오류', detail: error.message };
            }
        }
    };
    
    // 폼 유효성 검사
    const FormValidator = class {
        validate(data) {
            const fields = ['year', 'month', 'day', 'hour', 'minute'];
            for (const field of fields) {
                if (!data[field]) return { isValid: false, message: '모든 생년월일 정보를 입력해주세요.' };
                const val = parseInt(data[field]);
                if (isNaN(val)) return { isValid: false, message: '올바른 숫자 형식으로 입력해주세요.'};
                if (field === 'year' && (val < 1900 || val > new Date().getFullYear())) return { isValid: false, message: `연도는 1900년부터 ${new Date().getFullYear()}년 사이로 입력해주세요.` };
                if (field === 'month' && (val < 1 || val > 12)) return { isValid: false, message: '월은 1부터 12 사이로 입력해주세요.'};
                if (field === 'day' && (val < 1 || val > new Date(data.year, data.month, 0).getDate())) return { isValid: false, message: '유효하지 않은 날짜입니다.'};
                if (field === 'hour' && (val < 0 || val > 23)) return { isValid: false, message: '시간은 0부터 23 사이로 입력해주세요.'};
                if (field === 'minute' && (val < 0 || val > 59)) return { isValid: false, message: '분은 0부터 59 사이로 입력해주세요.'};
            }
            return { isValid: true };
        }
    };

    // 기본 디스플레이
    const BaseDisplay = class {
        constructor(sectionId) { this.section = Utils.getElement(sectionId); }
        clear() { if (this.section) this.section.innerHTML = ''; }
        show() { if(this.section) this.section.classList.add('visible'); }
        hide() { if(this.section) this.section.classList.remove('visible'); }
        createCard(title, content, className = '') {
            return Utils.createHTML('div', `
                <div class="card ${className}">
                    <h3 class="card-title">${title}</h3>
                    <div class="card-content">${this.formatContent(content)}</div>
                </div>`);
        }
        createImageCard(title, content, imageUrl) {
            const placeholder = `this.onerror=null; this.src='${CONFIG.PLACEHOLDER_IMAGE}';`;
            return Utils.createHTML('div', `
                <div class="card image-card">
                    <h3 class="card-title">${title}</h3>
                    <img src="${imageUrl || CONFIG.PLACEHOLDER_IMAGE}" alt="${title}" class="card-image" onerror="${placeholder}">
                    <div class="card-content">${this.formatContent(content)}</div>
                </div>`);
        }
        formatContent(content) {
            if (!content) return '';
            return content
                .replace(/【([^】]+)】/g, '<h4 class="section-title">$1</h4>')
                .replace(/▣\s*(.+)/g, '<h5 class="subsection-title">▣ $1</h5>')
                .replace(/•\s*(.+)/g, '<li>$1</li>')
                .replace(/\n/g, '<br>');
        }
    };

    // 각 분석 디스플레이 (상속)
    class IljuDisplay extends BaseDisplay {
        constructor() { super('ilju-analysis'); }
        display(data) {
            this.clear();
            const ilju = Utils.safeGet(data, 'ilju_analysis');
            if(ilju.title) this.section.appendChild(this.createImageCard(ilju.title, ilju.personality.overall, ilju.illustration_url));
            this.show();
        }
    }
    class SipsungDisplay extends BaseDisplay {
        constructor() { super('sipsung-analysis'); }
        display(data) {
            this.clear();
            const sipsung = Utils.safeGet(data, 'sipsung_analysis');
            if(sipsung.title) this.section.appendChild(this.createCard(sipsung.title, `${sipsung.content}<br><br>${sipsung.comprehensive}`));
            this.show();
        }
    }
    // ... 다른 디스플레이 클래스들도 유사하게 정의 ...
    class ComprehensiveDisplay extends BaseDisplay {
        constructor() { super('comprehensive-report'); }
        display(data) {
            this.clear();
            const report = Utils.safeGet(data, 'comprehensive_report');
            if(report.final_summary) this.section.appendChild(this.createCard(report.final_summary.title, report.final_summary.content));
            this.show();
        }
    }


    // 디스플레이 매니저
    const DisplayManager = class {
        constructor() {
            this.displays = {
                ilju: new IljuDisplay(),
                sipsung: new SipsungDisplay(),
                comprehensive: new ComprehensiveDisplay()
                // 모든 display 클래스 인스턴스화
            };
        }
        displayAll(data) { Object.values(this.displays).forEach(d => d.display(data)); }
        clearAll() { Object.values(this.displays).forEach(d => d.clear()); }
    };
    
    return { CONFIG, Utils, SajuAPI, FormValidator, BaseDisplay, DisplayManager };
})();

// 메인 애플리케이션
class SajuAppMain {
    constructor() {
        this.displayManager = new DisplayManager();
        this.validator = new FormValidator();
        this.init();
    }
    
    init() {
        Utils.getElement('analyze-btn')?.addEventListener('click', () => this.analyze());
    }
    
    async analyze() {
        const birthData = {
            year: Utils.getElement('year')?.value,
            month: Utils.getElement('month')?.value,
            day: Utils.getElement('day')?.value,
            hour: Utils.getElement('hour')?.value,
            minute: Utils.getElement('minute')?.value
        };
        
        const validation = this.validator.validate(birthData);
        if (!validation.isValid) {
            alert(validation.message);
            return;
        }

        const statusDiv = Utils.getElement('status');
        this.displayManager.clearAll();
        Utils.showSkeleton(true);
        if(statusDiv) statusDiv.innerHTML = '';

        try {
            const result = await SajuAPI.analyze(birthData);
            this.displayManager.displayAll(result);
            Utils.scrollToElement('ilju-analysis');
        } catch (error) {
            Utils.showError(statusDiv, error);
        } finally {
            Utils.showSkeleton(false);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.sajuApp = new SajuAppMain();
});
