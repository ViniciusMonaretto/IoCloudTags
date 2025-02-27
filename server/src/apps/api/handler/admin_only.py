from .base_handler import BaseHandler
from src.Model.user_model import TypeOfUser

class AdminHandler(BaseHandler):

    def prepare(self):
        if self.request.method == "OPTIONS":
            return

        if not self.current_user:
            self.set_status(401)
            self.write({"error": "Unauthorized access"})
            self.finish()
        
        if self.current_user['userType'] == TypeOfUser.Admin.value:
            self.set_status(403)
            self.write({"error": "Forbidden: You do not have access to this resource"})
            self.finish()
            return