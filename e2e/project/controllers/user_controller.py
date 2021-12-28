from project.service.user_service import UserService
from py3server.web.controllers.rest_controller import RestController
from py3server.web.mapping.delete_mapping import DeleteMapping
from py3server.web.mapping.get_mapping import GetMapping
from py3server.web.mapping.post_mapping import PostMapping
from py3server.web.mapping.put_mapping import PutMapping
from py3server.web.params.body import Body
from py3server.web.params.int_path_param import IntPP
from py3server.web.response import Response


@RestController('/users')
class UserController(object):
    user_service: UserService

    @PostMapping()
    def create_user(self, body: Body):
        """
        User creation endpoint;
        required:
            - firstname
            - lastname
        optional:
            - age
          """
        errors = []
        required_fields = ['firstname', 'lastname']
        for required_field in required_fields:
            if not body.get(required_field):
                errors.append({
                    'field': required_field,
                    'code': 'REQUIRED'
                })

        if len(errors) > 0:
            return Response(400, errors)

        firstname, lastname, age = [
            body['firstname'],
            body['lastname'],
            body.get('age', 0)
        ]

        user = self.user_service.add_user(firstname, lastname, age)

        return Response(200, user)

    @GetMapping()
    def get_users(self):
        users = self.user_service.get_users()
        return Response(200, users)

    @GetMapping('/{id}')
    def get_user(self, user_id: IntPP('id')):
        user = self.user_service.get_user(user_id)
        return Response(200, user)

    @PutMapping('/{id}')
    def update_user(self, user_id: IntPP('id'), body: Body):
        user = self.user_service.update_user(user_id, body)
        return Response(200, user)

    @DeleteMapping('/{id}')
    def delete_user(self, user_id: IntPP('id')):
        self.user_service.remove_user(user_id)
        return Response(204)
