import tornado.web
from ..token_manager import TokenManager
    
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        token = self.request.headers.get("Authorization")
        token_manager = TokenManager()
        if token:
            return token_manager.validate_token(token)
        return None
    
    def prepare(self):
        if not self.current_user:
            self.set_status(401)
            self.write({"error": "Unauthorized access"})
            self.finish()