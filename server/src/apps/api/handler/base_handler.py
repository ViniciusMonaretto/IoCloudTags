import tornado.web
from ..token_manager import TokenManager
    
class BaseHandler(tornado.web.RequestHandler):

    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins, or specify allowed origins
        self.set_header("Access-Control-Allow-Methods", "POST, DELETE, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_status(204)  # No Content for preflight
        self.finish()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")  # Allow specific methods
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")  # Allow specific headers

    def get_current_user(self):
        token = self.request.headers.get("Authorization")
        token_manager = TokenManager()
        if token:
            return token_manager.validate_token(token)
        return None
    
    def prepare(self):
        if self.request.method == "OPTIONS":
            return

        if not self.current_user:
            self.set_status(401)
            self.write({"error": "Unauthorized access"})
            self.finish()