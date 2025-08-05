// API 통신 모듈
import { CONFIG } from './config.js';

export class SajuAPI {
    static async analyze(birthData) {
        try {
            const response = await fetch(CONFIG.API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    year: parseInt(birthData.year),
                    month: parseInt(birthData.month),
                    day: parseInt(birthData.day),
                    hour: parseInt(birthData.hour),
                    minute: parseInt(birthData.minute)
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.message || '분석 실패');
            }

            return data.analysis_result || data.result;
            
        } catch (error) {
            console.error('API 호출 오류:', error);
            throw {
                message: '서버 연결 오류',
                detail: error.message
            };
        }
    }
    
    static async checkHealth() {
        try {
            const response = await fetch(CONFIG.API_URL.replace('/analysis', '/health'));
            return response.ok;
        } catch {
            return false;
        }
    }
}