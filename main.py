from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="My API",
    description="REST API built with FastAPI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Change to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory "database" (replace with real DB later) ────────────────────────
fake_db: dict[int, dict] = {
    1: {"id": 1, "name": "Alice",  "email": "alice@example.com", "created_at": "2024-01-01"},
    2: {"id": 2, "name": "Bob",    "email": "bob@example.com",   "created_at": "2024-01-02"},
}
next_id = 3

# ── Schemas (Pydantic models) ─────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {"message": "API is running", "docs": "/docs"}


@app.get("/users", response_model=list[UserResponse], tags=["Users"])
async def get_all_users():
    """Return all users."""
    return list(fake_db.values())


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: int):
    """Get a single user by ID."""
    user = fake_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(body: UserCreate):
    """Create a new user."""
    global next_id
    user = {
        "id": next_id,
        "name": body.name,
        "email": body.email,
        "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
    }
    fake_db[next_id] = user
    next_id += 1
    return user


@app.patch("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(user_id: int, body: UserUpdate):
    """Partially update a user."""
    user = fake_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    if body.name  is not None: user["name"]  = body.name
    if body.email is not None: user["email"] = body.email
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(user_id: int):
    """Delete a user."""
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    del fake_db[user_id]
