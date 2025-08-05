// 유틸리티 함수들
export const Utils = {
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
        const section = Utils.getElement(sectionId);
        if (section) {
            section.style.display = show ? 'block' : 'none';
        }
    },
    
    // 스크롤 애니메이션
    scrollToElement: (elementId, offset = 100) => {
        const element = Utils.getElement(elementId);
        if (element) {
            const y = element.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top: y, behavior: 'smooth' });
        }
    }
};