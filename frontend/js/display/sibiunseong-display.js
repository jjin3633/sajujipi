// 십이운성 분석 디스플레이
import { BaseDisplay } from './base-display.js';

export class SibiunseongDisplay extends BaseDisplay {
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