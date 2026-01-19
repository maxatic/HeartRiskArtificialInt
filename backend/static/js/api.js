/**
 * Shared API utility for making authenticated requests with auto-refresh logic.
 */

async function authenticatedFetch(url, options = {}) {
    let accessToken = localStorage.getItem('accessToken');

    // Merge headers, ensuring Content-Type is set if not provided (optional, typically good for JSON)
    // But be careful with FormData (which shouldn't have Content-Type manually set).
    // Let's safe-guard simple options.

    const headers = options.headers || {};
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    // Default config
    const config = {
        ...options,
        headers: headers
    };

    let response = await fetch(url, config);

    // If Access Token expired (401), try to refresh
    if (response.status === 401) {
        console.log("Access token expired. Attempting refresh...");
        const refreshToken = localStorage.getItem('refreshToken');

        if (!refreshToken) {
            window.location.href = '/auth/';
            return response;
        }

        try {
            const refreshResponse = await fetch('/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (refreshResponse.ok) {
                const data = await refreshResponse.json();
                console.log("Token refreshed successfully.");

                // 1. Save new access token
                localStorage.setItem('accessToken', data.access);

                // 2. Retry original request with new token
                config.headers['Authorization'] = `Bearer ${data.access}`;
                response = await fetch(url, config);

            } else {
                console.warn("Refresh token expired or invalid.");
                // Clear invalid tokens to prevent infinite loops or stale state
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                window.location.href = '/auth/';
            }
        } catch (error) {
            console.error("Error refreshing token:", error);
            window.location.href = '/auth/';
        }
    }

    return response;
}
