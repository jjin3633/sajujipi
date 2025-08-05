// 재물운 분석 디스플레이
import { BaseDisplay } from './base-display.js';

export class WealthDisplay extends BaseDisplay {
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