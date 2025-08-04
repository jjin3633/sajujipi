async function getAnalysis() {
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    const hour = document.getElementById('hour').value;
    const minute = document.getElementById('minute').value;
    const resultDiv = document.getElementById('result');

    if (!year || !month || !day || !hour || !minute) {
        resultDiv.innerHTML = "모든 값을 입력해주세요.";
        return;
    }

    resultDiv.innerHTML = "분석 중입니다... 잠시만 기다려주세요.";

    try {
        const response = await fetch('http://127.0.0.1:8000/analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                year: parseInt(year),
                month: parseInt(month),
                day: parseInt(day),
                hour: parseInt(hour),
                minute: parseInt(minute)
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        const { title, description, pros, cons, animal } = data.analysis_result;

        resultDiv.innerHTML = `
            <h3>${title}</h3>
            <p>${description}</p>
            <h4>장점</h4>
            <ul>
                ${pros.map(pro => `<li>${pro}</li>`).join('')}
            </ul>
            <h4>단점</h4>
            <ul>
                ${cons.map(con => `<li>${con}</li>`).join('')}
            </ul>
            <h4>상징 동물</h4>
            <p>${animal}</p>
        `;

    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = `분석 중 오류가 발생했습니다. 서버가 실행 중인지 확인해주세요. (오류: ${error.message})`;
    }
}
