document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('surveyForm');
    const messageContainer = document.getElementById('messageContainer');
    const submitBtn = document.getElementById('submitBtn');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        messageContainer.innerHTML = '';

        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        const payload = collectFormData(form);

        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';

        try {
            const result = await UserApi.save(payload);
            showMessage('success', 'Спасибо! Анкета успешно отправлена.');
            form.reset();
            form.classList.remove('was-validated');
        } catch (err) {
            console.error(err);
            const detail = err?.detail || err?.message || 'Не удалось отправить анкету. Попробуйте ещё раз.';
            showMessage('danger', detail);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Отправить анкету';
        }
    });

    function showMessage(type, text) {
        messageContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${escapeHtml(text)}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        messageContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});

/**
 * Собирает данные формы в объект, включая массивы чекбоксов.
 */
function collectFormData(form) {
    const data = {
        name: form.name.value.trim(),
        company: form.company.value.trim() || null,
        role: form.role.value || null,
        stand_interest: getCheckedValues(form, 'stand_interest'),
        directions: getCheckedValues(form, 'directions'),
        interest: getCheckedValues(form, 'interest'),
        phone: form.phone.value.trim(),
        email: form.email.value.trim(),
        followup: form.followup.value.trim() || null
    };
    return data;
}

function getCheckedValues(form, name) {
    return Array.from(form.querySelectorAll(`input[name="${name}"]:checked`))
        .map(el => el.value);
}