// 전역 설정
const CONFIG = {
    API_URL: 'https://sajujipi-backend.onrender.com/analysis',
    LOADING_MESSAGE: '분석 중입니다... 잠시만 기다려주세요.',
    ERROR_MESSAGE: '분석 중 오류가 발생했습니다.'
};

// 유틸리티 함수들
const Utils = {
    // 안전한 DOM 요소 가져오기
    getElement: (id) => document.getElementById(id) || console.error(`Element ${id} not found`),
    
    // HTML 생성 헬퍼
    createHTML: (tag, content, className = '') => {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (typeof content === 'string') {
            element.innerHTML = content;
        } else if (content) {
            element.appendChild(content);
        }
        return element;
    },
    
    // 안전한 데이터 접근
    safeGet: (obj, path, defaultValue = '') => {
        return path.split('.').reduce((current, key) => {
            return current && current[key] !== undefined ? current[key] : defaultValue;
        }, obj);
    },
    
    // 로딩 상태 관리
    showLoading: (element) => {
        if (element) {
            element.innerHTML = `<div class="loading"></div> ${CONFIG.LOADING_MESSAGE}`;
        }
    },
    
    // 에러 처리
    showError: (element, error) => {
        if (element) {
            element.innerHTML = `${CONFIG.ERROR_MESSAGE} (오류: ${error.message})`;
        }
    }
};

// 분석 결과 표시 클래스
class AnalysisDisplay {
    constructor() {
        this.sections = {
            ilju: 'ilju-analysis-section',
            sipsung: 'sipsung-analysis-section',
            sibiunseong: 'sibiunseong-analysis-section',
            sibisinsal: 'sibisinsal-analysis-section',
            guin: 'guin-analysis-section',
            wealth: 'wealth-luck-analysis-section',
            love: 'love-luck-analysis-section',
            career: 'career-luck-analysis-section',
            health: 'health-luck-analysis-section',
            daeun: 'daeun-analysis-section',
            comprehensive: 'comprehensive-report-section'
        };
    }
    
    // 모든 섹션 초기화
    clearAllSections() {
        Object.values(this.sections).forEach(sectionId => {
            const section = Utils.getElement(sectionId);
            if (section) {
                const title = section.querySelector('h2')?.textContent || '분석';
                section.innerHTML = `<h2>${title}</h2>`;
            }
        });
    }
    
    // 섹션별 표시 함수들
    displayIljuAnalysis(data) {
        const section = Utils.getElement(this.sections.ilju);
        const iljuAnalysis = Utils.safeGet(data, 'ilju_analysis');
        
        if (!iljuAnalysis || iljuAnalysis.error) return;
        
        let html = `
            <h3>${iljuAnalysis.title || '일주 분석'}</h3>
            <p>${iljuAnalysis.description || ''}</p>
        `;
        
        // 일주 일러스트
        if (iljuAnalysis.illustration_url) {
            html += `
                <div id="ilju-illustration-container" class="illustration-container">
                    <h4>당신의 일주 일러스트</h4>
                    <img src="data:image/png;base64,${iljuAnalysis.illustration_url}" 
                         alt="일주 일러스트" 
                         class="ai-illustration">
                </div>
            `;
        }
        
        // 성격 장단점
        if (iljuAnalysis.personality) {
            html += `
                <div id="ilju-personality-container">
                    <h4>성격 분석</h4>
                    <div class="characteristics-list">
                        <div class="characteristic-item positive">
                            <h5>장점</h5>
                            <ul>${(iljuAnalysis.personality.pros || []).map(item => `<li>${item}</li>`).join('')}</ul>
                        </div>
                        <div class="characteristic-item negative">
                            <h5>단점</h5>
                            <ul>${(iljuAnalysis.personality.cons || []).map(item => `<li>${item}</li>`).join('')}</ul>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // 동물 특성
        if (iljuAnalysis.animal) {
            html += `
                <div id="ilju-animal-container">
                    <h4>동물 특성</h4>
                    <p><strong>${iljuAnalysis.animal.name}</strong>: ${iljuAnalysis.animal.characteristics?.join(', ') || ''}</p>
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    displaySipsungAnalysis(data) {
        const section = Utils.getElement(this.sections.sipsung);
        const sipsungAnalysis = Utils.safeGet(data, 'sipsung_analysis');
        
        if (!sipsungAnalysis || sipsungAnalysis.error) return;
        
        let html = '<h3>십성 분석</h3>';
        
        // 시기별 분석
        const periods = ['연간', '월간', '일간', '시간'];
        periods.forEach(period => {
            const analysis = sipsungAnalysis[period];
            if (analysis) {
                html += `
                    <div class="period-analysis">
                        <h4>${period} 십성</h4>
                        <p>${analysis}</p>
                    </div>
                `;
            }
        });
        
        // 종합 분석
        if (sipsungAnalysis.종합) {
            html += `
                <div class="comprehensive-analysis">
                    <h4>종합 분석</h4>
                    <p>${sipsungAnalysis.종합}</p>
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    displaySibiunseongAnalysis(data) {
        const section = Utils.getElement(this.sections.sibiunseong);
        const sibiunseongAnalysis = Utils.safeGet(data, 'sibiunseong_analysis');
        const illustrationUrl = Utils.safeGet(data, 'sibiunseong_illustration_url');
        
        if (!sibiunseongAnalysis || sibiunseongAnalysis.error) return;
        
        let html = '<h3>십이운성 분석</h3>';
        
        // 시기별 분석
        const periods = ['연간', '월간', '일간', '시간'];
        periods.forEach(period => {
            const analysis = sibiunseongAnalysis[period];
            if (analysis) {
                html += `
                    <div class="period-analysis">
                        <h4>${period} 운성</h4>
                        <p>${analysis}</p>
                    </div>
                `;
            }
        });
        
        // 종합 분석
        if (sibiunseongAnalysis.종합) {
            html += `
                <div class="comprehensive-analysis">
                    <h4>종합 분석</h4>
                    <p>${sibiunseongAnalysis.종합}</p>
                </div>
            `;
        }
        
        // 일러스트
        if (illustrationUrl) {
            html += `
                <div id="sibiunseong-illustration-container" class="illustration-container">
                    <h4>십이운성 일러스트</h4>
                    <img src="data:image/png;base64,${illustrationUrl}" 
                         alt="십이운성 일러스트" 
                         class="ai-illustration">
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    // 나머지 분석 함수들도 비슷한 패턴으로 최적화...
    displaySibisinsalAnalysis(data) {
        const section = Utils.getElement(this.sections.sibisinsal);
        const sibisinsalAnalysis = Utils.safeGet(data, 'sibisinsal_analysis');
        
        if (!sibisinsalAnalysis || sibisinsalAnalysis.error) return;
        
        let html = '<h3>십이신살 분석</h3>';
        
        const periods = ['초년기', '청년기', '중년기', '장년기'];
        periods.forEach(period => {
            const analysis = sibisinsalAnalysis[period];
            if (analysis) {
                html += `
                    <div class="period-analysis">
                        <h4>${period}</h4>
                        <p>${analysis}</p>
                    </div>
                `;
            }
        });
        
        section.innerHTML = html;
    }
    
    displayGuinAnalysis(data) {
        const section = Utils.getElement(this.sections.guin);
        const guinAnalysis = Utils.safeGet(data, 'guin_analysis');
        
        if (!guinAnalysis || guinAnalysis.error) return;
        
        let html = '<h3>귀인 분석</h3>';
        
        // 시기별 분석
        if (guinAnalysis.period_analysis) {
            const periods = ['초년기', '청년기', '중년기', '장년기'];
            periods.forEach(period => {
                const analysis = guinAnalysis.period_analysis[period];
                if (analysis) {
                    html += `
                        <div class="period-analysis">
                            <h4>${period}</h4>
                            <p>${analysis}</p>
                        </div>
                    `;
                }
            });
        }
        
        // 종합 분석
        if (guinAnalysis.comprehensive) {
            html += `
                <div class="comprehensive-analysis">
                    <h4>종합 분석</h4>
                    <p>${guinAnalysis.comprehensive}</p>
                </div>
            `;
        }
        
        // 초상화
        if (guinAnalysis.portrait_url) {
            html += `
                <div id="guin-portrait-container" class="illustration-container">
                    <h4>귀인 초상화</h4>
                    <img src="data:image/png;base64,${guinAnalysis.portrait_url}" 
                         alt="귀인 초상화" 
                         class="ai-illustration">
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    // 나머지 분석 함수들도 동일한 패턴으로 구현...
    displayWealthAnalysis(data) {
        const section = Utils.getElement(this.sections.wealth);
        const wealthAnalysis = Utils.safeGet(data, 'wealth_luck_analysis');
        
        if (!wealthAnalysis || wealthAnalysis.error) return;
        
        let html = '<h3>재물운 분석</h3>';
        
        // 기본 정보
        if (wealthAnalysis.title) {
            html += `<h4>${wealthAnalysis.title}</h4>`;
        }
        if (wealthAnalysis.description) {
            html += `<p>${wealthAnalysis.description}</p>`;
        }
        
        // 확장 분석
        if (wealthAnalysis.overall_flow) {
            html += `
                <div id="wealth-overall-flow">
                    <h4>전체 흐름</h4>
                    <p>${wealthAnalysis.overall_flow}</p>
                </div>
            `;
        }
        
        if (wealthAnalysis.characteristics) {
            html += `
                <div id="wealth-characteristics">
                    <h4>재물운 특징</h4>
                    ${wealthAnalysis.characteristics.map(char => `
                        <div class="characteristic-item">
                            <h5>${char.title}</h5>
                            <p>${char.description}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        if (wealthAnalysis.people_analysis) {
            html += `
                <div id="wealth-people-analysis">
                    <h4>사람 분석</h4>
                    <p>${wealthAnalysis.people_analysis}</p>
                </div>
            `;
        }
        
        if (wealthAnalysis.business_analysis) {
            html += `
                <div id="wealth-business-analysis">
                    <h4>사업/투자 조언</h4>
                    <p>${wealthAnalysis.business_analysis}</p>
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    // 나머지 함수들도 비슷한 패턴으로 구현...
    displayLoveAnalysis(data) {
        // 연애운 분석 구현
        const section = Utils.getElement(this.sections.love);
        const loveAnalysis = Utils.safeGet(data, 'love_luck_analysis');
        
        if (!loveAnalysis || loveAnalysis.error) return;
        
        let html = '<h3>연애운 & 결혼운 분석</h3>';
        
        // 기본 정보
        if (loveAnalysis.title) {
            html += `<h4>${loveAnalysis.title}</h4>`;
        }
        if (loveAnalysis.description) {
            html += `<p>${loveAnalysis.description}</p>`;
        }
        
        // 확장 분석
        if (loveAnalysis.overall_tendency) {
            html += `
                <div id="love-overall-tendency">
                    <h4>전체적 경향</h4>
                    <p>${loveAnalysis.overall_tendency}</p>
                </div>
            `;
        }
        
        if (loveAnalysis.destiny_partner) {
            html += `
                <div id="love-destiny-partner">
                    <h4>인연 상대</h4>
                    <p>${loveAnalysis.destiny_partner}</p>
                </div>
            `;
        }
        
        if (loveAnalysis.improvement_points) {
            html += `
                <div id="love-improvement-points">
                    <h4>개선점</h4>
                    <p>${loveAnalysis.improvement_points}</p>
                </div>
            `;
        }
        
        if (loveAnalysis.flow_analysis) {
            html += `
                <div id="love-flow-analysis">
                    <h4>흐름 분석</h4>
                    <p>${loveAnalysis.flow_analysis}</p>
                </div>
            `;
        }
        
        if (loveAnalysis.timing_location) {
            html += `
                <div id="love-timing-location">
                    <h4>시기/장소</h4>
                    <p>${loveAnalysis.timing_location}</p>
                </div>
            `;
        }
        
        // 일러스트
        if (loveAnalysis.illustration_url) {
            html += `
                <div id="love-destiny-portrait-container" class="illustration-container">
                    <h4>인연 상대 초상화</h4>
                    <img src="data:image/png;base64,${loveAnalysis.illustration_url}" 
                         alt="인연 상대 초상화" 
                         class="ai-illustration">
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    displayCareerAnalysis(data) {
        const section = Utils.getElement(this.sections.career);
        const careerAnalysis = Utils.safeGet(data, 'career_luck_analysis');
        
        if (!careerAnalysis || careerAnalysis.error) return;
        
        let html = '<h3>직업운 분석</h3>';
        
        // 기본 정보
        if (careerAnalysis.title) {
            html += `<h4>${careerAnalysis.title}</h4>`;
        }
        if (careerAnalysis.description) {
            html += `<p>${careerAnalysis.description}</p>`;
        }
        
        // 확장 분석
        if (careerAnalysis.suitable_jobs) {
            html += `
                <div id="career-suitable-jobs">
                    <h4>적합한 직업</h4>
                    <ul>${careerAnalysis.suitable_jobs.map(job => `<li>${job}</li>`).join('')}</ul>
                </div>
            `;
        }
        
        if (careerAnalysis.business_vs_job) {
            html += `
                <div id="career-business-vs-job">
                    <h4>사업 vs 직장</h4>
                    <p>${careerAnalysis.business_vs_job}</p>
                </div>
            `;
        }
        
        if (careerAnalysis.advice) {
            html += `
                <div id="career-advice">
                    <h4>조언</h4>
                    <p>${careerAnalysis.advice}</p>
                </div>
            `;
        }
        
        if (careerAnalysis.caution_people) {
            html += `
                <div id="career-caution-people">
                    <h4>주의할 사람</h4>
                    <p>${careerAnalysis.caution_people}</p>
                </div>
            `;
        }
        
        // 아바타
        if (careerAnalysis.avatar_url) {
            html += `
                <div id="career-avatar-container" class="illustration-container">
                    <h4>직업 아바타</h4>
                    <img src="data:image/png;base64,${careerAnalysis.avatar_url}" 
                         alt="직업 아바타" 
                         class="ai-illustration">
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    displayHealthAnalysis(data) {
        const section = Utils.getElement(this.sections.health);
        const healthAnalysis = Utils.safeGet(data, 'health_luck_analysis');
        
        if (!healthAnalysis || healthAnalysis.error) return;
        
        let html = '<h3>건강운 분석</h3>';
        
        // 기본 정보
        if (healthAnalysis.title) {
            html += `<h4>${healthAnalysis.title}</h4>`;
        }
        if (healthAnalysis.description) {
            html += `<p>${healthAnalysis.description}</p>`;
        }
        
        // 확장 분석
        if (healthAnalysis.constitution) {
            html += `
                <div id="health-constitution">
                    <h4>체질</h4>
                    <p>${healthAnalysis.constitution}</p>
                </div>
            `;
        }
        
        if (healthAnalysis.weak_points) {
            html += `
                <div id="health-risk-areas">
                    <h4>위험 부위</h4>
                    <ul>${healthAnalysis.weak_points.map(point => `<li>${point}</li>`).join('')}</ul>
                </div>
            `;
        }
        
        if (healthAnalysis.suitable_exercise) {
            html += `
                <div id="health-suitable-exercise">
                    <h4>적합한 운동</h4>
                    <p>${healthAnalysis.suitable_exercise}</p>
                </div>
            `;
        }
        
        if (healthAnalysis.timing_analysis) {
            html += `
                <div id="health-timing-analysis">
                    <h4>시기별 분석</h4>
                    <p>${healthAnalysis.timing_analysis}</p>
                </div>
            `;
        }
        
        if (healthAnalysis.care_advice) {
            html += `
                <div id="health-care-advice">
                    <h4>관리 조언</h4>
                    <p>${healthAnalysis.care_advice}</p>
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    displayDaeunAnalysis(data) {
        const section = Utils.getElement(this.sections.daeun);
        const lifeFlowAnalysis = Utils.safeGet(data, 'life_flow_analysis');
        
        if (!lifeFlowAnalysis || lifeFlowAnalysis.error) return;
        
        let html = '<h3>대운 분석</h3>';
        
        // 90년 대운
        if (lifeFlowAnalysis.daeun_periods) {
            html += `
                <div id="daeun-90-years">
                    <h4>90년 대운</h4>
                    ${lifeFlowAnalysis.daeun_periods.map(period => `
                        <div class="period-analysis">
                            <h5>${period.period} (${period.age_range})</h5>
                            <p><strong>${period.status}</strong>: ${period.description}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        // 5년 세운
        if (lifeFlowAnalysis.seun_periods) {
            html += `
                <div id="daeun-5-years-future">
                    <h4>5년 세운</h4>
                    ${lifeFlowAnalysis.seun_periods.map(period => `
                        <div class="period-analysis">
                            <h5>${period.year}년</h5>
                            <p><strong>${period.status}</strong>: ${period.description}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        // 변화점
        if (lifeFlowAnalysis.change_points) {
            html += `
                <div id="daeun-samjae-analysis">
                    <h4>곧 맞딱뜨릴 삼재</h4>
                    ${lifeFlowAnalysis.change_points.map(point => `
                        <div class="caution-section">
                            <h5>${point.age}</h5>
                            <p>${point.description}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        // 미래 전망
        if (lifeFlowAnalysis.future_outlook) {
            html += `
                <div class="future-outlook">
                    <h4>미래 전망</h4>
                    <p>${lifeFlowAnalysis.future_outlook}</p>
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
    
    displayComprehensiveReport(data) {
        const section = Utils.getElement(this.sections.comprehensive);
        const comprehensiveReport = Utils.safeGet(data, 'comprehensive_report');
        
        if (!comprehensiveReport || comprehensiveReport.error) return;
        
        let html = '<h3>종합 리포트</h3>';
        
        // 종합 요약
        if (comprehensiveReport.summary) {
            html += `
                <div id="comprehensive-summary" class="comprehensive-analysis">
                    <h4>종합 요약</h4>
                    <p>${comprehensiveReport.summary}</p>
                </div>
            `;
        }
        
        // 종합 권장사항
        if (comprehensiveReport.recommendations) {
            html += `
                <div id="comprehensive-recommendations" class="recommendation-section">
                    <h5>종합 권장사항</h5>
                    <p>${comprehensiveReport.recommendations}</p>
                </div>
            `;
        }
        
        // 미래 전망
        if (comprehensiveReport.future_outlook) {
            html += `
                <div id="comprehensive-future-outlook" class="future-outlook">
                    <h4>미래 전망</h4>
                    <p>${comprehensiveReport.future_outlook}</p>
                </div>
            `;
        }
        
        section.innerHTML = html;
    }
}

// 전역 인스턴스 생성
const analysisDisplay = new AnalysisDisplay();

// 메인 분석 함수
async function getAnalysis() {
    // 입력 값 가져오기
    const year = Utils.getElement('year').value;
    const month = Utils.getElement('month').value;
    const day = Utils.getElement('day').value;
    const hour = Utils.getElement('hour').value;
    const minute = Utils.getElement('minute').value;
    
    const statusDiv = Utils.getElement('status-message');

    // 입력 검증
    if (!year || !month || !day || !hour || !minute) {
        statusDiv.innerHTML = "모든 값을 입력해주세요.";
        return;
    }

    // 이전 결과 초기화
    analysisDisplay.clearAllSections();
    Utils.showLoading(statusDiv);

    try {
        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                year: parseInt(year),
                month: parseInt(month),
                day: parseInt(day),
                hour: parseInt(hour),
                minute: parseInt(minute)
            }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        
        // 성공 시 상태 메시지 제거
        statusDiv.innerHTML = ""; 

        // 각 섹션별 분석 결과 표시
        analysisDisplay.displayIljuAnalysis(data.analysis_result);
        analysisDisplay.displaySipsungAnalysis(data.analysis_result);
        analysisDisplay.displaySibiunseongAnalysis(data.analysis_result);
        analysisDisplay.displaySibisinsalAnalysis(data.analysis_result);
        analysisDisplay.displayGuinAnalysis(data.analysis_result);
        analysisDisplay.displayWealthAnalysis(data.analysis_result);
        analysisDisplay.displayLoveAnalysis(data.analysis_result);
        analysisDisplay.displayCareerAnalysis(data.analysis_result);
        analysisDisplay.displayHealthAnalysis(data.analysis_result);
        analysisDisplay.displayDaeunAnalysis(data.analysis_result);
        analysisDisplay.displayComprehensiveReport(data.analysis_result);

    } catch (error) {
        console.error('Error:', error);
        Utils.showError(statusDiv, error);
        analysisDisplay.clearAllSections();
    }
}
