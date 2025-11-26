/**
 * Visibility Manager
 * Handles field-level visibility controls
 */

class VisibilityManager {
    constructor() {
        this.visibilityLevels = {
            'public': {
                label: 'Public',
                description: 'Visible to everyone',
                icon: '🌐'
            },
            'lateral_entrants_only': {
                label: 'Lateral Entrants Only',
                description: 'Only visible to other lateral entry officers',
                icon: '👥'
            },
            'private': {
                label: 'Private',
                description: 'Only visible to you and admins',
                icon: '🔒'
            }
        };
    }

    /**
     * Get current visibility settings for a profile
     */
    async getVisibilitySettings(entrantId) {
        try {
            const response = await authClient.api(`/api/profiles/${entrantId}/visibility`);
            const data = await response.json();

            if (data.success) {
                return data.settings;
            }

            throw new Error(data.error || 'Failed to load visibility settings');
        } catch (error) {
            console.error('Error loading visibility settings:', error);
            throw error;
        }
    }

    /**
     * Update visibility for a single field
     */
    async updateFieldVisibility(entrantId, fieldName, visibilityLevel) {
        try {
            const response = await authClient.api(`/api/profiles/${entrantId}/visibility/${fieldName}`, {
                method: 'PATCH',
                body: JSON.stringify({ visibility_level: visibilityLevel })
            });

            const data = await response.json();

            if (data.success) {
                return true;
            }

            throw new Error(data.error || 'Failed to update visibility');
        } catch (error) {
            console.error('Error updating visibility:', error);
            throw error;
        }
    }

    /**
     * Bulk update visibility settings
     */
    async bulkUpdateVisibility(entrantId, updates) {
        try {
            const response = await authClient.api(`/api/profiles/${entrantId}/visibility/bulk`, {
                method: 'PATCH',
                body: JSON.stringify({ updates })
            });

            const data = await response.json();

            if (data.success) {
                return true;
            }

            throw new Error(data.error || 'Failed to update visibility');
        } catch (error) {
            console.error('Error bulk updating visibility:', error);
            throw error;
        }
    }

    /**
     * Create visibility control dropdown
     */
    createVisibilityControl(fieldName, currentLevel = 'public') {
        const container = document.createElement('div');
        container.className = 'visibility-control';

        const select = document.createElement('select');
        select.className = 'px-2 py-1 border border-gray-300 rounded text-sm';
        select.dataset.field = fieldName;

        Object.entries(this.visibilityLevels).forEach(([level, config]) => {
            const option = document.createElement('option');
            option.value = level;
            option.textContent = `${config.icon} ${config.label}`;
            option.selected = level === currentLevel;
            select.appendChild(option);
        });

        container.appendChild(select);

        return container;
    }

    /**
     * Create visibility indicator (read-only)
     */
    createVisibilityIndicator(level) {
        const config = this.visibilityLevels[level] || this.visibilityLevels.public;

        const indicator = document.createElement('span');
        indicator.className = 'inline-flex items-center gap-1 px-2 py-1 text-xs rounded-full';

        if (level === 'public') {
            indicator.classList.add('bg-green-100', 'text-green-800');
        } else if (level === 'lateral_entrants_only') {
            indicator.classList.add('bg-blue-100', 'text-blue-800');
        } else {
            indicator.classList.add('bg-gray-100', 'text-gray-800');
        }

        indicator.innerHTML = `
            <span>${config.icon}</span>
            <span>${config.label}</span>
        `;

        indicator.title = config.description;

        return indicator;
    }

    /**
     * Render visibility settings form
     */
    renderVisibilitySettings(containerElement, entrantId, fields) {
        containerElement.innerHTML = '<p class="text-gray-500 text-center py-4">Loading visibility settings...</p>';

        this.getVisibilitySettings(entrantId).then(settings => {
            // Convert settings array to object for easier lookup
            const settingsMap = {};
            settings.forEach(s => {
                settingsMap[s.field_name] = s.visibility_level;
            });

            // Render controls for each field
            const html = `
                <div class="space-y-4">
                    <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                        <p class="text-sm text-blue-700">
                            Control who can see each field of your profile. Changes are saved automatically.
                        </p>
                    </div>

                    ${fields.map(field => `
                        <div class="flex items-center justify-between py-2 border-b border-gray-200">
                            <div>
                                <label class="font-medium text-gray-900">${field.label}</label>
                                ${field.description ? `<p class="text-xs text-gray-500">${field.description}</p>` : ''}
                            </div>
                            <div id="visibility-${field.name}"></div>
                        </div>
                    `).join('')}

                    <div class="flex gap-2 pt-4">
                        <button id="setAllPublic" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                            Make All Public
                        </button>
                        <button id="setAllPrivate" class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700">
                            Make All Private
                        </button>
                    </div>
                </div>
            `;

            containerElement.innerHTML = html;

            // Add controls for each field
            fields.forEach(field => {
                const controlContainer = document.getElementById(`visibility-${field.name}`);
                const control = this.createVisibilityControl(
                    field.name,
                    settingsMap[field.name] || 'public'
                );

                controlContainer.appendChild(control);

                // Add change handler
                control.querySelector('select').addEventListener('change', async (e) => {
                    const newLevel = e.target.value;
                    try {
                        await this.updateFieldVisibility(entrantId, field.name, newLevel);
                        // Show success feedback
                        e.target.classList.add('border-green-500');
                        setTimeout(() => e.target.classList.remove('border-green-500'), 1000);
                    } catch (error) {
                        alert('Failed to update visibility: ' + error.message);
                        e.target.value = settingsMap[field.name] || 'public'; // Revert
                    }
                });
            });

            // Bulk update buttons
            document.getElementById('setAllPublic').addEventListener('click', async () => {
                if (!confirm('Make all fields public?')) return;

                const updates = fields.map(f => ({
                    field_name: f.name,
                    visibility_level: 'public'
                }));

                try {
                    await this.bulkUpdateVisibility(entrantId, updates);
                    this.renderVisibilitySettings(containerElement, entrantId, fields); // Reload
                } catch (error) {
                    alert('Failed to update visibility: ' + error.message);
                }
            });

            document.getElementById('setAllPrivate').addEventListener('click', async () => {
                if (!confirm('Make all fields private?')) return;

                const updates = fields.map(f => ({
                    field_name: f.name,
                    visibility_level: 'private'
                }));

                try {
                    await this.bulkUpdateVisibility(entrantId, updates);
                    this.renderVisibilitySettings(containerElement, entrantId, fields); // Reload
                } catch (error) {
                    alert('Failed to update visibility: ' + error.message);
                }
            });
        }).catch(error => {
            containerElement.innerHTML = `<p class="text-red-500 text-center py-4">Error loading visibility settings: ${error.message}</p>`;
        });
    }
}

// Create global instance
window.visibilityManager = new VisibilityManager();
