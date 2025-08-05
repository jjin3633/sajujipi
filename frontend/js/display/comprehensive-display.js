// 종합 리포트 디스플레이
import { BaseDisplay } from './base-display.js';

export class ComprehensiveDisplay extends BaseDisplay {
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