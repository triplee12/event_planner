#!/usr/bin/python3
"""User routes."""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from models.db_connect import get_session
from auths.password_hasher import HashPassword
from schemas.users import User, UserSignIn

user_router: APIRouter = APIRouter(prefix="/users", tags=["Users"])
hash_password: HashPassword = HashPassword()


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: User, session=Depends(get_session)):
    """User sign up route."""
    if session.get(User, data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email already exists."
        )
    
    hash_user_pwd: str = hash_password.create_hash(data.password)
    data.password = hash_user_pwd
    session.add(data)
    session.commit()
    session.refresh(data)
    return {"message": "Signed up successfully"}


@user_router.post("/login")
async def login(user: UserSignIn, session=Depends(get_session)):
    """User login route."""
    statement = select(User)
    users = session.exec(statement).all()
    for usr in users:
        if user.email not in usr.email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist."
            )

        if usr.password != hash_password.verify_hash(
            user.password, usr.password
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials"
            )
    return {"message": "Signed in successfully"}


@user_router.get("/")
async def get_users(session=Depends(get_session)):
    """Get all users."""
    statement = select(User)
    users = session.exec(statement).all()
    return users


@user_router.get("/{email}")
async def get_user_by_email(email: str, session=Depends(get_session)):
    """Get a user by email."""
    statement = select(User)
    users = session.exec(statement).all()
    for user in users:
        if email in user.email:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User does not exist."
    )
