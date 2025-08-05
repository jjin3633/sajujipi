// 대운 분석 디스플레이
import { BaseDisplay } from './base-display.js';

export class DaeunDisplay extends BaseDisplay {
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