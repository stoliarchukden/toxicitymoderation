from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comment import Comment
from app.services.classifier import predict_toxicity
from app.services.explanation import explain_comment
from app.services.auth import require_login


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    protection = require_login(request)

    if protection:
        return protection

    comments = (
        db.query(Comment)
        .order_by(Comment.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Панель модератора",
            "comments": comments,
        },
    )

@router.get("/comments/{comment_id}", response_class=HTMLResponse)
def comment_detail(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_db),
):
    protection = require_login(request)

    if protection:
        return protection

    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if comment is None:
        return RedirectResponse(
            url="/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="comment_detail.html",
        context={
            "title": "Деталі коментаря",
            "comment": comment,
        },
    )

@router.get("/add-comment", response_class=HTMLResponse)
def add_comment_page(request: Request):
    
    protection = require_login(request)

    if protection:
        return protection
    
    return templates.TemplateResponse(
        request=request,
        name="add_comment.html",
        context={
            "title": "Додати коментар",
        },
    )


@router.post("/add-comment")
def add_comment(
    author_name: str = Form(...),
    text: str = Form(...),
    db: Session = Depends(get_db),
):
    prediction = predict_toxicity(text)
    explanations = explain_comment(text)

    comment = Comment(
        author_name=author_name,
        text=text,
        model_label=prediction["label"],
        toxicity_score=prediction["score"],
        explanation_json=explanations,
        moderation_status="pending",
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return RedirectResponse(
        url="/dashboard",
        status_code=303,
    )