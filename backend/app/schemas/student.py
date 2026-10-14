
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentProfileCreate(BaseModel):
    user_id: int = Field(gt=0)
    department_id: int = Field(gt=0)
    roll_number: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    academic_year: int = Field(ge=1)
    academic_phase: str = Field(pattern=r"^(FE|SE|TE|BE)$")
    semester: int = Field(ge=1, le=8)
    cgpa: float | None = Field(default=None, ge=0, le=10)
    graduation_year: int = Field(ge=2000, le=2100)


class StudentProfileUpdate(BaseModel):
    first_name: str | None = Field(
        default=None, min_length=1, max_length=100
    )
    last_name: str | None = Field(
        default=None, min_length=1, max_length=100
    )
    academic_year: int | None = Field(default=None, ge=1)
    academic_phase: str | None = Field(
        default=None, pattern=r"^(FE|SE|TE|BE)$"
    )
    semester: int | None = Field(default=None, ge=1, le=8)
    cgpa: float | None = Field(default=None, ge=0, le=10)
    graduation_year: int | None = Field(
        default=None, ge=2000, le=2100
    )


class StudentProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    department_id: int
    roll_number: str
    first_name: str
    last_name: str
    academic_year: int
    academic_phase: str
    semester: int
    cgpa: float | None
    graduation_year: int
    created_at: datetime
    updated_at: datetime
