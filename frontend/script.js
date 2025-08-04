async function getAnalysis() {
    // 입력 값 가져오기
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    const hour = document.getElementById('hour').value;
    const minute = document.getElementById('minute').value;
    
    // HTML 요소 가져오기
    const statusDiv = document.getElementById('status-message');
    const iljuSection = document.getElementById('ilju-analysis-section');
    const sipsungSection = document.getElementById('sipsung-analysis-section');

    // 1. 이전 결과 및 상태 메시지 초기화
    iljuSection.innerHTML = "";
    sipsungSection.innerHTML = "";
    statusDiv.innerHTML = ""; 

    if (!year || !month || !day || !hour || !minute) {
        statusDiv.innerHTML = "모든 값을 입력해주세요.";
        return;
    }

    // 2. "분석 중" 상태 메시지 표시
    statusDiv.innerHTML = "분석 중입니다... 잠시만 기다려주세요.";

    try {
        const response = await fetch('http://127.0.0.1:8000/analysis', {
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

        // 5. 시기별 십성 분석 결과 표시
        const sipsungAnalysis = data.analysis_result.sipsung_analysis;
        if (sipsungAnalysis && !sipsungAnalysis.error) {
            let sipsungHtml = '<h2>시기별 성향 분석</h2>';
            for (const [period, analysis] of Object.entries(sipsungAnalysis)) {
                sipsungHtml += `
                    <h4>${period}</h4>
                    <p>${analysis}</p>
                `;
            }
            sipsungSection.innerHTML = sipsungHtml;
        }

    } catch (error) {
        console.error('Error:', error);
        // 오류 발생 시 상태 메시지에만 오류 표시
        statusDiv.innerHTML = `분석 중 오류가 발생했습니다. (오류: ${error.message})`;
        iljuSection.innerHTML = "";
        sipsungSection.innerHTML = "";
    }
}
