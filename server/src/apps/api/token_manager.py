import time
import threading
import uuid

class TokenManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TokenManager, cls).__new__(cls, *args, **kwargs)
                    cls._instance.tokens = {}
                    cls._instance.expiration_time = 3600  # Tokens expire after 1 hour
        return cls._instance

    def add_token(self, user_type, user_id):
        token = str(uuid.uuid4())
        expiration = time.time() + self.expiration_time
        with self._lock:
            self.tokens[token] = ({
                'userType': user_type,
                'userId': user_id
                }, expiration)
        return token

    def remove_token(self, token):
        with self._lock:
            self.tokens.pop(token, None)

    def validate_token(self, token): 
        with self._lock:
            if token in self.tokens:
                user_type, expiration = self.tokens[token]
                if time.time() < expiration:
                    return user_type
                else:
                    self.tokens.pop(token, None)  # Remove expired token
        return None

    def cleanup_expired_tokens(self):
        current_time = time.time()
        with self._lock:
            expired_tokens = [token for token, (_, expiration) in self.tokens.items() if current_time >= expiration]
            for token in expired_tokens:
                self.tokens.pop(token, None)
