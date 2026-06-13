from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import Base
from app.database import engine
from app.models.comment import Comment
from app.routers.comments import router as comments_router
from app.models.moderation_action import ModerationAction
from app.routers.moderation import router as moderation_router
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.statistics import get_statistics
from starlette.middleware.sessions import SessionMiddleware
from app.config import SECRET_KEY
from app.routers.auth import router as auth_router
from app.services.auth import require_login

app = FastAPI(title="Toxicity Moderation")

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(comments_router)

app.include_router(moderation_router)

app.include_router(auth_router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "title": "Головна",
        },
    )


@app.get("/statistics", response_class=HTMLResponse)
def statistics(
    request: Request,
    db: Session = Depends(get_db),
):
    protection = require_login(request)

    if protection:
        return protection
    
    stats = get_statistics(db)

    return templates.TemplateResponse(
        request=request,
        name="statistics.html",
        context={
            "title": "Статистика",
            "stats": stats,
        },
    )


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Application is running",
    }