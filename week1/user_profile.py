from pydantic import BaseModel, Field, field_validator, ValidationError
import re

class UserProfile(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=120)
    email: str
    pan: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, v):
    
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", v.upper()):
            raise ValueError("Invalid PAN format (expected ABCDE1234F)")
        return v.upper()


try:
    user = UserProfile(
        name="Ravi Kumar",
        age=25,
        email="ravi@example.com",
        pan="ABCDE1234F",
    )
    print(" Valid:", user.model_dump())
except ValidationError as e:
    print(" ValidationError caught as expected:\n", e)


try:
    bad = UserProfile(
        name="R",
        age=15,
        email="not-an-email",
        pan="12345ABCDE",
    )
    print(bad)
except ValidationError as e:
    print(" ValidationError caught as expected:\n", e)
    print("Error count:", e.error_count())