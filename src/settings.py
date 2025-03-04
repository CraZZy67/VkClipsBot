from dataclasses import dataclass

@dataclass
class Settings: 
    CREDS_PATH = 'creds/'
    VIDEO_PATH = 'media/'
    
    USERS_FILE_NAME = 'user_creds'
    ANONYM_FILE_NAME = 'anonym_creds'
    