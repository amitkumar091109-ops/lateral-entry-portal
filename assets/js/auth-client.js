/**
 * Authentication Client
 * Handles frontend authentication state and API calls
 */

class AuthClient {
    constructor() {
        this.currentUser = null;
        this.initialized = false;
    }

    /**
     * Initialize auth client and check current session
     */
    async init() {
        if (this.initialized) return;

        try {
            const user = await this.getCurrentUser();
            this.currentUser = user;
            this.initialized = true;

            // Emit custom event for other components
            window.dispatchEvent(new CustomEvent('auth:initialized', {
                detail: { user: this.currentUser }
            }));

            return user;
        } catch (error) {
            console.error('Auth initialization error:', error);
            this.initialized = true;
            return null;
        }
    }

    /**
     * Get current authenticated user
     * @returns {Promise<Object|null>} User object or null if not authenticated
     */
    async getCurrentUser() {
        try {
            const response = await fetch('/api/auth/me', {
                credentials: 'include'
            });

            if (response.ok) {
                const user = await response.json();
                this.currentUser = user;
                return user;
            }

            this.currentUser = null;
            return null;
        } catch (error) {
            console.error('Get current user error:', error);
            this.currentUser = null;
            return null;
        }
    }

    /**
     * Check if user is authenticated
     * @returns {boolean}
     */
    isAuthenticated() {
        return this.currentUser !== null;
    }

    /**
     * Check if user is admin
     * @returns {boolean}
     */
    isAdmin() {
        return this.currentUser?.role === 'admin';
    }

    /**
     * Check if user is approved
     * @returns {boolean}
     */
    isApproved() {
        return this.currentUser?.is_approved === true;
    }

    /**
     * Initiate Google OAuth login
     */
    async login() {
        try {
            window.location.href = '/api/auth/google/login';
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    /**
     * Logout current user
     */
    async logout() {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                this.currentUser = null;

                // Emit logout event
                window.dispatchEvent(new CustomEvent('auth:logout'));

                // Redirect to home
                window.location.href = '/';
            } else {
                throw new Error('Logout failed');
            }
        } catch (error) {
            console.error('Logout error:', error);
            throw error;
        }
    }

    /**
     * Get approval status for pending users
     * @returns {Promise<Object>} Status object
     */
    async getApprovalStatus() {
        try {
            const response = await fetch('/api/auth/status', {
                credentials: 'include'
            });

            if (response.ok) {
                return await response.json();
            }

            throw new Error('Failed to get approval status');
        } catch (error) {
            console.error('Get approval status error:', error);
            throw error;
        }
    }

    /**
     * Require authentication - redirect to login if not authenticated
     * @param {boolean} requireApproval - Also require user to be approved
     */
    async requireAuth(requireApproval = true) {
        if (!this.initialized) {
            await this.init();
        }

        if (!this.isAuthenticated()) {
            // Store intended destination
            sessionStorage.setItem('auth_redirect', window.location.pathname);
            window.location.href = '/pages/login.html';
            return false;
        }

        if (requireApproval && !this.isApproved()) {
            window.location.href = '/pages/pending-approval.html';
            return false;
        }

        return true;
    }

    /**
     * Require admin role - redirect if not admin
     */
    async requireAdmin() {
        const hasAuth = await this.requireAuth(true);
        if (!hasAuth) return false;

        if (!this.isAdmin()) {
            window.location.href = '/pages/forbidden.html';
            return false;
        }

        return true;
    }

    /**
     * Get authentication headers for API calls
     * @returns {Object} Headers object
     */
    getHeaders() {
        return {
            'Content-Type': 'application/json'
        };
    }

    /**
     * Make authenticated API call
     * @param {string} url - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<Response>}
     */
    async api(url, options = {}) {
        const defaultOptions = {
            credentials: 'include',
            headers: this.getHeaders()
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...(options.headers || {})
            }
        };

        try {
            const response = await fetch(url, mergedOptions);

            // Handle 401 Unauthorized
            if (response.status === 401) {
                this.currentUser = null;
                window.dispatchEvent(new CustomEvent('auth:unauthorized'));

                // Redirect to login for non-public pages
                if (!window.location.pathname.startsWith('/pages/login')) {
                    sessionStorage.setItem('auth_redirect', window.location.pathname);
                    window.location.href = '/pages/login.html';
                }
            }

            // Handle 403 Forbidden
            if (response.status === 403) {
                const data = await response.json();

                // Check if pending approval
                if (data.error?.includes('pending approval')) {
                    window.location.href = '/pages/pending-approval.html';
                } else {
                    window.location.href = '/pages/forbidden.html';
                }
            }

            return response;
        } catch (error) {
            console.error('API call error:', error);
            throw error;
        }
    }
}

// Create global auth client instance
const authClient = new AuthClient();

// Auto-initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        authClient.init();
    });
} else {
    authClient.init();
}

// Export for use in other scripts
window.authClient = authClient;
