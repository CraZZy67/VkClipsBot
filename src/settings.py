import dotenv

import os


class Settings:
    dotenv.load_dotenv()

    SLESH = '\\' if os.getenv('PLATFORM') == 'Windows' else '/'
    
    CREDS_PATH = f'creds{SLESH}'
    VIDEO_PATH = f'media{SLESH}'
    STATES_PATH = f'states{SLESH}'
    
    USERS_FILE_NAME = 'user_creds'
    ANONYM_FILE_NAME = 'anonym_creds'
    PUBLICS_STATE_NAME = 'publics'
    
    LOGIN_LINK = 'https://login.vk.com/?act=web_token'
    
    HEADERS = {
        'accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://vk.com', 'priority': 'u=1, i',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    MAX_LEN_QUEUE = 5
    