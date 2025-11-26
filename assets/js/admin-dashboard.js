/**
 * Admin Dashboard
 * Handles all admin functionality
 */

// Require admin auth
authClient.requireAdmin();

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(t => {
        t.classList.remove('tab-active');
        t.classList.add('text-gray-500', 'border-transparent');
    });

    const activeTab = document.querySelector(`[data-tab="${tabName}"]`);
    activeTab.classList.add('tab-active');
    activeTab.classList.remove('text-gray-500', 'border-transparent');

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });

    document.getElementById(`tab-${tabName}`).classList.remove('hidden');

    // Load data for the tab
    loadTabData(tabName);
}

function loadTabData(tabName) {
    switch (tabName) {
        case 'pending-users':
            loadPendingUsers();
            break;
        case 'users':
            loadAllUsers();
            break;
        case 'edits':
            loadFieldEdits();
            break;
        case 'uploads':
            loadUploads();
            break;
        case 'flagged':
            loadFlaggedContent();
            break;
        case 'settings':
            loadSettings();
            break;
        case 'audit':
            loadAuditLog();
            break;
    }
}

// ============================================================================
// Dashboard Stats
// ============================================================================

async function loadStats() {
    try {
        const response = await authClient.api('/api/admin/stats/dashboard');
        const data = await response.json();

        if (data.success) {
            document.getElementById('statPendingApprovals').textContent = data.stats.pending_approvals;
            document.getElementById('statTotalUsers').textContent = data.stats.total_users;
            document.getElementById('statPendingEdits').textContent = data.stats.pending_edits;
            document.getElementById('statPendingUploads').textContent = data.stats.pending_uploads;
            document.getElementById('statFlaggedContent').textContent = data.stats.flagged_content;
            document.getElementById('statRecentLogins').textContent = data.stats.recent_logins;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// ============================================================================
// Pending Users
// ============================================================================

async function loadPendingUsers() {
    const container = document.getElementById('pendingUsersList');
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading...</p>';

    try {
        const response = await authClient.api('/api/admin/users/pending');
        const data = await response.json();

        if (data.success && data.users.length > 0) {
            container.innerHTML = data.users.map(user => `
                <div class="border border-gray-200 rounded-lg p-4">
                    <div class="flex items-start justify-between">
                        <div class="flex items-center gap-4">
                            <img src="${user.picture_url || '/assets/images/default-avatar.png'}"
                                 alt="${user.name}" class="w-12 h-12 rounded-full">
                            <div>
                                <h3 class="font-semibold text-gray-900">${user.name}</h3>
                                <p class="text-sm text-gray-600">${user.email}</p>
                                <p class="text-xs text-gray-500 mt-1">
                                    Requested: ${new Date(user.requested_at).toLocaleString()}
                                </p>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="approveUser(${user.id})"
                                    class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
                                Approve
                            </button>
                            <button onclick="rejectUser(${user.id})"
                                    class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
                                Reject
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No pending user approvals</p>';
        }
    } catch (error) {
        console.error('Error loading pending users:', error);
        container.innerHTML = '<p class="text-red-500 text-center py-8">Error loading pending users</p>';
    }
}

async function approveUser(pendingId) {
    if (!confirm('Approve this user?')) return;

    try {
        const response = await authClient.api(`/api/admin/users/pending/${pendingId}/approve`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            alert('User approved successfully!');
            loadPendingUsers();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error approving user:', error);
        alert('Failed to approve user');
    }
}

async function rejectUser(pendingId) {
    const reason = prompt('Enter rejection reason (optional):');
    if (reason === null) return;

    try {
        const response = await authClient.api(`/api/admin/users/pending/${pendingId}/reject`, {
            method: 'POST',
            body: JSON.stringify({ reason })
        });

        const data = await response.json();

        if (data.success) {
            alert('User rejected');
            loadPendingUsers();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error rejecting user:', error);
        alert('Failed to reject user');
    }
}

// ============================================================================
// All Users
// ============================================================================

async function loadAllUsers(search = '') {
    const container = document.getElementById('usersList');
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading...</p>';

    try {
        const response = await authClient.api(`/api/admin/users?search=${encodeURIComponent(search)}`);
        const data = await response.json();

        if (data.success && data.users.length > 0) {
            container.innerHTML = data.users.map(user => `
                <div class="border border-gray-200 rounded-lg p-4">
                    <div class="flex items-start justify-between">
                        <div class="flex items-center gap-4">
                            <img src="${user.picture_url || '/assets/images/default-avatar.png'}"
                                 alt="${user.name}" class="w-12 h-12 rounded-full">
                            <div>
                                <h3 class="font-semibold text-gray-900">${user.name}</h3>
                                <p class="text-sm text-gray-600">${user.email}</p>
                                <div class="flex gap-2 mt-1">
                                    <span class="badge ${user.role === 'admin' ? 'badge-blue' : 'badge-green'}">
                                        ${user.role}
                                    </span>
                                    <span class="badge ${user.is_active ? 'badge-green' : 'badge-red'}">
                                        ${user.is_active ? 'Active' : 'Inactive'}
                                    </span>
                                    ${user.entrant_name ? `<span class="badge badge-blue">${user.entrant_name}</span>` : ''}
                                </div>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="toggleUserStatus(${user.id}, ${!user.is_active})"
                                    class="px-3 py-1 text-sm ${user.is_active ? 'bg-red-100 text-red-600 hover:bg-red-200' : 'bg-green-100 text-green-600 hover:bg-green-200'} rounded">
                                ${user.is_active ? 'Deactivate' : 'Activate'}
                            </button>
                            <button onclick="deleteUser(${user.id})"
                                    class="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700">
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No users found</p>';
        }
    } catch (error) {
        console.error('Error loading users:', error);
        container.innerHTML = '<p class="text-red-500 text-center py-8">Error loading users</p>';
    }
}

async function toggleUserStatus(userId, activate) {
    try {
        const response = await authClient.api(`/api/admin/users/${userId}`, {
            method: 'PATCH',
            body: JSON.stringify({ is_active: activate })
        });

        const data = await response.json();

        if (data.success) {
            loadAllUsers();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error updating user:', error);
        alert('Failed to update user');
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) return;

    try {
        const response = await authClient.api(`/api/admin/users/${userId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            alert('User deleted successfully');
            loadAllUsers();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        alert('Failed to delete user');
    }
}

// Search functionality
document.getElementById('userSearch')?.addEventListener('input', (e) => {
    const search = e.target.value;
    clearTimeout(window.userSearchTimeout);
    window.userSearchTimeout = setTimeout(() => loadAllUsers(search), 300);
});

// ============================================================================
// Field Edits
// ============================================================================

async function loadFieldEdits() {
    const container = document.getElementById('fieldEditsList');
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading...</p>';

    try {
        const response = await authClient.api('/api/admin/moderation/field-edits');
        const data = await response.json();

        if (data.success && data.requests.length > 0) {
            container.innerHTML = data.requests.map(req => `
                <div class="border border-gray-200 rounded-lg p-4">
                    <div class="flex items-start justify-between mb-3">
                        <div>
                            <h3 class="font-semibold text-gray-900">${req.user_name}</h3>
                            <p class="text-sm text-gray-600">${req.entrant_name || 'Profile Edit'}</p>
                            <p class="text-xs text-gray-500">${new Date(req.created_at).toLocaleString()}</p>
                        </div>
                        <span class="badge badge-yellow">Pending</span>
                    </div>
                    <div class="bg-gray-50 rounded p-3 mb-3">
                        <p class="text-sm font-medium text-gray-700 mb-1">Field: ${req.field_name}</p>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <p class="text-xs text-gray-500 mb-1">Old Value:</p>
                                <p class="text-sm text-gray-900">${req.old_value || '<em>Empty</em>'}</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-500 mb-1">New Value:</p>
                                <p class="text-sm text-gray-900 font-semibold">${req.new_value}</p>
                            </div>
                        </div>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="approveFieldEdit(${req.id})"
                                class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
                            Approve
                        </button>
                        <button onclick="rejectFieldEdit(${req.id})"
                                class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
                            Reject
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No pending field edits</p>';
        }
    } catch (error) {
        console.error('Error loading field edits:', error);
        container.innerHTML = '<p class="text-red-500 text-center py-8">Error loading field edits</p>';
    }
}

async function approveFieldEdit(requestId) {
    try {
        const response = await authClient.api(`/api/admin/moderation/field-edits/${requestId}/approve`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            alert('Edit approved and applied');
            loadFieldEdits();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error approving edit:', error);
        alert('Failed to approve edit');
    }
}

async function rejectFieldEdit(requestId) {
    const reason = prompt('Enter rejection reason:');
    if (!reason) return;

    try {
        const response = await authClient.api(`/api/admin/moderation/field-edits/${requestId}/reject`, {
            method: 'POST',
            body: JSON.stringify({ reason })
        });

        const data = await response.json();

        if (data.success) {
            alert('Edit rejected');
            loadFieldEdits();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error rejecting edit:', error);
        alert('Failed to reject edit');
    }
}

// ============================================================================
// Uploads
// ============================================================================

async function loadUploads() {
    const container = document.getElementById('uploadsList');
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading...</p>';

    try {
        const response = await authClient.api('/api/admin/moderation/uploads');
        const data = await response.json();

        if (data.success && data.uploads.length > 0) {
            container.innerHTML = data.uploads.map(upload => `
                <div class="border border-gray-200 rounded-lg p-4">
                    <div class="flex items-start gap-4">
                        ${upload.file_type.startsWith('image/') ?
                            `<img src="${upload.file_path}" class="w-32 h-32 object-cover rounded" alt="Upload">` :
                            `<div class="w-32 h-32 bg-gray-100 rounded flex items-center justify-center">
                                <svg class="w-12 h-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/>
                                </svg>
                            </div>`
                        }
                        <div class="flex-1">
                            <h3 class="font-semibold text-gray-900">${upload.user_name}</h3>
                            <p class="text-sm text-gray-600">${upload.file_type} - ${upload.purpose}</p>
                            <p class="text-xs text-gray-500">${new Date(upload.uploaded_at).toLocaleString()}</p>
                            <div class="flex gap-2 mt-3">
                                <button onclick="approveUpload(${upload.id})"
                                        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                                    Approve
                                </button>
                                <button onclick="rejectUpload(${upload.id})"
                                        class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                                    Reject
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No pending uploads</p>';
        }
    } catch (error) {
        console.error('Error loading uploads:', error);
        container.innerHTML = '<p class="text-red-500 text-center py-8">Error loading uploads</p>';
    }
}

async function approveUpload(uploadId) {
    try {
        const response = await authClient.api(`/api/admin/moderation/uploads/${uploadId}/approve`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            alert('Upload approved');
            loadUploads();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error approving upload:', error);
        alert('Failed to approve upload');
    }
}

async function rejectUpload(uploadId) {
    const reason = prompt('Enter rejection reason:');
    if (!reason) return;

    try {
        const response = await authClient.api(`/api/admin/moderation/uploads/${uploadId}/reject`, {
            method: 'POST',
            body: JSON.stringify({ reason })
        });

        const data = await response.json();

        if (data.success) {
            alert('Upload rejected');
            loadUploads();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error rejecting upload:', error);
        alert('Failed to reject upload');
    }
}

// ============================================================================
// Flagged Content
// ============================================================================

async function loadFlaggedContent() {
    const container = document.getElementById('flaggedContentList');
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading...</p>';

    try {
        const response = await authClient.api('/api/admin/moderation/flagged-content');
        const data = await response.json();

        if (data.success && data.flagged.length > 0) {
            container.innerHTML = data.flagged.map(flag => `
                <div class="border border-red-200 bg-red-50 rounded-lg p-4">
                    <div class="flex items-start justify-between mb-3">
                        <div>
                            <h3 class="font-semibold text-gray-900">Reported by: ${flag.reporter_name}</h3>
                            <p class="text-sm text-gray-600">${new Date(flag.reported_at).toLocaleString()}</p>
                        </div>
                        <span class="badge badge-red">Flagged</span>
                    </div>
                    <div class="bg-white rounded p-3 mb-3">
                        <p class="text-sm text-gray-700"><strong>Type:</strong> ${flag.content_type}</p>
                        <p class="text-sm text-gray-700 mt-1"><strong>Reason:</strong> ${flag.reason}</p>
                        ${flag.details ? `<p class="text-sm text-gray-600 mt-1">${flag.details}</p>` : ''}
                    </div>
                    <div class="flex gap-2">
                        <button onclick="resolveFlagged(${flag.id}, 'remove')"
                                class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                            Remove Content
                        </button>
                        <button onclick="resolveFlagged(${flag.id}, 'keep')"
                                class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                            Keep Content
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No flagged content</p>';
        }
    } catch (error) {
        console.error('Error loading flagged content:', error);
        container.innerHTML = '<p class="text-red-500 text-center py-8">Error loading flagged content</p>';
    }
}

async function resolveFlagged(flagId, action) {
    const notes = prompt('Add admin notes (optional):');
    if (notes === null) return;

    try {
        const response = await authClient.api(`/api/admin/moderation/flagged-content/${flagId}/resolve`, {
            method: 'POST',
            body: JSON.stringify({ action, notes })
        });

        const data = await response.json();

        if (data.success) {
            alert('Flagged content resolved');
            loadFlaggedContent();
            loadStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error resolving flagged content:', error);
        alert('Failed to resolve flagged content');
    }
}

// ============================================================================
// Settings
// ============================================================================

async function loadSettings() {
    const container = document.getElementById('settingsList');
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading...</p>';

    try {
        const response = await authClient.api('/api/admin/settings');
        const data = await response.json();

        if (data.success && data.settings.length > 0) {
            // Group settings by category
            const grouped = {};
            data.settings.forEach(setting => {
                const category = setting.setting_key.split('_')[0];
                if (!grouped[category]) grouped[category] = [];
                grouped[category].push(setting);
            });

            container.innerHTML = Object.entries(grouped).map(([category, settings]) => `
                <div class="border border-gray-200 rounded-lg p-4">
                    <h3 class="font-semibold text-gray-900 mb-3 capitalize">${category} Settings</h3>
                    <div class="space-y-3">
                        ${settings.map(setting => `
                            <div class="flex items-center justify-between">
                                <div class="flex-1">
                                    <label class="text-sm font-medium text-gray-700">
                                        ${setting.setting_key.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase())}
                                    </label>
                                    ${setting.description ? `<p class="text-xs text-gray-500">${setting.description}</p>` : ''}
                                </div>
                                <input type="text"
                                       value="${setting.setting_value}"
                                       onchange="updateSetting('${setting.setting_key}', this.value)"
                                       class="w-32 px-3 py-2 border border-gray-300 rounded">
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No settings found</p>';
        }
    } catch (error) {
        console.error('Error loading settings:', error);
        container.innerHTML = '<p class="text-red-500 text-center py-8">Error loading settings</p>';
    }
}

async function updateSetting(key, value) {
    try {
        const response = await authClient.api(`/api/admin/settings/${key}`, {
            method: 'PATCH',
            body: JSON.stringify({ value })
        });

        const data = await response.json();

        if (data.success) {
            // Success feedback
        } else {
            alert('Error: ' + data.error);
            loadSettings(); // Reload to reset value
        }
    } catch (error) {
        console.error('Error updating setting:', error);
        alert('Failed to update setting');
        loadSettings();
    }
}

// ============================================================================
// Audit Log
// ============================================================================

async function loadAuditLog() {
    const container = document.getElementById('auditLogList');
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading...</p>';

    try {
        const response = await authClient.api('/api/admin/audit-log');
        const data = await response.json();

        if (data.success && data.logs.length > 0) {
            container.innerHTML = `
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Entity</th>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Details</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            ${data.logs.map(log => `
                                <tr>
                                    <td class="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">
                                        ${new Date(log.created_at).toLocaleString()}
                                    </td>
                                    <td class="px-4 py-3 text-sm text-gray-900">
                                        ${log.user_name}
                                    </td>
                                    <td class="px-4 py-3 text-sm">
                                        <span class="badge badge-blue">${log.action}</span>
                                    </td>
                                    <td class="px-4 py-3 text-sm text-gray-900">
                                        ${log.entity_type}
                                    </td>
                                    <td class="px-4 py-3 text-sm text-gray-600">
                                        ${log.new_value || '-'}
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } else {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No audit log entries</p>';
        }
    } catch (error) {
        console.error('Error loading audit log:', error);
        container.innerHTML = '<p class="text-red-500 text-center py-8">Error loading audit log</p>';
    }
}

// ============================================================================
// Initialize
// ============================================================================

// Load admin name
authClient.init().then(() => {
    if (authClient.currentUser) {
        document.getElementById('adminName').textContent = authClient.currentUser.name;
    }
});

// Load initial data
loadStats();
loadPendingUsers();

// Auto-refresh stats every 30 seconds
setInterval(loadStats, 30000);

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    authClient.logout();
});
