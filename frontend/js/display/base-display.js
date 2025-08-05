// 기본 디스플레이 클래스
import { Utils } from '../utils.js';

export class BaseDisplay {
    constructor(sectionId) {
        this.section = Utils.getElement(sectionId);
    }
    
    clear() {
        if (this.section) {
            this.section.innerHTML = '';
        }
    }
    
    show() {
        Utils.toggleSection(this.section?.id, true);
    }
    
    hide() {
        Utils.toggleSection(this.section?.id, false);
    }
    
    createCard(title, content, className = '') {
        return Utils.createHTML('div', `
            <div class="card ${className}">
                <h3 class="card-title">${title}</h3>
                <div class="card-content">${content}</div>
            </div>
        `);
    }
    
    createImageCard(title, content, imageUrl) {
        return Utils.createHTML('div', `
            <div class="card image-card">
                <h3 class="card-title">${title}</h3>
                ${imageUrl ? `<img src="${imageUrl}" alt="${title}" class="card-image">` : ''}
                <div class="card-content">${content}</div>
            </div>
        `);
    }
    
    formatContent(content) {
        if (!content) return '';
        
        // 줄바꿈 처리
        return content
            .replace(/【([^】]+)】/g, '<h4 class="section-title">$1</h4>')
            .replace(/▣\s*(.+)/g, '<h5 class="subsection-title">▣ $1</h5>')
            .replace(/•\s*(.+)/g, '<li>$1</li>')
            .replace(/(\n|^)(\d+)\.\s*(.+)/g, '$1<div class="numbered-item"><span class="number">$2.</span>$3</div>')
            .replace(/\n/g, '<br>');
    }
}