from classes.user import User


class Platform:

    all_users = []

    def __init__(self):
        pass

    def create_user(self, name):
        user = User(name)
        self.all_users.append(user)
        return user