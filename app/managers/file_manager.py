
import os
from pathlib import Path
from typing import List, Union

from dotenv import load_dotenv
from fastapi import UploadFile

from app.models import FileModel, UserModel
from app.constants import FileTypeEnum, FileExtensionEnum, AccessType
from app.utils import Util


# Load environment configuration
load_dotenv()

class FileManager():

    def __init__(self, user_id = 1):
        self.user_id = user_id
        # Get storage path from environment or use default
        self.storage_path = os.getenv("FILE_STORAGE_PATH")
        # Ensure storage directory exists
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)


    async def upload_file(
            self,
            files: Union[UploadFile, List[UploadFile]]
        ):
        """
            This method ensure files (or file) are uploaded
            Uploaded : It means files are saved to the specified locations by environment vars
                        and daved all the saved meta data to the database.
        """
        # Convert single file to list for uniform processing
        if not isinstance(files, list):
            files = [files]
        
        uploaded_files = []
        user = await UserModel.get(id=self.user_id)
        for file in files:
            try:
                # Step 1: Copy the file to storage
                file_path = await self._handle_file_copying(user, file)
                
                # Step 2: Extract file metadata
                file_size = await self._get_file_size(file_path)
                file_type, file_extension = Util.get_file_type_and_extension(file.filename)
                
                # Step 3: Create database record
                file_record = FileModel(
                    name=str(file.filename),
                    original_filename=self.generate_file_name(file.filename),
                    mime_type=file.content_type,
                    type=file_type,
                    extension=file_extension,
                    file_path=file_path,
                    owner_id=self.user_id,  # Hardcoded to user_id 1 for now
                    size=file_size,
                    access_type=AccessType.PRIVATE,  # Default to private
                    metadata={},
                    shared_with=[]
                )
                
                # Save to database
                await file_record.save()
                uploaded_files.append(file_record)
                
            except Exception as e:
                # Log error and continue with other files
                print(f"Error uploading file {file.filename}: {str(e)}")
                # You might want to raise an exception or collect errors
                raise
        
        return uploaded_files


    def generate_file_name(self, file_name: str):
        pfft = file_name.split('.')
        name = pfft[0]
        ext = pfft[1]
        return f"{name}-{Util.get_uuid()}.{ext}"


    async def _handle_file_copying(self, user, file: UploadFile) -> str:
        """This handles the file copying operation in specified location in manager."""
        # Generate unique filename
        unique_filename = self.generate_file_name(file.filename)
        destination = os.path.join(self.storage_path, user.email, unique_filename)

        # Copy file to destination
        file_path = await Util.copy_file(file.file, destination)
        return file_path
    
    
    async def _get_file_size(self, file_path: str) -> float:
        """Get file size in bytes."""
        return float(os.path.getsize(file_path))
    
    
    async def list_files(self):
        files = await FileModel.filter(owner=self.user_id)
        return files
    
    async def download_file(self, file_id: str):
        """
        It downloads the file
        
        :param file_id: primary key for the file object.
        :type file_id: str
        """
        
        file = await FileModel.filter(id=file_id).first()


