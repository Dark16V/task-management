from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

class RegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str

    @field_validator("username")
    def username_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Username cannot be empty")
        return value

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("The passwords do not match")
        return self


class LoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6)
