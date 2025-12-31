from enum import Enum

class FileTypeEnum(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    GIF = "gif"
    AUDIO = "audio"
    OTHERS = "others"
    

class FileExtensionEnum(str, Enum):
    JPG = "jpg"
    JPEG = "jpeg"
    MKV = "mkv"
    MP4 = "mp4"
    MP3 = "mp3"
    PDF = "pdf"
    DOC = "doc"
    PPT = "ppt"


class UserRoleType(str, Enum):
    STANDARD = "standard"
    ADMIN = "admin"


class AccessType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    