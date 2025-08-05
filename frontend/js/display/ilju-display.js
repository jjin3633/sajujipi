// 일주 분석 디스플레이
import { BaseDisplay } from './base-display.js';
import { Utils } from '../utils.js';

export class IljuDisplay extends BaseDisplay {
    constructor() {
        super('ilju-analysis');
    }
    
    display(data) {
        this.clear();
        
        const iljuData = Utils.safeGet(data, 'comprehensive_report.ilju_analysis', null);
        
        if (!iljuData) {
            this.section.innerHTML = '<p class="no-data">일주 분석 데이터가 없습니다.</p>';
            return;
        }
        
        const content = this.formatContent(iljuData.content || '');
        const card = this.createImageCard(
            iljuData.title || '일주 분석',
            content,
            iljuData.illustration_url
        );
        
        this.section.appendChild(card);
        this.show();
    }
}