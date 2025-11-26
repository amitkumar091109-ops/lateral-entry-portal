# Capability Spec: Upload Moderation

**Feature**: `upload-moderation`  
**Parent Change**: `add-user-profiles-and-feeds`  
**Status**: Draft

## Overview

Implement a moderation system where all user-uploaded files (photos and documents) are reviewed and approved by administrators before becoming publicly visible.

## Requirements

### Functional Requirements

1. **Upload Submission**:
   - User uploads photo or document
   - File goes to moderation queue
   - User sees "pending approval" status
   - User can see their pending uploads
   - User can delete pending uploads

2. **Moderation Queue**:
   - Admin sees list of pending uploads
   - Admin can view upload preview
   - Admin can approve upload (makes it public)
   - Admin can reject upload with reason
   - Admin can see upload metadata (size, dimensions, uploader)

3. **Status Tracking**:
   - Pending: Awaiting admin review
   - Approved: Published and visible to public
   - Rejected: Not published, user can see reason
   - Deleted: User removed before approval

4. **Notifications**:
   - User notified when upload approved
   - User notified when upload rejected with reason
   - Admin notified of new uploads (optional email)

### Non-Functional Requirements

1. **Performance**:
   - Moderation queue loads in < 2 seconds
   - Approve/reject action completes in < 500ms
   - Preview images load in < 1 second

2. **Usability**:
   - Clear moderation interface
   - Easy approve/reject actions
   - Bulk actions for multiple uploads
   - Filter by upload type, user, date

3. **Security**:
   - Only admins can access moderation queue
   - Audit log of all moderation actions
   - Rejected uploads stored for review

## Technical Specification

### API Endpoints

```
# User endpoints
GET    /api/uploads/pending         - Get own pending uploads
POST   /api/uploads/photo           - Upload photo
POST   /api/uploads/document        - Upload document
DELETE /api/uploads/:id             - Delete own pending upload

# Admin endpoints
GET    /api/admin/pending-uploads   - List uploads awaiting moderation
POST   /api/admin/uploads/:id/approve - Approve upload
POST   /api/admin/uploads/:id/reject  - Reject upload with reason
GET    /api/admin/uploads/stats     - Moderation statistics
```

### Database Schema

```sql
CREATE TABLE uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER NOT NULL,
    uploaded_by INTEGER NOT NULL,
    file_type VARCHAR(50) NOT NULL, -- photo, document
    original_filename VARCHAR(255),
    stored_filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    width INTEGER,
    height INTEGER,
    caption TEXT,
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    
    -- Moderation fields
    moderation_status VARCHAR(50) DEFAULT 'pending',
    moderated_by INTEGER,
    moderated_at TIMESTAMP,
    moderation_notes TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id),
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    FOREIGN KEY (moderated_by) REFERENCES users(id)
);

CREATE INDEX idx_uploads_moderation ON uploads(moderation_status, uploaded_at);
CREATE INDEX idx_uploads_entrant ON uploads(entrant_id, is_public);
```

### Moderation Workflow

```
1. User uploads file
   ↓
2. Server validates file (type, size)
   ↓
3. File stored with status='pending', is_public=false
   ↓
4. Optional: Admin notified via email
   ↓
5. Admin views moderation queue
   ↓
6. Admin approves OR rejects
   ↓
7a. APPROVE:                    7b. REJECT:
    - Set status='approved'         - Set status='rejected'
    - Set is_public=true            - Set is_public=false
    - Record admin ID               - Record admin ID
    - Log action                    - Add rejection reason
    - Notify user                   - Log action
                                    - Notify user with reason
```

## User Interface

### User's Pending Uploads View

```html
<div class="pending-uploads">
    <h2>Your Uploads</h2>
    
    <div class="upload-grid">
        <div class="upload-card pending">
            <img src="/uploads/thumb/..." />
            <div class="upload-status">
                <span class="badge badge-warning">Pending Approval</span>
                <p>Uploaded 2 hours ago</p>
            </div>
            <button class="btn-delete">Delete</button>
        </div>
        
        <div class="upload-card approved">
            <img src="/uploads/thumb/..." />
            <div class="upload-status">
                <span class="badge badge-success">Approved</span>
                <p>Published 1 day ago</p>
            </div>
        </div>
        
        <div class="upload-card rejected">
            <img src="/uploads/thumb/..." />
            <div class="upload-status">
                <span class="badge badge-danger">Rejected</span>
                <p class="rejection-reason">Image quality too low</p>
            </div>
            <button class="btn-reupload">Re-upload</button>
        </div>
    </div>
</div>
```

### Admin Moderation Queue

```html
<div class="moderation-queue">
    <h1>Pending Uploads</h1>
    
    <div class="filters">
        <select id="filter-type">
            <option value="all">All Types</option>
            <option value="photo">Photos</option>
            <option value="document">Documents</option>
        </select>
        
        <button id="bulk-approve">Approve Selected</button>
        <button id="bulk-reject">Reject Selected</button>
    </div>
    
    <div class="upload-list">
        <div class="upload-item">
            <input type="checkbox" class="select-upload" />
            
            <div class="upload-preview">
                <img src="/uploads/thumb/..." />
            </div>
            
            <div class="upload-info">
                <h3>Profile Photo</h3>
                <p><strong>Uploader:</strong> John Doe (john@example.com)</p>
                <p><strong>Profile:</strong> Jane Smith, Joint Secretary</p>
                <p><strong>Uploaded:</strong> 2024-11-25 14:30</p>
                <p><strong>Size:</strong> 2.4 MB (1200x800)</p>
            </div>
            
            <div class="upload-actions">
                <button class="btn-approve">
                    <i class="fas fa-check"></i> Approve
                </button>
                <button class="btn-reject">
                    <i class="fas fa-times"></i> Reject
                </button>
            </div>
        </div>
    </div>
</div>
```

### Rejection Modal

```html
<div class="modal reject-modal">
    <h2>Reject Upload</h2>
    
    <div class="upload-preview">
        <img src="/uploads/medium/..." />
    </div>
    
    <label for="rejection-reason">Reason for rejection:</label>
    <textarea id="rejection-reason" rows="4" placeholder="Explain why this upload is rejected..."></textarea>
    
    <div class="quick-reasons">
        <button class="quick-reason">Image quality too low</button>
        <button class="quick-reason">Inappropriate content</button>
        <button class="quick-reason">Wrong file type</button>
        <button class="quick-reason">Not related to profile</button>
    </div>
    
    <div class="modal-actions">
        <button class="btn-primary" onclick="confirmReject()">Reject Upload</button>
        <button class="btn-secondary" onclick="closeModal()">Cancel</button>
    </div>
</div>
```

## Backend Implementation

### Moderation Service

```python
# moderation_service.py

class ModerationService:
    def __init__(self, db):
        self.db = db
    
    def get_pending_uploads(self, filters=None):
        """Get all uploads pending moderation"""
        query = """
            SELECT u.*, 
                   up.name as uploader_name,
                   up.email as uploader_email,
                   e.name as profile_name,
                   e.position as profile_position
            FROM uploads u
            JOIN users up ON u.uploaded_by = up.id
            JOIN lateral_entrants e ON u.entrant_id = e.id
            WHERE u.moderation_status = 'pending'
            ORDER BY u.uploaded_at ASC
        """
        return self.db.execute(query).fetchall()
    
    def approve_upload(self, upload_id, admin_id):
        """Approve an upload"""
        self.db.execute("""
            UPDATE uploads
            SET moderation_status = 'approved',
                is_public = TRUE,
                moderated_by = ?,
                moderated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (admin_id, upload_id))
        self.db.commit()
        
        # Log action
        audit_log.log(
            user_id=admin_id,
            action='approve_upload',
            entity_type='upload',
            entity_id=upload_id
        )
        
        # Notify user
        upload = self.get_upload(upload_id)
        notification_service.notify_upload_approved(upload)
    
    def reject_upload(self, upload_id, admin_id, reason):
        """Reject an upload"""
        self.db.execute("""
            UPDATE uploads
            SET moderation_status = 'rejected',
                is_public = FALSE,
                moderated_by = ?,
                moderated_at = CURRENT_TIMESTAMP,
                moderation_notes = ?
            WHERE id = ?
        """, (admin_id, reason, upload_id))
        self.db.commit()
        
        # Log action
        audit_log.log(
            user_id=admin_id,
            action='reject_upload',
            entity_type='upload',
            entity_id=upload_id,
            new_value=reason
        )
        
        # Notify user
        upload = self.get_upload(upload_id)
        notification_service.notify_upload_rejected(upload, reason)
```

## Security Considerations

1. **Access Control**: Only admins can moderate uploads
2. **Audit Trail**: All moderation actions logged with admin ID
3. **File Retention**: Rejected uploads kept for 30 days
4. **Abuse Prevention**: Rate limit on re-uploads after rejection

## Testing Strategy

### Test Cases

1. **Upload Pending Status**:
   - Upload file → verify status='pending', is_public=false
   - Verify upload not visible to public
   - Verify user can see own pending upload

2. **Admin Approval**:
   - Admin approves upload
   - Verify status='approved', is_public=true
   - Verify upload now visible to public
   - Verify user notified

3. **Admin Rejection**:
   - Admin rejects with reason
   - Verify status='rejected', is_public=false
   - Verify upload not visible to public
   - Verify user sees rejection reason

4. **Bulk Actions**:
   - Select multiple uploads
   - Approve all → verify all approved
   - Reject all → verify all rejected with same reason

## Success Criteria

- [ ] All uploads go through moderation
- [ ] Admins can efficiently review uploads
- [ ] Users receive clear feedback on status
- [ ] Audit log captures all actions
- [ ] Performance meets requirements
- [ ] No unapproved content visible to public
- [ ] Bulk actions work correctly

## Related Specs

- [File Upload](../uploads/file-upload.md)
- [Admin Panel](../admin-panel/dashboard.md)
- [Notifications](../admin-panel/notifications.md)
