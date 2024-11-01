from fastapi import APIRouter, Request, Response
import controller.user as user_controller
from api_models import *

class UserRoutes:
    
    def __init__(self):
        self.router = APIRouter(
            prefix='/api/user'
        )
        self.router.add_api_route('/{session}', self.get_user_info, methods=['GET'])
        self.router.add_api_route('', self.add_user, methods=['POST'])
        self.router.add_api_route('', self.update_user_info, methods=['PUT'])
        self.router.add_api_route('', self.delete_user, methods=['DELETE'])


    async def get_user_info(self, request: Request, session):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)
        
        return user_controller.get_user_info(session)


    async def add_user(self, user: UserPydantic):
        return user_controller.add_user(user.dict())


    async def update_user_info(self, request: Request, user: updateUser):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)

        return user_controller.update_user(user)


    async def delete_user(self, request: Request, session: UserDeletePydantic):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)

        return user_controller.delete_user(session.dict())

