from fastapi import APIRouter, Request


from app.serializer import UserRegisterPayload, UserLoginPayload
from app.models.response import UserResponse
from app.exceptions import UserAlreadyExistsException
from app.managers import UserManager

user = APIRouter(
    prefix="/auth"
)

@user.post("/register", response_model=UserResponse)
async def create_user(request: Request, payload: UserRegisterPayload):
    """Create User"""

    manager = UserManager()
    response = await manager.create_user(payload)
    return response


@user.post("/login")
async def login(request: Request, payload: UserLoginPayload):
    
    response =await UserManager().login(payload)
    return response


@user.post("/logout")
async def logout(request: Request):
    return {
        "message":"You are succesfully logged out.",
        "status": 200
    }