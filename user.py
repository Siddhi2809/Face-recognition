from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, password, name, type):
        self.id = user_id
        self.password = password
        self.name = name
        self.type = type

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True 

    @property
    def is_active(self):
        return True 

    @property
    def is_anonymous(self):
        return False
