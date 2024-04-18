#!/usr/bin/env python3
"""
SessionExpAuth class to manage API authentication
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from models.user import User
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class to manage API authentication
    """

    def __init__(self):
        """Initialize SessionExpAuth
        """
        s_duration = getenv('SESSION_DURATION')
        try:
            session_duration = int(s_duration)
        except Exception:
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Create session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return
        session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user ID from session
        """
        if not session_id:
            return
        if session_id not in self.user_id_by_session_id.keys():
            return
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return
        if self.session_duration <= 0:
            return session_dict.get('user_id')
       created_at = session_dict.get('created_at')
        if not created_at:
            return
        expired_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expired_time:
            return
        return session_dict.get('user_id')
