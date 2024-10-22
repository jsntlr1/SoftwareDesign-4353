from flask import Flask, request, jsonify, Blueprint
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
notifications_bp = Blueprint('notifications', __name__)

#temp test before database implementation
notifications = [
    {
        'id': 1,
        'user_id': 1,
        'message': 'You have been assigned to Event 1.',
        'timestamp': datetime.now(),
        'read': False
    },
]

@notifications_bp.route('/mark_notification_read', methods=['POST'])
def mark_notification_read():
    data = request.get_json()
    notification_id = data.get('notification_id')
    for n in notifications:
        if n['id'] == notification_id:
            n['read'] = True
            logging.info(f'Notification {notification_id} marked as read')
            break
    
    return '', 204

@notifications_bp.route('/get_notifications')
def get_notifications():
    user_id = request.args.get('user_id', 1)
    unread = request.args.get('unread', 'false').lower() == 'true'
    user_notifications = [n for n in notifications if n['user_id'] == int(user_id) and (not n['read'] if unread else True)]
    return jsonify({'notifications': user_notifications})