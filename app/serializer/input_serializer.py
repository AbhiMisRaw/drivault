from typing_extensions import Self

from pydantic import BaseModel, model_validator


class UserLoginPayload(BaseModel):
    email: str
    password: str

class UserRegisterPayload(BaseModel):
    fullname: str
    email: str
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self


class UploadFile(BaseModel):
    pass
