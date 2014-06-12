import json
import re

from flask import request, session
from pyoauth2_shift.provider import AuthorizationProvider

class Application(object):
    def find(id):
        return True

class ShiftAuthorizationProvider(AuthorizationProvider):

    def validate_client_id(self, client_id):
        return Application.find(client_id) is not None

    def validate_client_secret(self, client_id, client_request):
        app = Application.find(client_id)
        if app is not None and app.secret == client_secret:
            return True
        return False

    def validate_redirect_uri(self, client_id, redirect_uri):
        app = Application.find(client_id)
        if app is not None and app.redirect_uri == redirect_uri.split('?')[0]:
            return True
        return False

    def validate_access(self):
        return session.user is not None

    def validate_scope(self, client_id, scope):
        return True if scope == "" else False

    def persist_authorization_code(self, client_id, code, scope):
        key = 'oauth2.authorization_code.%s:%s' % (client_id, code)

        data = {'client_id': client_id,
                'scope': scope,
                'user_id': session.user.id}
        self.redis.setex(key, 60, json.dumps(data))

    def persist_token_information(self, client_id, scope, access_token,
                                  token_type, expires_in, refresh_token,
                                  data):
        access_key = 'oauth.access_token:%s' % access_token
        self.redis.setex(access_key, expires_in, json.dumps(data))

        refresh_key = 'oauth2.refresh_token%s:%s' % (client_id, refresh_token)
        self.redis.set(refresh_key, json.dumps(data))

        key = 'oauth2.client_user.%s:%s' % (client_id, data.get('user_id'))
        self.redis.sadd(key, access_key, refresh_key)

    def from_authorization_code(self, client_id, code, scope):
        key = 'oauth2.authorization_code.%s:%s' % (client_id, code)
        data = self.redis.get(key)
        if data is not None:
            if(scope == '' or scope == data.get('scope')) and data.get('client_id') == client_id:
                return data
        return None

    def from_refresh_token(self, client_id, refresh_token, scope):
        key = 'oauth2.refresh_token.%s:%s' % (client_id, refresh_token)
        data = self.redis.get(key)
        if data is not None:
            data = json.loads(data)
            if(scope == '' or scope == data.get('scope')) and data.get('client_id') == client_id:
                return data
        return None

    def discard_authorization_code(self, client_id, code):
        key = 'oauth2.authorization_code.%s:%s' % (client_id, code)
        self.redis.delete(key)

    def discard_refresh_token(self, client_id, refresh_token):
        key = 'oauth2.refresh_token.%s:%s' % (client_id, refresh_token)
        self.redis.delete(key)

    def discard_client_user_tokens(self, client_id, user_id):
        keys = 'oauth2.client_user.%s:%s' % (client_id, user_id)
        pipe = self.redis.pipeline()
        for key in self.redis.smembers(keys):
            pipe.delete(key)
        pipe.execute()
