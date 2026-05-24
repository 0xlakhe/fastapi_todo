import sqlite3
from fastapi import APIRouter, HTTPException, status
from models.user import UserLogin, UserRegister
from database import create_user, get_user
from auth import hash_password, verify_password, create_token

auth_router = APIRouter()


@auth_router.post("/auth/register")
def c_user(user: UserRegister):
    details = user.model_dump()
    pass_word = hash_password(details["password"])
    try:
        create_user(details["username"], details["email"], pass_word)
    except sqlite3.IntegrityError as e:
        print(f"Database conflict: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )
    return "user created successfully"


@auth_router.post("/auth/login")
def l_user(user: UserLogin):
    details = user.model_dump()
    login_details = get_user(details["identifier"])

    if login_details is None:
        raise HTTPException(status_code=404, detail="No such user")

    check_password = verify_password(details["password"], login_details["password"])
    if not check_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return create_token({"user_id": login_details["id"]})
