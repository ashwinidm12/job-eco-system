from dotenv import load_dotenv
import os
import requests

load_dotenv()

print("MONGO URI:", os.getenv("MONGODB_URI"))
"""
Job Eco System - FastAPI backend
Auth + Jobs API
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from pymongo import MongoClient

from auth import create_access_token, get_current_user
from models import TokenResponse, UserLogin, UserRegister

# ---------- App ----------
app = FastAPI(
    title="Job Eco System API",
    description="AI-powered job aggregation platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- MongoDB ----------
mongo_uri = os.getenv("MONGODB_URI")

if not mongo_uri:
    raise Exception("❌ MONGODB_URI not found in backend/.env")

client = MongoClient(mongo_uri)
db = client["job_ecosystem"]
users = db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

def current_user_dep(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
):
    return get_current_user(users, credentials)

# ---------- Health ----------
@app.get("/health")
def health():
    try:
        db.command("ping")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}",
        )

# ---------- REGISTER ----------
@app.post("/register")
def register(user: UserRegister):
    try:
        if users.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="User already exists")

        hashed = pwd_context.hash(user.password[:72])

        users.insert_one({
            "email": user.email,
            "password": hashed
        })

        return {"message": "User created"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}",
        )

# ---------- LOGIN ----------
@app.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    try:
        db_user = users.find_one({"email": user.email})

        if not db_user or not pwd_context.verify(
            user.password[:72],   # ✅ FIX HERE
            db_user["password"],
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(data={"sub": user.email})

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            message="Login success",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}",
        )

# ---------- Protected: profile ----------
@app.get("/me")
def me(current_user: dict = Depends(current_user_dep)):
    return {"email": current_user["email"]}

# ---------- Protected: jobs ----------
@app.get("/jobs")
def get_jobs(current_user: dict = Depends(current_user_dep)):
    try:
        url = "https://remotive.com/api/remote-jobs"
        res = requests.get(url, timeout=10)
        data = res.json()

        jobs_list = []

        for job in data["jobs"][:12]:
            jobs_list.append({
                "title": job["title"],
                "company": job["company_name"],
                "location": job["candidate_required_location"],
            })

        return {"jobs": jobs_list}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Job API failed: {str(e)}",
        )
