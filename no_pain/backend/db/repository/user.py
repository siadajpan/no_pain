from sqlalchemy.orm import Session

from no_pain.backend.core.hashing import Hasher
from no_pain.backend.db.models.user import User
from no_pain.backend.schemas.user import UserCreate
import secrets
from datetime import datetime, timedelta
from no_pain.backend.db.models.user_verification import UserVerification
from no_pain.backend.db.models.user_role import UserRole
from no_pain.backend.db.models.doctor import Doctor
from no_pain.backend.db.models.patient import Patient
from no_pain.backend.db.models.practice import Practice


def create_new_user(user: UserCreate, db: Session):
    first_name = user.first_name
    last_name = user.last_name
    
    if user.role == UserRole.PRACTICE:
        if not user.practice_name:
            raise ValueError("Practice Name is required")
        first_name = user.practice_name
        last_name = ""  # No last name for practice

    new_user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        first_name=first_name,
        last_name=last_name,
        is_active=False,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.role == UserRole.PATIENT:
        patient = Patient(user_id=new_user.id)
        db.add(patient)
    elif user.role == UserRole.DOCTOR:
        doctor = Doctor(user_id=new_user.id, profile_picture=user.profile_picture)
        db.add(doctor)
    elif user.role == UserRole.PRACTICE:
        practice = Practice(
            user_id=new_user.id,
            street_address=user.street_address,
            city=user.city,
            postcode=user.postcode,
            phone=user.phone,
            name=user.practice_name
        )
        db.add(practice)
    
    db.commit()

    return new_user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).one_or_none()
    return user


def update_user_password(user, new_password, db: Session):
    hashed_password = Hasher.get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    return user


def create_verification_token(user_id: int, db: Session):
    # 1. Generate a secure random string
    token = secrets.token_urlsafe(32)

    # 2. Set expiration (e.g., 24 hours from now)
    expires_at = datetime.utcnow() + timedelta(hours=24)

    # 3. Save to the new table
    db_verification = UserVerification(
        user_id=user_id, token=token, expires_at=expires_at
    )

    db.add(db_verification)
    db.commit()
    return token
