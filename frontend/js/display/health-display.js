// 건강운 분석 디스플레이
import { BaseDisplay } from './base-display.js';

export class HealthDisplay extends BaseDisplay {
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