from tortoise.exceptions import IntegrityError
from pydantic import BaseModel

from app.models import UserModel as User
from app.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.utils.security import create_access_token, verify_password, hash_password

class UserManager():
    def __init__(self):
        pass

    async def create_user(self, model: BaseModel):
        try:
            user = User(**model.model_dump())
            user.password = hash_password(user.password)
            await user.save()
        except (IntegrityError) as e:
            raise UserAlreadyExistsException("User with this email already exists")

        return user
    
    async def login(self, model: BaseModel):
        auth_error = InvalidCredentialsException()
        #  find user using email.
        user = await User.filter(is_active=True).filter(email=model.email).first()
        # check password
        if user:
            print("user is exist")
            print(user)
            print(user.email)

        if not user or not verify_password(model.password, user.password):
            print(user)
            raise auth_error
        
        user_info = {
            "id":user.id,
            "email":user.email,
            "role":user.role
        }
        
        # print("password is verified")
        access_token = create_access_token(data = user_info)
        response = {
            "token":access_token,
            "token_type":"bearer",
            "user":user_info
        }
        return response

# I want to write a route handler where a user can upload 
# single or multiple files. and as of now we have no 