import os

class Config:
    # SECRET_KEY = 'thisIsSecretKey'  
    JWT_ALGORITHM = 'HS256'
    MONGO_URI = 'mongodb://localhost:27017/MovieDB'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads') #os.getcwd is get current working directory.
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    API_KEY = 'dd39691a'
    YOUTUBE_API_KEY = 'AIzaSyAHX3vfeBZ51GkPTHV6TWWK4y4NIoPwOxY'
