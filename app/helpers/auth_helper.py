# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()

# # Password hashing context using passlib
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Use environment variables for sensitive information
# SECRET_KEY = os.getenv("SECRET_KEY")  # Store in .env file
# if not SECRET_KEY:
#     raise ValueError("SECRET_KEY environment variable is not set")
    
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry duration


# # Function to verify password
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verifies a plain-text password against a hashed password using bcrypt.
#     """
#     return pwd_context.verify(plain_password, hashed_password)


# # Function to hash password
# def hash_password(password: str) -> str:
#     """
#     Hashes a plain-text password using bcrypt.
#     """
#     return pwd_context.hash(password)


# # Function to create a JWT token
# def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
#     """
#     Creates a JWT token with an expiration time.
#     """
#     to_encode = data.copy()
    
#     # Set the expiration time for the token
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
    
#     # Encode the JWT token
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# # Function to verify and decode JWT token
# def verify_token(token: str):
#     """
#     Verifies the JWT token, decodes it, and returns the payload.
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise Exception("Could not validate credentials")
