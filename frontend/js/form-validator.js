// 폼 유효성 검사 모듈
export class FormValidator {
    validate(birthData) {
        // 모든 필드가 입력되었는지 확인
        if (!birthData.year || !birthData.month || !birthData.day || !birthData.hour || !birthData.minute) {
            return {
                isValid: false,
                message: '모든 생년월일 정보를 입력해주세요.'
            };
        }
        
        // 숫자 형식 검사
        const year = parseInt(birthData.year);
        const month = parseInt(birthData.month);
        const day = parseInt(birthData.day);
        const hour = parseInt(birthData.hour);
        const minute = parseInt(birthData.minute);
        
        if (isNaN(year) || isNaN(month) || isNaN(day) || isNaN(hour) || isNaN(minute)) {
            return {
                isValid: false,
                message: '올바른 숫자 형식으로 입력해주세요.'
            };
        }
        
        // 연도 범위 검사 (1900년 ~ 현재 연도)
        const currentYear = new Date().getFullYear();
        if (year < 1900 || year > currentYear) {
            return {
                isValid: false,
                message: `연도는 1900년부터 ${currentYear}년 사이로 입력해주세요.`
            };
        }
        
        // 월 범위 검사
        if (month < 1 || month > 12) {
            return {
                isValid: false,
                message: '월은 1부터 12 사이로 입력해주세요.'
            };
        }
        
        // 일 범위 검사
        const maxDays = this.getDaysInMonth(year, month);
        if (day < 1 || day > maxDays) {
            return {
                isValid: false,
                message: `${month}월은 1일부터 ${maxDays}일까지입니다.`
            };
        }
        
        // 시간 범위 검사
        if (hour < 0 || hour > 23) {
            return {
                isValid: false,
                message: '시간은 0부터 23 사이로 입력해주세요.'
            };
        }
        
        // 분 범위 검사
        if (minute < 0 || minute > 59) {
            return {
                isValid: false,
                message: '분은 0부터 59 사이로 입력해주세요.'
            };
        }
        
        return { isValid: true };
    }
    
    getDaysInMonth(year, month) {
        return new Date(year, month, 0).getDate();
    }
}