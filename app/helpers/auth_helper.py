from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Password hashing context using passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm for JWT tokens (use environment variables in a real project)
SECRET_KEY = "your_secret_key_here"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry duration


# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password using bcrypt.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Function to hash password
def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    """
    return pwd_context.hash(password)


# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT token with an expiration time.
    """
    to_encode = data.copy()
    
    # Set the expiration time for the token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify and decode JWT token
def verify_token(token: str):
    """
    Verifies the JWT token, decodes it, and returns the payload.
    """
    # try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Could not validate credentials")
