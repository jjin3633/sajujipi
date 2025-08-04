async function getAnalysis() {
    // 입력 값 및 HTML 요소 가져오기
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    const hour = document.getElementById('hour').value;
    const minute = document.getElementById('minute').value;
    
    const statusDiv = document.getElementById('status-message');

    // 1. 이전 결과 초기화
    clearAllSections();
    statusDiv.innerHTML = ""; 

    if (!year || !month || !day || !hour || !minute) {
        statusDiv.innerHTML = "모든 값을 입력해주세요.";
        return;
    }

    // 2. "분석 중" 상태 메시지 표시
    statusDiv.innerHTML = '<div class="loading"></div> 분석 중입니다... 잠시만 기다려주세요.';

    try {
        const response = await fetch('https://sajujipi-backend.onrender.com/analysis', {
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
        
        // 3. 성공 시 상태 메시지 제거
        statusDiv.innerHTML = ""; 

        // 4. 각 섹션별 분석 결과 표시
        displayIljuAnalysis(data.analysis_result);
        displaySipsungAnalysis(data.analysis_result);
        displaySibiunseongAnalysis(data.analysis_result);
        displaySibisinsalAnalysis(data.analysis_result);
        displayGuinAnalysis(data.analysis_result);
        displayWealthAnalysis(data.analysis_result);
        displayLoveAnalysis(data.analysis_result);
        displayCareerAnalysis(data.analysis_result);
        displayHealthAnalysis(data.analysis_result);
        displayDaeunAnalysis(data.analysis_result);
        displayComprehensiveReport(data.analysis_result);

    } catch (error) {
        console.error('Error:', error);
        statusDiv.innerHTML = `분석 중 오류가 발생했습니다. (오류: ${error.message})`;
        clearAllSections();
    }
}

function clearAllSections() {
    // 모든 섹션 초기화
    const sections = [
        'ilju-analysis-section', 'sipsung-analysis-section', 'sibiunseong-analysis-section',
        'sibisinsal-analysis-section', 'guin-analysis-section', 'wealth-luck-analysis-section',
        'love-luck-analysis-section', 'career-luck-analysis-section', 'health-luck-analysis-section',
        'daeun-analysis-section', 'comprehensive-report-section'
    ];
    
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.innerHTML = `<h2>${section.querySelector('h2')?.textContent || '분석'}</h2>`;
        }
    });
}

// 1. 일주 분석 표시
function displayIljuAnalysis(data) {
    const iljuSection = document.getElementById('ilju-analysis-section');
    const iljuAnalysis = data.ilju_analysis;
    
    if (iljuAnalysis && !iljuAnalysis.error) {
        let html = `
            <h3>${iljuAnalysis.title}</h3>
            <p>${iljuAnalysis.description}</p>
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
        if (iljuAnalysis.pros && iljuAnalysis.pros.length > 0) {
            html += `
                <div id="ilju-personality-container">
                    <h4>내 성격 장점</h4>
                    <ul>${iljuAnalysis.pros.map(pro => `<li>${pro}</li>`).join('')}</ul>
                </div>
            `;
        }
        
        if (iljuAnalysis.cons && iljuAnalysis.cons.length > 0) {
            html += `
                <div id="ilju-personality-container">
                    <h4>내 성격 단점</h4>
                    <ul>${iljuAnalysis.cons.map(con => `<li>${con}</li>`).join('')}</ul>
                </div>
            `;
        }
        
        // 일주 동물 특징
        if (iljuAnalysis.animal) {
            html += `
                <div id="ilju-animal-container">
                    <h4>내 일주 동물 특징</h4>
                    <p>${iljuAnalysis.animal}</p>
                </div>
            `;
        }
        
        iljuSection.innerHTML = html;
    }
}

// 2. 십성 분석 표시
function displaySipsungAnalysis(data) {
    const sipsungSection = document.getElementById('sipsung-analysis-section');
    const sipsungAnalysis = data.sipsung_analysis;
    
    if (sipsungAnalysis && !sipsungAnalysis.error) {
        let html = '';
        
        // 시기별 성향 분석
        html += '<div id="sipsung-period-analysis">';
        html += '<h4>시기별 성향 분석</h4>';
        for (const [period, analysis] of Object.entries(sipsungAnalysis)) {
            html += `
                <div class="period-analysis">
                    <h5>${period}</h5>
                    <p>${analysis}</p>
                </div>
            `;
        }
        html += '</div>';
        
        // 종합 성향 분석
        html += `
            <div id="sipsung-comprehensive-analysis" class="comprehensive-analysis">
                <h4>종합 성향 분석</h4>
                <p>당신의 십성 분석을 종합하면, ${getSipsungSummary(sipsungAnalysis)}</p>
            </div>
        `;
        
        sipsungSection.innerHTML = html;
    }
}

// 3. 십이운성 분석 표시
function displaySibiunseongAnalysis(data) {
    const sibiunseongSection = document.getElementById('sibiunseong-analysis-section');
    const sibiunseongAnalysis = data.sibiunseong_analysis;
    
    if (sibiunseongAnalysis && !sibiunseongAnalysis.error) {
        let html = '';
        
        // 시기별 십이운성 분석
        html += '<div id="sibiunseong-period-analysis">';
        html += '<h4>시기별 십이운성 분석</h4>';
        for (const [period, analysis] of Object.entries(sibiunseongAnalysis)) {
            html += `
                <div class="period-analysis">
                    <h5>${period.replace('주', '운')}</h5>
                    <p>${analysis}</p>
                </div>
            `;
        }
        html += '</div>';
        
        // 종합 십이운성 분석
        html += `
            <div id="sibiunseong-comprehensive-analysis" class="comprehensive-analysis">
                <h4>종합 십이운성 분석</h4>
                <p>당신의 십이운성 분석을 종합하면, ${getSibiunseongSummary(sibiunseongAnalysis)}</p>
            </div>
        `;
        
        // 십이운성 일러스트
        if (data.sibiunseong_illustration_url) {
            html += `
                <div id="sibiunseong-illustration-container" class="illustration-container">
                    <h4>나의 십이운성 일러스트</h4>
                    <img src="data:image/png;base64,${data.sibiunseong_illustration_url}" 
                         alt="십이운성 일러스트" 
                         class="ai-illustration">
                </div>
            `;
        }
        
        sibiunseongSection.innerHTML = html;
    }
}

// 4. 십이신살 분석 표시
function displaySibisinsalAnalysis(data) {
    const sibisinsalSection = document.getElementById('sibisinsal-analysis-section');
    const sibisinsalAnalysis = data.sibisinsal_analysis;
    
    if (sibisinsalAnalysis && !sibisinsalAnalysis.error) {
        let html = '<div id="sibisinsal-period-analysis">';
        html += '<h4>시기별 십이신살 분석</h4>';
        
        for (const [period, analysis] of Object.entries(sibisinsalAnalysis)) {
            html += `
                <div class="period-analysis">
                    <h5>${period}</h5>
                    <p>${analysis}</p>
                </div>
            `;
        }
        
        html += '</div>';
        sibisinsalSection.innerHTML = html;
    }
}

// 5. 귀인 분석 표시
function displayGuinAnalysis(data) {
    const guinSection = document.getElementById('guin-analysis-section');
    const guinAnalysis = data.guin_analysis;
    
    if (guinAnalysis && !guinAnalysis.error) {
        let html = '';
        
        // 시기별 귀인 분석
        html += '<div id="guin-period-analysis">';
        html += '<h4>시기별 귀인 분석</h4>';
        for (const [period, analysis] of Object.entries(guinAnalysis.period_analysis || {})) {
            html += `
                <div class="period-analysis">
                    <h5>${period}</h5>
                    <p>${analysis}</p>
                </div>
            `;
        }
        html += '</div>';
        
        // 종합 귀인 분석
        if (guinAnalysis.comprehensive) {
            html += `
                <div id="guin-comprehensive-analysis" class="comprehensive-analysis">
                    <h4>종합 귀인 분석</h4>
                    <p>${guinAnalysis.comprehensive}</p>
                </div>
            `;
        }
        
        // 귀인 초상화
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
        
        guinSection.innerHTML = html;
    }
}

// 6. 재물운 분석 표시
function displayWealthAnalysis(data) {
    const wealthSection = document.getElementById('wealth-luck-analysis-section');
    const wealthAnalysis = data.wealth_luck_analysis;
    
    if (wealthAnalysis && !wealthAnalysis.error) {
        let html = `
            <h3>${wealthAnalysis.title}</h3>
            <p>${wealthAnalysis.description}</p>
        `;
        
        // 전반적인 재물운 흐름
        if (wealthAnalysis.overall_flow) {
            html += `
                <div id="wealth-overall-flow" class="flow-analysis">
                    <h4>전반적인 재물운 흐름</h4>
                    <p>${wealthAnalysis.overall_flow}</p>
                </div>
            `;
        }
        
        // 내 재물운 특징
        if (wealthAnalysis.characteristics) {
            html += `
                <div id="wealth-characteristics">
                    <h4>내 재물운 특징</h4>
                    <div class="characteristics-list">
                        ${wealthAnalysis.characteristics.map(char => `
                            <div class="characteristic-item">
                                <h5>${char.title}</h5>
                                <p>${char.description}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        // 이익과 손해를 가져다 줄 사람들
        if (wealthAnalysis.people_analysis) {
            html += `
                <div id="wealth-people-analysis">
                    <h4>나에게 이익과 손해를 가져다 줄 사람들</h4>
                    <p>${wealthAnalysis.people_analysis}</p>
                </div>
            `;
        }
        
        // 재테크 분석
        if (wealthAnalysis.business_analysis) {
            html += `
                <div id="wealth-business-analysis" class="recommendation-section">
                    <h5>나에게 맞는 사업 아이템 또는 재테크</h5>
                    <p>${wealthAnalysis.business_analysis}</p>
                </div>
            `;
        }
        
        // 재물운 그래프
        if (wealthAnalysis.graph_data) {
            html += `
                <div id="wealth-graph-container" class="graph-container">
                    <h4>인생의 재물운 그래프</h4>
                    <div id="wealth-chart"></div>
                </div>
            `;
        }
        
        wealthSection.innerHTML = html;
    }
}

// 7. 연애운 & 결혼운 분석 표시
function displayLoveAnalysis(data) {
    const loveSection = document.getElementById('love-luck-analysis-section');
    const loveAnalysis = data.love_luck_analysis;
    
    if (loveAnalysis && !loveAnalysis.error) {
        let html = `
            <h3>${loveAnalysis.title}</h3>
            <p>${loveAnalysis.description}</p>
        `;
        
        // 전반적인 연애 성향
        if (loveAnalysis.overall_tendency) {
            html += `
                <div id="love-overall-tendency">
                    <h4>나의 전반적인 연애 성향</h4>
                    <p>${loveAnalysis.overall_tendency}</p>
                </div>
            `;
        }
        
        // 운명의 짝 소개
        if (loveAnalysis.destiny_partner) {
            html += `
                <div id="love-destiny-partner">
                    <h4>내 운명의 짝 소개</h4>
                    <p>${loveAnalysis.destiny_partner}</p>
                </div>
            `;
        }
        
        // 개선점
        if (loveAnalysis.improvement_points) {
            html += `
                <div id="love-improvement-points" class="caution-section">
                    <h5>이성에게 사랑받기 위한 나의 부족한 점 & 개선점</h5>
                    <p>${loveAnalysis.improvement_points}</p>
                </div>
            `;
        }
        
        // 애정운 흐름
        if (loveAnalysis.flow_analysis) {
            html += `
                <div id="love-flow-analysis" class="flow-analysis">
                    <h4>내 애정운 흐름</h4>
                    <p>${loveAnalysis.flow_analysis}</p>
                </div>
            `;
        }
        
        // 연애운이 높은 시기와 장소
        if (loveAnalysis.timing_location) {
            html += `
                <div id="love-timing-location" class="timing-location">
                    <h5>나의 연애운이 높은 시기와 장소</h5>
                    <p>${loveAnalysis.timing_location}</p>
                </div>
            `;
        }
        
        // 운명의 짝 초상화
        if (loveAnalysis.destiny_portrait_url) {
            html += `
                <div id="love-destiny-portrait-container" class="illustration-container">
                    <h4>운명의 짝 초상화</h4>
                    <img src="data:image/png;base64,${loveAnalysis.destiny_portrait_url}" 
                         alt="운명의 짝 초상화" 
                         class="ai-illustration">
                </div>
            `;
        }
        
        loveSection.innerHTML = html;
    }
}

// 8. 직업운 분석 표시
function displayCareerAnalysis(data) {
    const careerSection = document.getElementById('career-luck-analysis-section');
    const careerAnalysis = data.career_luck_analysis;
    
    if (careerAnalysis && !careerAnalysis.error) {
        let html = `
            <h3>${careerAnalysis.title}</h3>
            <p>${careerAnalysis.description}</p>
        `;
        
        // 잘 맞는 직업/직장
        if (careerAnalysis.suitable_jobs) {
            html += `
                <div id="career-suitable-jobs">
                    <h4>나와 잘 맞는 직업/직장</h4>
                    <ul>${careerAnalysis.suitable_jobs.map(job => `<li>${job}</li>`).join('')}</ul>
                </div>
            `;
        }
        
        // 사업 vs 직장 분석
        if (careerAnalysis.business_vs_job) {
            html += `
                <div id="career-business-vs-job" class="recommendation-section">
                    <h5>사업 vs 직장 나에겐 뭐가 맞을까 분석</h5>
                    <p>${careerAnalysis.business_vs_job}</p>
                </div>
            `;
        }
        
        // 성공적인 직장생활을 위한 조언
        if (careerAnalysis.advice) {
            html += `
                <div id="career-advice" class="recommendation-section">
                    <h5>성공적인 직장생활을 위한 조언</h5>
                    <p>${careerAnalysis.advice}</p>
                </div>
            `;
        }
        
        // 주의해야 할 사람 분석
        if (careerAnalysis.caution_people) {
            html += `
                <div id="career-caution-people" class="caution-section">
                    <h5>주의해야 할 사람 분석</h5>
                    <p>${careerAnalysis.caution_people}</p>
                </div>
            `;
        }
        
        // AI 아바타
        if (careerAnalysis.avatar_url) {
            html += `
                <div class="avatar-container">
                    <h4>당신의 직업 아바타</h4>
                    <img src="data:image/png;base64,${careerAnalysis.avatar_url}" 
                         alt="직업 아바타" 
                         class="ai-avatar">
                </div>
            `;
        }
        
        careerSection.innerHTML = html;
    }
}

// 9. 건강운 분석 표시
function displayHealthAnalysis(data) {
    const healthSection = document.getElementById('health-luck-analysis-section');
    const healthAnalysis = data.health_luck_analysis;
    
    if (healthAnalysis && !healthAnalysis.error) {
        let html = `
            <h3>${healthAnalysis.title}</h3>
            <p>${healthAnalysis.description}</p>
        `;
        
        // 타고난 체질과 건강 상태
        if (healthAnalysis.constitution) {
            html += `
                <div id="health-constitution">
                    <h4>타고난 체질과 건강 상태 브리핑</h4>
                    <p>${healthAnalysis.constitution}</p>
                </div>
            `;
        }
        
        // 강점과 주의점
        if (healthAnalysis.strong_points && healthAnalysis.strong_points.length > 0) {
            html += `
                <h4>강점</h4>
                <ul>${healthAnalysis.strong_points.map(point => `<li>${point}</li>`).join('')}</ul>
            `;
        }
        
        if (healthAnalysis.weak_points && healthAnalysis.weak_points.length > 0) {
            html += `
                <h4>주의점</h4>
                <ul>${healthAnalysis.weak_points.map(point => `<li>${point}</li>`).join('')}</ul>
            `;
        }
        
        // 잘 맞는 운동
        if (healthAnalysis.suitable_exercise) {
            html += `
                <div id="health-suitable-exercise" class="recommendation-section">
                    <h5>나와 잘 맞는 운동은?</h5>
                    <p>${healthAnalysis.suitable_exercise}</p>
                </div>
            `;
        }
        
        // 시기에 따른 건강운
        if (healthAnalysis.timing_analysis) {
            html += `
                <div id="health-timing-analysis">
                    <h4>시기에 따른 건강운</h4>
                    <p>${healthAnalysis.timing_analysis}</p>
                </div>
            `;
        }
        
        // 오행 균형
        if (healthAnalysis.oheng_balance) {
            html += `
                <h4>오행 균형</h4>
                <p>${healthAnalysis.oheng_balance} 오행 분포를 가지고 있습니다.</p>
            `;
        }
        
        // 건강 관리 조언
        if (healthAnalysis.care_advice) {
            html += `
                <h4>건강 관리 조언</h4>
                <p>${healthAnalysis.care_advice}</p>
            `;
        }
        
        healthSection.innerHTML = html;
    }
}

// 10. 대운 분석 표시
function displayDaeunAnalysis(data) {
    const daeunSection = document.getElementById('daeun-analysis-section');
    const lifeFlowAnalysis = data.life_flow_analysis;
    
    if (lifeFlowAnalysis && !lifeFlowAnalysis.error) {
        let html = '';
        
        // 90세까지의 대운
        if (lifeFlowAnalysis.daeun_periods) {
            html += '<div id="daeun-90-years">';
            html += '<h4>90세까지의 대운</h4>';
            for (const period of lifeFlowAnalysis.daeun_periods) {
                html += `
                    <div class="period-analysis">
                        <h5>${period.period} (${period.age_range})</h5>
                        <p><strong>${period.status}:</strong> ${period.description}</p>
                    </div>
                `;
            }
            html += '</div>';
        }
        
        // 향후 5년간의 연운과 삼재
        if (lifeFlowAnalysis.seun_periods) {
            html += '<div id="daeun-5-years-future">';
            html += '<h4>향후 5년간의 연운과 삼재</h4>';
            for (const period of lifeFlowAnalysis.seun_periods) {
                html += `
                    <div class="period-analysis">
                        <h5>${period.year}년 (${period.status})</h5>
                        <p>${period.description}</p>
                    </div>
                `;
            }
            html += '</div>';
        }
        
        // 곧 맞딱뜨릴 삼재
        if (lifeFlowAnalysis.change_points) {
            html += '<div id="daeun-samjae-analysis">';
            html += '<h4>곧 맞딱뜨릴 삼재</h4>';
            for (const point of lifeFlowAnalysis.change_points) {
                html += `
                    <div class="caution-section">
                        <h5>${point.age}</h5>
                        <p>${point.description}</p>
                    </div>
                `;
            }
            html += '</div>';
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
        
        daeunSection.innerHTML = html;
    }
}

// 11. 종합 리포트 표시
function displayComprehensiveReport(data) {
    const comprehensiveSection = document.getElementById('comprehensive-report-section');
    const comprehensiveReport = data.comprehensive_report;
    
    if (comprehensiveReport && !comprehensiveReport.error) {
        let html = '';
        
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
        
        comprehensiveSection.innerHTML = html;
    }
}

// 헬퍼 함수들
function getSipsungSummary(sipsungAnalysis) {
    // 십성 분석 요약 생성
    return "당신의 십성 분석을 통해 인생의 각 시기별 특성을 파악할 수 있습니다.";
}

function getSibiunseongSummary(sibiunseongAnalysis) {
    // 십이운성 분석 요약 생성
    return "당신의 십이운성 분석을 통해 각 시기별 에너지의 흐름을 이해할 수 있습니다.";
}

function generateComprehensiveSummary(data) {
    // 종합 요약 생성
    return "당신의 사주를 종합적으로 분석한 결과, 다양한 운세의 조화를 통해 인생의 방향성을 제시합니다.";
}

function generateComprehensiveRecommendations(data) {
    // 종합 권장사항 생성
    return "현재 상황과 미래 전망을 고려한 구체적인 권장사항을 제시합니다.";
}

function generateComprehensiveFutureOutlook(data) {
    // 종합 미래 전망 생성
    return "당신의 사주를 바탕으로 한 미래 전망과 준비해야 할 사항들을 안내합니다.";
}
