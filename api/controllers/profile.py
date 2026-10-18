from flask import jsonify, g, Blueprint, redirect
from flask import request
from auth import requires_auth
from auth0Mgmt import get_user_info_with_userids, get_name, update_user_profilepic
from werkzeug.utils import secure_filename
import os
from object_storage import upload_profile_picture, signed_profile_picture_url

bp = Blueprint('profile', __name__)


@bp.route('/profile/picture/<user_id>', methods=['GET'])
def get_profile_picture(user_id):
    """Resolve a stable avatar address without exposing a public bucket."""
    try:
        signed_url = signed_profile_picture_url(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid profile picture user ID'}), 400
    response = redirect(signed_url, code=302)
    response.headers['Cache-Control'] = 'no-store'
    return response


@bp.route('/profile', methods=['GET'])
@requires_auth
def get_profile_details():
    user_id = g.user.get('sub')

    user_ids = [user_id]
    user_info = get_user_info_with_userids(user_ids)
    user_info = user_info[0]

    return jsonify({
        'picture': user_info.get("picture"), 'name': get_name(user_info)
    }), 200


@bp.route('/profile', methods=['PUT'])
@requires_auth
def update_profile_details():
    user_id = g.user.get('sub')

    file = request.files['file'] if 'file' in request.files else None
    public_url = None

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        temp_path = os.path.join('/tmp', filename)
        file.save(temp_path)

        try:
            public_url = upload_profile_picture(temp_path, user_id, file.mimetype)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        file = None

    name = request.form.get('name', None)

    update_user_profilepic(user_id, public_url, name)

    return jsonify({
        'picture': public_url, 'name': name, 'connection': 'Username-Password-Authentication'
    }), 200
