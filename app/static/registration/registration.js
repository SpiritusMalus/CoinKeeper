const emailInput = document.getElementById('reg-email');
const passwordInput = document.getElementById('reg-password');
const repeatPasswordInput = document.getElementById('repeat-reg-password');
const submitButton = document.getElementById('reg-submit');


function validatePassword() {
    const password = passwordInput.value;
    const errors = [];

    // Минимальная длина
    if (password.length < 8) {
        errors.push('Пароль должен содержать минимум 8 символов');
    }

    // Проверка на цифры
    if (!/\d/.test(password)) {
        errors.push('Добавьте хотя бы одну цифру');
    }

    // Проверка на заглавные буквы
    if (!/[A-Z]/.test(password)) {
        errors.push('Добавьте хотя бы одну заглавную букву');
    }

    // Проверка на строчные буквы
    if (!/[a-z]/.test(password)) {
        errors.push('Добавьте хотя бы одну строчную букву');
    }

    // Проверка на специальные символы
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
        errors.push('Добавьте хотя бы один специальный символ');
    }

    // Проверка на пробелы
    if (/\s/.test(password)) {
        errors.push('Пароль не должен содержать пробелов');
    }
   
    return errors;
}

function isValidEmail() {
    const regex = /^\S+@\S+\.\S+$/;
    return regex.test(emailInput.value);
}

function showEmailError() {
    const errorDiv = document.getElementById('email-error');

    errorDiv.innerHTML = isValidEmail()
        ?  ''
        : '<div style="color: red; margin: 5px 0;">• Email не соответствует стандарту example@example.com</div>';
}

function isValidRepeatPassword() {
    return passwordInput.value === repeatPasswordInput.value;
}

function showPassErrors(errors) {
    const errorsDiv = document.getElementById('pass-error');

    errorsDiv.innerHTML = errors.map(error => 
        `<div style="color: red; margin: 5px 0;">• ${error}</div>`
    ).join('');
}

function showRepeatPassError() {
    const errorDiv = document.getElementById('repeat-pass-error');

    errorDiv.innerHTML = isValidRepeatPassword()
        ?  ''
        : '<div style="color: red; margin: 5px 0;">• Пароли должны совпадать</div>';
}

submitButton.addEventListener('click', function(event) {
    const passErrors = validatePassword();
    if (Boolean(passErrors.length) || !isValidRepeatPassword()){
        event.preventDefault();
        showPassErrors(passErrors);
        showRepeatPassError();
        showEmailError();
    }
    
});

passwordInput.addEventListener('input', () => {
    showPassErrors(validatePassword());
});

repeatPasswordInput.addEventListener('input', () => {
    showRepeatPassError();
});

emailInput.addEventListener('input', () => {
    showEmailError();
});