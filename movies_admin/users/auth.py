import http
import json
from logging import getLogger

import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

logger = getLogger(__name__)


class CustomBackend(BaseBackend):
    ADMIN_ROLE = "admin"

    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        payload = {'email': username, 'password': password}
        response = requests.post(url, data=json.dumps(payload))
        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()
        
        try:
            user, created = User.objects.get_or_create(id=data['id'],)
            user.email = data.get('email')
            user.is_admin = True if self.ADMIN_ROLE in data.get('roles', []) else False
            user.is_active = True
            user.save()
        except Exception as e:
            logger.info(e)
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
