from datetime import datetime

from pydantic import BaseModel, Field, constr, field_validator

from typing import Optional

from utils import Sex, form_body, get_attributes_enum
from models import User


class UserBase(BaseModel):
    """Base user scheme"""
    pass

    class Config:
        orm_mode = True 
        from_attributes = True


@form_body
class UserCreateScheme(UserBase):
    """Create user scheme"""
    e_mail: Optional[constr(max_length=30)] = Field(pattern=r"[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+")
    first_name: Optional[constr(max_length=10)] = Field(default="Ivan")
    last_name: Optional[constr(max_length=15)] = Field(default="Ivanov")
    sex: Sex = Field(...)
    latitude: Optional[float] = Field(default=0)
    longitude: Optional[float] = Field(default=0)
    
    @field_validator('sex', mode="after")
    def validate_sex(cls, value) -> str:
        if isinstance(value, Sex):          
            return value.value
        return value
    
    @field_validator('e_mail', mode="before")
    def validate_email(cls, value: str) -> str:
        return value.lower()
    

class UserCreateResponseScheme(UserBase):
    """Response status od creation scheme"""
    id: Optional[int] = Field(...)
    
    
class UserListRequestScheme(UserBase):
    sortion_filter: Optional[bool] = Field(default=True)
    distance_filter: Optional[float] = Field(default=None)
    distance_filter_lat: Optional[float] = Field(default=0.0)
    distance_filter_long: Optional[float] = Field(default=0.0)
    sortion_field: Optional[get_attributes_enum(cls=User, drop_attrs=("avatar", ))] = Field(default=None)

    @field_validator('sortion_field', mode="after")
    def validate_sex(cls, value) -> str:
        if not value:
            return
        return value.value
    

class UserUnitListResponseScheme(UserBase):
    id: Optional[int] = Field(...)
    e_mail: Optional[constr(max_length=30)] = Field(pattern=r"[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+")
    first_name: Optional[constr(max_length=10)] = Field(default="Ivan")
    last_name: Optional[constr(max_length=15)] = Field(default="Ivanov")
    sex: Sex = Field(...)
    latitude: Optional[float] = Field(default=0)
    longitude: Optional[float] = Field(default=0)
    matches: Optional[int] = Field(...)
    matches_update: Optional[datetime] = Field(...)
    registration_date: Optional[datetime] = Field(...)
    