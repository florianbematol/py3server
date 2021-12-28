from py3server.app.repository import Repository


@Repository()
class UserRepository:

    def __init__(self):
        self.users = []

    def add_user(self, firstname, lastname, age):
        user = {
            "firstname": firstname,
            "lastname": lastname,
            "age": age
        }
        self.users.append(user)
        return user

    def get_users(self):
        return self.users

    def get_user(self, user_id):
        if user_id > len(self.users):
            return None
        return self.users[user_id - 1]

    def update_user(self, user_id, data):
        self.users[user_id - 1].update(data)
        return self.users[user_id - 1]

    def remove_user(self, user_id):
        del self.users[user_id - 1]
