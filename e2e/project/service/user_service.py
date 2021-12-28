from py3server.app.service import Service
from project.repository.user_repository import UserRepository


@Service()
class UserService:
    user_repo: UserRepository

    def add_user(self, firstname, lastname, age):
        return self.user_repo.add_user(firstname, lastname, age)

    def get_users(self):
        return self.user_repo.get_users()

    def get_user(self, user_id):
        return self.user_repo.get_user(user_id)

    def update_user(self, user_id, data):
        return self.user_repo.update_user(user_id, data)

    def remove_user(self, user_id):
        return self.user_repo.remove_user(user_id)
