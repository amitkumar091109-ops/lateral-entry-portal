"""
Upload Routes
API endpoints for file uploads (photos and documents)
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
import os
from PIL import Image

from ..database import db, row_to_dict
from ..auth.decorators import require_auth
from ..config import get_config

config = get_config()

upload_bp = Blueprint('upload', __name__, url_prefix='/api/uploads')

# Allowed file extensions
ALLOWED_IMAGES = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_DOCUMENTS = {'pdf', 'doc', 'docx', 'txt'}

# Max file sizes (in bytes)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename, file_type):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()

    if file_type == 'image':
        return ext in ALLOWED_IMAGES
    elif file_type == 'document':
        return ext in ALLOWED_DOCUMENTS

    return False


def resize_image(file_path, max_width=1200, max_height=1200):
    """Resize image to maximum dimensions while maintaining aspect ratio"""
    try:
        with Image.open(file_path) as img:
            # Convert RGBA to RGB if needed
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Calculate new dimensions
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # Save optimized
            img.save(file_path, optimize=True, quality=85)

        return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False


@upload_bp.route('/image', methods=['POST'])
@require_auth
def upload_image():
    """Upload profile photo or gallery image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        purpose = request.form.get('purpose', 'profile_photo')  # or 'gallery'

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename, 'image'):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_IMAGE_SIZE:
            return jsonify({'error': f'File too large. Max size: {MAX_IMAGE_SIZE / 1024 / 1024}MB'}), 400

        # Create uploads directory
        upload_dir = Path(__file__).parent.parent.parent / 'uploads' / 'images'
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(file.filename)
        unique_filename = f"{timestamp}_{request.current_user['user_id']}_{filename}"
        file_path = upload_dir / unique_filename

        # Save file
        file.save(file_path)

        # Resize image
        resize_image(file_path)

        # Get file type
        file_type = file.content_type

        # Insert into database
        upload_id = db.insert("""
            INSERT INTO uploads (
                user_id, file_path, file_type, file_size, purpose, moderation_status
            )
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (
            request.current_user['user_id'],
            f'/uploads/images/{unique_filename}',
            file_type,
            file_size,
            purpose
        ))

        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully and pending moderation',
            'upload_id': upload_id,
            'file_path': f'/uploads/images/{unique_filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@upload_bp.route('/document', methods=['POST'])
@require_auth
def upload_document():
    """Upload document"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        purpose = request.form.get('purpose', 'document')

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename, 'document'):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, DOC, DOCX, TXT'}), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_DOCUMENT_SIZE:
            return jsonify({'error': f'File too large. Max size: {MAX_DOCUMENT_SIZE / 1024 / 1024}MB'}), 400

        # Create uploads directory
        upload_dir = Path(__file__).parent.parent.parent / 'uploads' / 'documents'
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(file.filename)
        unique_filename = f"{timestamp}_{request.current_user['user_id']}_{filename}"
        file_path = upload_dir / unique_filename

        # Save file
        file.save(file_path)

        # Get file type
        file_type = file.content_type

        # Insert into database
        upload_id = db.insert("""
            INSERT INTO uploads (
                user_id, file_path, file_type, file_size, purpose, moderation_status
            )
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (
            request.current_user['user_id'],
            f'/uploads/documents/{unique_filename}',
            file_type,
            file_size,
            purpose
        ))

        return jsonify({
            'success': True,
            'message': 'Document uploaded successfully and pending moderation',
            'upload_id': upload_id,
            'file_path': f'/uploads/documents/{unique_filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@upload_bp.route('/my-uploads', methods=['GET'])
@require_auth
def get_my_uploads():
    """Get current user's uploads"""
    try:
        uploads = db.execute("""
            SELECT * FROM uploads
            WHERE user_id = ?
            ORDER BY uploaded_at DESC
        """, (request.current_user['user_id'],))

        return jsonify({
            'success': True,
            'uploads': [row_to_dict(u) for u in uploads]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@upload_bp.route('/<int:upload_id>', methods=['DELETE'])
@require_auth
def delete_upload(upload_id):
    """Delete an upload"""
    try:
        # Check ownership
        upload = db.execute_one("""
            SELECT * FROM uploads WHERE id = ?
        """, (upload_id,))

        if not upload:
            return jsonify({'error': 'Upload not found'}), 404

        upload_dict = row_to_dict(upload)

        if upload_dict['user_id'] != request.current_user['user_id'] and request.current_user['role'] != 'admin':
            return jsonify({'error': 'Forbidden'}), 403

        # Delete file
        file_path = Path(__file__).parent.parent.parent / upload_dict['file_path'].lstrip('/')
        if file_path.exists():
            file_path.unlink()

        # Delete from database
        db.execute("DELETE FROM uploads WHERE id = ?", (upload_id,))

        return jsonify({
            'success': True,
            'message': 'Upload deleted successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
