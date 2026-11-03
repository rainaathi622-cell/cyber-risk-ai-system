import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.auth_schema import UserSignup, UserLogin, Token, UserResponse
from services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Simple protection against password guessing:
# after 5 wrong passwords, that email is locked for 5 minutes.
# This is kept in memory, so it resets when the server restarts.
MAX_FAILED_ATTEMPTS = 5
LOCK_SECONDS = 300
failed_logins: dict[str, list[float]] = {}


def check_not_locked(email: str) -> None:
    now = time.time()
    recent = [t for t in failed_logins.get(email, []) if now - t < LOCK_SECONDS]
    failed_logins[email] = recent
    if len(recent) >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many failed attempts. Please try again in 5 minutes.",
        )


@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    email = login_data.email
    check_not_locked(email)

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        failed_logins.setdefault(email, []).append(time.time())
        raise HTTPException(status_code=401, detail="Invalid email or password")

    failed_logins.pop(email, None)

    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}