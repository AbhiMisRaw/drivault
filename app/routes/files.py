from typing import List
from fastapi import (
    APIRouter,
    Request,
    UploadFile, 
    Depends
)
from app.utils.security import get_current_user
from app.models import UserModel

from app.managers import FileManager
file = APIRouter(
    prefix="/files"
)

@file.get("/list/all")
async def list_files(request: Request, user: UserModel = Depends(get_current_user)):
    print(user)
    user_id = user.id
    manager = FileManager(
        user_id=user_id
    )

    response = await manager.list_files()
    return response


@file.post("/upload")
async def upload_files(
    request: Request,
    files: List[UploadFile],
    user: UserModel = Depends(get_current_user)
):

    user_id = user.id
    manager = FileManager(
        user_id=user_id
    )

    response = await manager.upload_file(files)
    return response

