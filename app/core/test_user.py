from app.core.models import UserInDB
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Test user credentials
TEST_USER = {
    "username": "test@example.com",
    "email": "test@example.com",
    "full_name": "Test User",
    "disabled": False,
    "hashed_password": get_password_hash("testpassword123")
}

# Create test user instance
test_user_db = UserInDB(**TEST_USER)

def get_test_user():
    """Get the test user for authentication testing."""
    return test_user_db 