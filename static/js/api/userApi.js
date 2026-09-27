// Запросы к API пользователей (анкет)
const UserApi = (() => {
    const BASE_URL = '/api/user';

    async function request(url, options = {}) {
        const response = await fetch(url, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });

        let body = null;
        try { body = await response.json(); } catch (_) { /* ignore */ }

        if (!response.ok) {
            const err = new Error(body?.detail || `HTTP ${response.status}`);
            err.status = response.status;
            err.detail = body?.detail;
            throw err;
        }
        return body;
    }

    return {
    
        save(payload) {
            return request(`${BASE_URL}/save`, {
                method: 'POST',
                body: JSON.stringify(payload)
            });
        }
    };
})();