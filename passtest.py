from jose import jwt
from datetime import datetime, timedelta

# Replace with your actual secret key and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def encode_password(password: str) -> str:
    """
    Encodes a password into a JWT token.
    
    Args:
        password (str): The plaintext password to encode.
    
    Returns:
        str: A JWT token containing the password.
    """
    # Create a payload with the password and an expiration time (optional)
    payload = {
        "password": password,
        "exp": datetime.utcnow() + timedelta(days=365)  # Token expires in 1 year
    }
    
    # Encode the payload into a JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

if __name__ == "__main__":
    # Prompt the user for a password
    password = input("Enter the password to encode: ")
    
    # Encode the password
    encoded_password = encode_password(password)
    
    # Output the encoded password
    print(f"Encoded password (JWT): {encoded_password}")