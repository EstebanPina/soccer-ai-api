from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import user
from app.api.v1.endpoints import favorite
from app.api.v1.endpoints import sportsdb
from app.api.v1.endpoints import soccer_matches
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.get("/")
def health_check():
    return {"message": "API is running"}

app.include_router(auth.router, prefix="/api_soccer/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api_soccer/v1/user", tags=["user"])
app.include_router(favorite.router, prefix="/api_soccer/v1/favorite", tags=["favorite"])
app.include_router(sportsdb.router, prefix="/api_soccer/v1/sportsdb", tags=["sportsdb"])
app.include_router(soccer_matches.router, prefix="/api_soccer/v1/soccer_matches", tags=["soccer_matches"])
