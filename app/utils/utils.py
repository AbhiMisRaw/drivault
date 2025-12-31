import os
import uuid
import tempfile
import aiofiles


from pathlib import Path
from typing import BinaryIO, Union

from app.constants import FileExtensionEnum, FileTypeEnum

class Util:

    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())
    
    @staticmethod
    async def copy_file(
        file_object: BinaryIO,
        destination: Union[str, Path],
        chunk_size: int = 65536
    )-> str:
        """
        Asynchronously copy a file object to the specified location.
        
        Args:
            file_object: A file-like object (e.g., UploadFile.file, open file handle)
            destination: Destination path where the file should be copied
            chunk_size: Size of chunks to read/write at a time (default: 64KB)
        
        Returns:
            str: The absolute path of the destination file
        """
        destination_path = Path(destination)

        # Ensure parent directories exist
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(destination_path, 'wb') as dest_file:
            while chunk := file_object.read(chunk_size):
                await dest_file.write(chunk)
        return str(destination_path.absolute())
    

    @staticmethod
    def get_file_type_and_extension(filename: str):
        """Determine file type based on extension."""
        extension = Util.get_file_extension(filename)
        
        if not extension:
            return FileTypeEnum.OTHERS, None
        
        # Image types
        if extension in [FileExtensionEnum.JPG, FileExtensionEnum.JPEG]:
            return FileTypeEnum.IMAGE, extension
        
        # Video types
        if extension in [FileExtensionEnum.MKV, FileExtensionEnum.MP4]:
            return FileTypeEnum.VIDEO, extension
        
        # Audio types
        if extension == FileExtensionEnum.MP3:
            return FileTypeEnum.AUDIO, extension
        
        # Document types
        if extension in [FileExtensionEnum.PDF, FileExtensionEnum.DOC, FileExtensionEnum.PPT]:
            return FileTypeEnum.DOCUMENT, extension
        
        return FileTypeEnum.OTHERS, extension
    
    
    @staticmethod
    def get_file_extension(filename: str) -> FileExtensionEnum:
        """Extract and validate file extension."""
        parts = filename.rsplit('.', 1)
        if len(parts) < 2:
            return None
        
        ext = parts[1].lower()
        try:
            return FileExtensionEnum(ext)
        except ValueError:
            return None


    @staticmethod
    def validate_storage_path(storage_path: str = None, default_path: str = "./uploads") -> str:
        """
        Validate and ensure the storage path is writable and safe to use.
        
        This function:
        1. Uses default path if storage_path is None or empty
        2. Checks if the path is a system path (restricted locations)
        3. Verifies write permissions
        4. Creates the directory if it doesn't exist
        5. Tests write access by creating a temporary file
        
        Args:
            storage_path: The path to validate (from env or user input)
            default_path: Fallback path if storage_path is invalid (default: "./uploads")
        
        Returns:
            str: Validated and absolute storage path
        
        Raises:
            PermissionError: If the path is not writable
            ValueError: If the path is a system path or invalid
        """
        # Use default if no path provided
        if not storage_path or storage_path.strip() == "":
            storage_path = default_path
            print(f"ℹ️  No FILE_STORAGE_PATH provided, using default: {storage_path}")
        
        # Remove quotes if present (from .env files)
        storage_path = storage_path.strip().strip('"').strip("'")
        
        # Convert to Path object and resolve to absolute path
        path_obj = Path(storage_path).expanduser().resolve()
        
        # Check if it's a system path (restricted locations)
        if Util._is_system_path(path_obj):
            error_msg = (
                f"❌ Storage path '{path_obj}' appears to be a system path. "
                f"System paths (like /usr, /bin, /etc, /sys, /proc, etc.) are not allowed. "
                f"Please use a local path like './uploads' or a path in your home directory. "
                f"Falling back to default: {default_path}"
            )
            print(error_msg)
            # Fallback to default path
            path_obj = Path(default_path).expanduser().resolve()
        
        # Try to create the directory if it doesn't exist
        try:
            path_obj.mkdir(parents=True, exist_ok=True)
            print(f"✅ Storage directory created/verified: {path_obj}")
        except PermissionError as e:
            raise PermissionError(
                f"❌ Cannot create storage directory at '{path_obj}'. "
                f"Permission denied. Please check directory permissions or use a different path."
            ) from e
        except Exception as e:
            raise ValueError(
                f"❌ Failed to create storage directory at '{path_obj}': {str(e)}"
            ) from e
        
        # Test write permissions by creating a temporary file
        if not Util._test_write_permission(path_obj):
            raise PermissionError(
                f"❌ Storage path '{path_obj}' exists but is not writable. "
                f"Please check permissions or choose a different path."
            )
        
        print(f"✅ Storage path validated with write access: {path_obj}")
        return str(path_obj)
    
    @staticmethod
    def _is_system_path(path_obj: Path) -> bool:
        """Check if the path is a system/restricted path."""
        path_str = str(path_obj).lower()
        
        # List of system directories that should not be used for file storage
        system_paths = ['/usr', '/bin', '/sbin', '/etc', '/sys', '/proc', '/boot', '/dev', '/lib', '/lib64']
        
        # Check if path starts with any system path or is at root level (except /tmp and /var/tmp)
        for sys_path in system_paths:
            if path_str.startswith(sys_path):
                return True
        
        # Check if trying to write directly to root (/)
        if path_obj.parent == path_obj.root and path_str not in ['/tmp', '/var/tmp']:
            return True
        
        return False
    
    @staticmethod
    def _test_write_permission(path_obj: Path) -> bool:
        """Test if we can write to the directory."""
        test_file = path_obj / f".write_test_{uuid.uuid4().hex}"
        try:
            test_file.touch()
            test_file.unlink()
            return True
        except Exception:
            return False


    @staticmethod
    def validate_storage_path(storage_path: str = None, default_path: str = "./uploads") -> str:
        """
        Validate and ensure the storage path is writable and safe to use.
        
        This function:
        1. Uses default path if storage_path is None or empty
        2. Checks if the path is a system path (restricted locations)
        3. Verifies write permissions
        4. Creates the directory if it doesn't exist
        5. Tests write access by creating a temporary file
        
        Args:
            storage_path: The path to validate (from env or user input)
            default_path: Fallback path if storage_path is invalid (default: "./uploads")
        
        Returns:
            str: Validated and absolute storage path
        
        Raises:
            PermissionError: If the path is not writable
            ValueError: If the path is a system path or invalid
        """
        # Use default if no path provided
        if not storage_path or storage_path.strip() == "":
            storage_path = default_path
            print(f"ℹ️  No FILE_STORAGE_PATH provided, using default: {storage_path}")
        
        # Remove quotes if present (from .env files)
        storage_path = storage_path.strip().strip('"').strip("'")
        
        # Convert to Path object and resolve to absolute path
        path_obj = Path(storage_path).expanduser().resolve()
        
        # Check if it's a system path (restricted locations)
        if Util._is_system_path(path_obj):
            error_msg = (
                f"❌ Storage path '{path_obj}' appears to be a system path. "
                f"System paths (like /usr, /bin, /etc, /sys, /proc, etc.) are not allowed. "
                f"Please use a local path like './uploads' or a path in your home directory. "
                f"Falling back to default: {default_path}"
            )
            print(error_msg)
            # Fallback to default path
            path_obj = Path(default_path).expanduser().resolve()
        
        # Try to create the directory if it doesn't exist
        try:
            path_obj.mkdir(parents=True, exist_ok=True)
            print(f"✅ Storage directory created/verified: {path_obj}")
        except PermissionError as e:
            raise PermissionError(
                f"❌ Cannot create storage directory at '{path_obj}'. "
                f"Permission denied. Please check directory permissions or use a different path."
            ) from e
        except Exception as e:
            raise ValueError(
                f"❌ Failed to create storage directory at '{path_obj}': {str(e)}"
            ) from e
        
        # Test write permissions by creating a temporary file
        if not Util._test_write_permission(path_obj):
            raise PermissionError(
                f"❌ Storage path '{path_obj}' exists but is not writable. "
                f"Please check permissions or choose a different path."
            )
        
        print(f"✅ Storage path validated with write access: {path_obj}")
        return str(path_obj)
    
    @staticmethod
    def _is_system_path(path_obj: Path) -> bool:
        """Check if the path is a system/restricted path."""
        path_str = str(path_obj).lower()
        
        # List of system directories that should not be used for file storage
        system_paths = ['/usr', '/bin', '/sbin', '/etc', '/sys', '/proc', '/boot', '/dev', '/lib', '/lib64']
        
        # Check if path starts with any system path or is at root level (except /tmp and /var/tmp)
        for sys_path in system_paths:
            if path_str.startswith(sys_path):
                return True
        
        # Check if trying to write directly to root (/)
        if path_obj.parent == path_obj.root and path_str not in ['/tmp', '/var/tmp']:
            return True
        
        return False
    
    @staticmethod
    def _test_write_permission(path_obj: Path) -> bool:
        """Test if we can write to the directory."""
        test_file = path_obj / f".write_test_{uuid.uuid4().hex}"
        try:
            test_file.touch()
            test_file.unlink()
            return True
        except Exception:
            return False
