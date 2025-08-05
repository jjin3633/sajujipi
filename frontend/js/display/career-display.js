// 직업운 분석 디스플레이
import { BaseDisplay } from './base-display.js';

export class CareerDisplay extends BaseDisplay {
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