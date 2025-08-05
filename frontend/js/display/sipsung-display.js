// 십성 분석 디스플레이
import { BaseDisplay } from './base-display.js';

export class SipsungDisplay extends BaseDisplay {
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