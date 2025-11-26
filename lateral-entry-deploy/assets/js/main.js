/**
 * Main JavaScript for Lateral Entry Portal
 * Handles API calls, navigation, and common functionality
 */

// API Base URL - auto-detect or fallback to static files
// For production (prabhu.app), we don't have an API server, so we use static JSON
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : null; // Force static fallback for production

// Determine base path for static files (handles subdirectory deployments)
const BASE_PATH = window.location.pathname.includes('/lateral-entry/') 
    ? '/lateral-entry/' 
    : '/';

// Log configuration on startup
console.log('=== Lateral Entry Portal Configuration ===');
console.log('Hostname:', window.location.hostname);
console.log('API URL:', API_BASE_URL || 'Using static JSON files');
console.log('Base Path:', BASE_PATH);
console.log('==========================================');

// API Helper Functions
const API = {
    // Flag to track if we should use static files
    useStaticFallback: false,
    
    async get(endpoint) {
        // If API_BASE_URL is null (production), use static files directly
        if (!API_BASE_URL || this.useStaticFallback) {
            return await this.getStatic(endpoint);
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.warn(`API unavailable (${endpoint}), falling back to static files:`, error.message);
            this.useStaticFallback = true;
            return await this.getStatic(endpoint);
        }
    },
    
    async getStatic(endpoint) {
        try {
            // Map API endpoints to static JSON files
            let staticFile = null;
            
            if (endpoint === '/stats') {
                staticFile = `${BASE_PATH}data/stats.json`;
            } else if (endpoint === '/batches') {
                staticFile = `${BASE_PATH}data/batches.json`;
            } else if (endpoint.startsWith('/batches/')) {
                // For batch detail, we'll fetch entrants and filter
                const year = parseInt(endpoint.split('/')[2]);
                return await this.getBatchDetailStatic(year);
            } else if (endpoint.startsWith('/entrants')) {
                staticFile = `${BASE_PATH}data/entrants.json`;
            }
            
            if (!staticFile) {
                console.error(`No static fallback for endpoint: ${endpoint}`);
                return null;
            }
            
            console.log(`Loading static file: ${staticFile}`);
            const response = await fetch(staticFile);
            if (!response.ok) {
                console.error(`Static file load failed: ${staticFile} - Status: ${response.status}`);
                throw new Error(`Static file not found: ${staticFile}`);
            }
            let data = await response.json();
            console.log(`Static file loaded successfully: ${staticFile}`, data);
            
            // For entrants endpoint, ensure consistent format
            if (endpoint.startsWith('/entrants') && Array.isArray(data)) {
                // If it's an array, wrap it in an object for consistency
                // But also support limit parameter for recent appointments
                const params = new URLSearchParams(endpoint.split('?')[1] || '');
                const limit = params.get('limit');
                const entrants = limit ? data.slice(0, parseInt(limit)) : data;
                return entrants; // Return array directly as expected by most callers
            }
            
            return data;
        } catch (error) {
            console.error(`Static fallback failed (${endpoint}):`, error);
            return null;
        }
    },
    
    async getBatchDetailStatic(year) {
        try {
            // Load entrants.json and filter by year
            const response = await fetch(`${BASE_PATH}data/entrants.json`);
            if (!response.ok) throw new Error('Failed to load entrants.json');
            let data = await response.json();
            
            // Handle both array and object formats
            const allEntrants = Array.isArray(data) ? data : (data.entrants || []);
            const entrants = allEntrants.filter(e => e.batch_year === year);
            
            if (entrants.length === 0) {
                return null;
            }
            
            // Calculate statistics
            const ministries = new Set(entrants.map(e => e.ministry).filter(Boolean));
            const positions = new Set(entrants.map(e => e.position).filter(Boolean));
            
            // Group by position
            const byPosition = {};
            entrants.forEach(e => {
                byPosition[e.position] = (byPosition[e.position] || 0) + 1;
            });
            
            return {
                batch_year: year,
                statistics: {
                    total: entrants.length,
                    ministries: ministries.size,
                    positions: positions.size
                },
                by_position: Object.entries(byPosition).map(([position, count]) => ({
                    position,
                    count
                })),
                entrants: entrants
            };
        } catch (error) {
            console.error(`Failed to generate batch detail for ${year}:`, error);
            return null;
        }
    },
    
    stats: async () => {
        return await API.get('/stats');
    },
    
    entrants: async (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return await API.get(`/entrants${query ? '?' + query : ''}`);
    },
    
    entrant: async (id) => {
        return await API.get(`/entrants/${id}`);
    },
    
    batches: async () => {
        return await API.get('/batches');
    },
    
    batch: async (year) => {
        return await API.get(`/batches/${year}`);
    },
    
    ministries: async () => {
        return await API.get('/ministries');
    },
    
    positions: async () => {
        return await API.get('/positions');
    },
    
    search: async (query) => {
        return await API.get(`/search?q=${encodeURIComponent(query)}`);
    },
    
    timeline: async () => {
        return await API.get('/timeline');
    },
};

// Format date helper
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' });
}

// Number formatting
function formatNumber(num) {
    return new Intl.NumberFormat('en-IN').format(num);
}

// Show loading state
function showLoading(element) {
    element.innerHTML = `
        <div class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
    `;
}

// Show error message
function showError(element, message) {
    element.innerHTML = `
        <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
            <i class="fas fa-exclamation-triangle text-red-500 text-2xl mb-2"></i>
            <p class="text-red-700">${message}</p>
        </div>
    `;
}

// Mobile navigation handler
function initMobileNav() {
    const mobileNav = document.getElementById('mobile-nav');
    if (!mobileNav) return;
    
    const navItems = mobileNav.querySelectorAll('[data-page]');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    navItems.forEach(item => {
        const page = item.getAttribute('data-page');
        if (currentPage === page || (currentPage === '' && page === 'index.html')) {
            item.classList.add('text-blue-600');
            item.querySelector('i').classList.add('text-blue-600');
        }
        
        item.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = page;
        });
    });
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    
    if (!searchInput || !searchBtn) return;
    
    const performSearch = async () => {
        const query = searchInput.value.trim();
        if (!query) return;
        
        // Redirect to profiles page with search query (only from index.html)
        window.location.href = `./pages/profiles.html?search=${encodeURIComponent(query)}`;
    };
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
}

// Create entrant card
function createEntrantCard(entrant) {
    // Determine correct path based on current location
    const isInPagesDir = window.location.pathname.includes('/pages/');
    const profileLink = isInPagesDir 
        ? `./profile-detail.html?id=${entrant.id}`
        : `./pages/profile-detail.html?id=${entrant.id}`;
    
    // Function to check if ministry and department are essentially the same
    function shouldShowDepartment(ministry, department) {
        if (!ministry || !department) return true;
        ministry = ministry.toLowerCase().trim();
        department = department.toLowerCase().trim();
        
        // Exact same
        if (ministry === department) return false;
        
        // Department is just ministry with suffix
        if (department === ministry || 
            department.startsWith(ministry) ||
            ministry.startsWith(department)) {
            return false;
        }
        
        return true;
    }
    
    const showDepartment = shouldShowDepartment(entrant.ministry, entrant.department);
    
    return `
        <div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden">
            <div class="p-5">
                <div class="flex items-start justify-between mb-3">
                    <div>
                        <h3 class="text-lg font-semibold text-gray-900 mb-1">${entrant.name}</h3>
                        <p class="text-sm text-blue-600 font-medium">${entrant.position}</p>
                    </div>
                    <span class="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-full">
                        ${entrant.batch_year}
                    </span>
                </div>
                
                <div class="space-y-2 mb-4">
                    <div class="flex items-start text-sm text-gray-600">
                        <i class="fas fa-building w-5 mr-2 mt-0.5 text-gray-400"></i>
                        <span>${entrant.ministry || 'N/A'}</span>
                    </div>
                    ${showDepartment ? `
                    <div class="flex items-start text-sm text-gray-600">
                        <i class="fas fa-briefcase w-5 mr-2 mt-0.5 text-gray-400"></i>
                        <span>${entrant.department || 'N/A'}</span>
                    </div>
                    ` : ''}
                    ${entrant.date_of_appointment ? `
                    <div class="flex items-start text-sm text-gray-600">
                        <i class="fas fa-calendar w-5 mr-2 mt-0.5 text-gray-400"></i>
                        <span>Appointed: ${formatDate(entrant.date_of_appointment)}</span>
                    </div>
                    ` : ''}
                </div>
                
                <a href="${profileLink}" 
                   class="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200">
                    View Profile
                </a>
            </div>
        </div>
    `;
}

// Create stats card
function createStatsCard(icon, label, value, color = 'blue') {
    return `
        <div class="bg-white rounded-lg shadow-md p-5 hover:shadow-lg transition-shadow duration-300">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-gray-600 mb-1">${label}</p>
                    <p class="text-3xl font-bold text-gray-900">${formatNumber(value)}</p>
                </div>
                <div class="bg-${color}-100 p-3 rounded-full">
                    <i class="fas fa-${icon} text-${color}-600 text-2xl"></i>
                </div>
            </div>
        </div>
    `;
}

// Create batch card
function createBatchCard(batch) {
    return `
        <a href="./pages/batch-${batch.batch_year}.html" 
           class="block bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
            <div class="p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-2xl font-bold text-gray-900">Batch ${batch.batch_year}</h3>
                    <span class="px-4 py-2 bg-blue-100 text-blue-700 text-lg font-semibold rounded-full">
                        ${batch.count} ${batch.count === 1 ? 'Person' : 'People'}
                    </span>
                </div>
                <div class="text-gray-600">
                    <i class="fas fa-arrow-right text-blue-600"></i>
                    <span class="ml-2">View Details</span>
                </div>
            </div>
        </a>
    `;
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initSearch();
});

// Export for use in other modules
window.LateralEntry = {
    API,
    formatDate,
    formatNumber,
    showLoading,
    showError,
    createEntrantCard,
    createStatsCard,
    createBatchCard,
};
