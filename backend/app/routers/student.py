
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.database import get_db
from app.models.department import Department
from app.models.student import Student
from app.models.user import User
from app.schemas.student import (
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate,
)


router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/protected")
def student_protected(
    current_user: User = Depends(require_role("STUDENT")),
):
    return {
        "message": "Student access granted",
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }


@router.get("/me", response_model=StudentProfileResponse)
def get_my_profile(
    current_user: User = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile has not been created yet",
        )

    return profile


@router.patch("/me", response_model=StudentProfileResponse)
def update_my_profile(
    payload: StudentProfileUpdate,
    current_user: User = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile has not been created yet",
        )

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile


@router.post(
    "/profiles",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student_profile(
    payload: StudentProfileCreate,
    current_user: User = Depends(require_role("HOD")),
    db: Session = Depends(get_db),
):
    student_user = (
        db.query(User)
        .filter(User.id == payload.user_id)
        .first()
    )

    if student_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student user account not found",
        )

    if student_user.role != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The selected user does not have the STUDENT role",
        )

    if not student_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The student user account is inactive",
        )

    department = (
        db.query(Department)
        .filter(Department.id == payload.department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    existing_profile = (
        db.query(Student)
        .filter(
            (Student.user_id == payload.user_id)
            | (Student.roll_number == payload.roll_number)
        )
        .first()
    )

    if existing_profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "A profile already exists for this user "
                "or roll number"
            ),
        )

    profile = Student(**payload.model_dump())

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get(
    "/profiles",
    response_model=list[StudentProfileResponse],
)
def list_student_profiles(
    current_user: User = Depends(require_role("HOD")),
    db: Session = Depends(get_db),
):
    return db.query(Student).order_by(Student.id).all()


@router.get(
    "/profiles/{student_id}",
    response_model=StudentProfileResponse,
)
def get_student_profile(
    student_id: int,
    current_user: User = Depends(require_role("HOD")),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )

    return profile


@router.patch(
    "/profiles/{student_id}",
    response_model=StudentProfileResponse,
)
def update_student_profile(
    student_id: int,
    payload: StudentProfileUpdate,
    current_user: User = Depends(require_role("HOD")),
    db: Session = Depends(get_db),
):
    profile = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile
