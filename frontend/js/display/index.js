// 디스플레이 모듈 통합
import { IljuDisplay } from './ilju-display.js';
import { SipsungDisplay } from './sipsung-display.js';
import { SibiunseongDisplay } from './sibiunseong-display.js';
import { CareerDisplay } from './career-display.js';
import { LoveDisplay } from './love-display.js';
import { WealthDisplay } from './wealth-display.js';
import { HealthDisplay } from './health-display.js';
import { DaeunDisplay } from './daeun-display.js';
import { ComprehensiveDisplay } from './comprehensive-display.js';

export class DisplayManager {
    constructor() {
        this.displays = {
            ilju: new IljuDisplay(),
            sipsung: new SipsungDisplay(),
            sibiunseong: new SibiunseongDisplay(),
            career: new CareerDisplay(),
            love: new LoveDisplay(),
            wealth: new WealthDisplay(),
            health: new HealthDisplay(),
            daeun: new DaeunDisplay(),
            comprehensive: new ComprehensiveDisplay()
        };
    }
    
    displayAll(data) {
        // 모든 섹션 표시
        Object.values(this.displays).forEach(display => {
            display.display(data);
        });
    }
    
    clearAll() {
        // 모든 섹션 초기화
        Object.values(this.displays).forEach(display => {
            display.clear();
        });
    }
    
    hideAll() {
        // 모든 섹션 숨기기
        Object.values(this.displays).forEach(display => {
            display.hide();
        });
    }
}