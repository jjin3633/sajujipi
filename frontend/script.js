async function getAnalysis() {
    // 입력 값 및 HTML 요소 가져오기
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    const hour = document.getElementById('hour').value;
    const minute = document.getElementById('minute').value;
    
    const statusDiv = document.getElementById('status-message');
    const iljuSection = document.getElementById('ilju-analysis-section');
    const wealthLuckSection = document.getElementById('wealth-luck-analysis-section');
    const loveLuckSection = document.getElementById('love-luck-analysis-section');
    const careerLuckSection = document.getElementById('career-luck-analysis-section');
    const healthLuckSection = document.getElementById('health-luck-analysis-section');
    const sipsungSection = document.getElementById('sipsung-analysis-section');
    const sibiunseongSection = document.getElementById('sibiunseong-analysis-section');

    // 1. 이전 결과 초기화
    iljuSection.innerHTML = "";
    wealthLuckSection.innerHTML = "";
    loveLuckSection.innerHTML = "";
    careerLuckSection.innerHTML = "";
    healthLuckSection.innerHTML = "";
    sipsungSection.innerHTML = "";
    sibiunseongSection.innerHTML = "";
    statusDiv.innerHTML = ""; 

    if (!year || !month || !day || !hour || !minute) {
        statusDiv.innerHTML = "모든 값을 입력해주세요.";
        return;
    }

    // 2. "분석 중" 상태 메시지 표시
    statusDiv.innerHTML = "분석 중입니다... 잠시만 기다려주세요.";

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

        // 4. 일주 분석 결과 표시
        const iljuAnalysis = data.analysis_result.ilju_analysis;
        if (iljuAnalysis && !iljuAnalysis.error) {
            iljuSection.innerHTML = `
                <h2>일주 분석</h2>
                <h3>${iljuAnalysis.title}</h3>
                <p>${iljuAnalysis.description}</p>
                <h4>장점</h4>
                <ul>${iljuAnalysis.pros.map(pro => `<li>${pro}</li>`).join('')}</ul>
                <h4>단점</h4>
                <ul>${iljuAnalysis.cons.map(con => `<li>${con}</li>`).join('')}</ul>
                <h4>상징 동물</h4>
                <p>${iljuAnalysis.animal}</p>
            `;
        }

        // 5. 재물운 분석 결과 표시
        const wealthLuckAnalysis = data.analysis_result.wealth_luck_analysis;
        if (wealthLuckAnalysis && !wealthLuckAnalysis.error) {
            wealthLuckSection.innerHTML = `
                <h2>재물운 분석</h2>
                <h3>${wealthLuckAnalysis.title}</h3>
                <p>${wealthLuckAnalysis.description}</p>
            `;
        }

        // 6. 연애운 분석 결과 표시 (AI 일러스트 포함)
        const loveLuckAnalysis = data.analysis_result.love_luck_analysis;
        if (loveLuckAnalysis && !loveLuckAnalysis.error) {
            let loveHtml = `
                <h2>연애운 분석</h2>
                <h3>${loveLuckAnalysis.title}</h3>
                <p>${loveLuckAnalysis.description}</p>
            `;
            
            // AI 일러스트가 있으면 표시
            if (loveLuckAnalysis.illustration_url) {
                loveHtml += `
                    <div class="illustration-container">
                        <h4>당신의 연애 스타일 일러스트</h4>
                        <img src="data:image/png;base64,${loveLuckAnalysis.illustration_url}" 
                             alt="연애 스타일 일러스트" 
                             class="ai-illustration">
                    </div>
                `;
            }
            
            loveLuckSection.innerHTML = loveHtml;
        }

        // 7. 직업운 분석 결과 표시 (AI 아바타 포함)
        const careerLuckAnalysis = data.analysis_result.career_luck_analysis;
        if (careerLuckAnalysis && !careerLuckAnalysis.error) {
            let careerHtml = `
                <h2>직업운 분석</h2>
                <h3>${careerLuckAnalysis.title}</h3>
                <p>${careerLuckAnalysis.description}</p>
            `;
            
            // AI 아바타가 있으면 표시
            if (careerLuckAnalysis.avatar_url) {
                careerHtml += `
                    <div class="avatar-container">
                        <h4>당신의 직업 아바타</h4>
                        <img src="data:image/png;base64,${careerLuckAnalysis.avatar_url}" 
                             alt="직업 아바타" 
                             class="ai-avatar">
                    </div>
                `;
            }
            
            careerLuckSection.innerHTML = careerHtml;
        }

        // 8. 건강운 분석 결과 표시
        const healthLuckAnalysis = data.analysis_result.health_luck_analysis;
        if (healthLuckAnalysis && !healthLuckAnalysis.error) {
            healthLuckSection.innerHTML = `
                <h2>건강운 분석</h2>
                <h3>${healthLuckAnalysis.title}</h3>
                <p>${healthLuckAnalysis.description}</p>
                <h4>강점</h4>
                <ul>${healthLuckAnalysis.strong_points.map(point => `<li>${point}</li>`).join('')}</ul>
                <h4>주의점</h4>
                <ul>${healthLuckAnalysis.weak_points.map(point => `<li>${point}</li>`).join('')}</ul>
                <h4>오행 균형</h4>
                <p>${healthLuckAnalysis.oheng_balance} 오행 분포를 가지고 있습니다.</p>
                <h4>건강 관리 조언</h4>
                <p>${healthLuckAnalysis.care_advice}</p>
            `;
        }

        // 9. 시기별 십성 분석 결과 표시
        const sipsungAnalysis = data.analysis_result.sipsung_analysis;
        if (sipsungAnalysis && !sipsungAnalysis.error) {
            let sipsungHtml = '<h2>시기별 성향 분석 (십성)</h2>';
            for (const [period, analysis] of Object.entries(sipsungAnalysis)) {
                sipsungHtml += `
                    <h4>${period}</h4>
                    <p>${analysis}</p>
                `;
            }
            sipsungSection.innerHTML = sipsungHtml;
        }
        
        // 10. 시기별 십이운성 분석 결과 표시
        const sibiunseongAnalysis = data.analysis_result.sibiunseong_analysis;
        if (sibiunseongAnalysis && !sibiunseongAnalysis.error) {
            let sibiunseongHtml = '<h2>시기별 에너지 분석 (십이운성)</h2>';
            for (const [period, analysis] of Object.entries(sibiunseongAnalysis)) {
                sibiunseongHtml += `
                    <h4>${period.replace('주', '운')}</h4>
                    <p>${analysis}</p>
                `;
            }
            sibiunseongSection.innerHTML = sibiunseongHtml;
        }

    } catch (error) {
        console.error('Error:', error);
        statusDiv.innerHTML = `분석 중 오류가 발생했습니다. (오류: ${error.message})`;
        iljuSection.innerHTML = "";
        wealthLuckSection.innerHTML = "";
        loveLuckSection.innerHTML = "";
        careerLuckSection.innerHTML = "";
        healthLuckSection.innerHTML = "";
        sipsungSection.innerHTML = "";
        sibiunseongSection.innerHTML = "";
    }
}
