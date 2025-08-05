// 연애운 & 결혼운 분석 디스플레이
import { BaseDisplay } from './base-display.js';

export class LoveDisplay extends BaseDisplay {
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