class Config:
    MONGO_URI = "mongodb://localhost:27017/taskmanager"
    JWT_SECRET_KEY = "456789897865453456788"  
    SECRET_KEY = "somerandomsecretkey"
    DEBUG = True
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token" 
    JWT_COOKIE_SECURE= False  
    WTF_CSRF_ENABLED = False
    JWT_COOKIE_CSRF_PROTECT = False

