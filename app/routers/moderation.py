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
from app.models.moderation_action import ModerationAction
from app.services.auth import require_login

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

def update_moderation_status(
    comment_id: int,
    new_status: str,
    action_type: str,
    note: str | None,
    db: Session,
):
    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if comment is None:
        return

    old_status = comment.moderation_status

    comment.moderation_status = new_status

    action = ModerationAction(
        comment_id=comment.id,
        moderator_name="moderator",
        action_type=action_type,
        old_status=old_status,
        new_status=new_status,
        note=note,
    )

    db.add(action)
    db.commit()


@router.post("/comments/{comment_id}/approve")
def approve_comment(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_db),
):
    protection = require_login(request)

    if protection:
        return protection

    update_moderation_status(
        comment_id=comment_id,
        new_status="approved",
        action_type="approve",
        note=None,
        db=db,
    )

    return RedirectResponse(
        url="/dashboard",
        status_code=303,
    )


@router.post("/comments/{comment_id}/reject")
def reject_comment(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_db),
):
    protection = require_login(request)

    if protection:
        return protection

    update_moderation_status(
        comment_id=comment_id,
        new_status="rejected",
        action_type="reject",
        note=None,
        db=db,
    )

    return RedirectResponse(
        url="/dashboard",
        status_code=303,
    )


@router.get("/moderation-log", response_class=HTMLResponse)
def moderation_log(
    request: Request,
    db: Session = Depends(get_db),
):
    protection = require_login(request)

    if protection:
        return protection

    actions = (
        db.query(ModerationAction)
        .order_by(ModerationAction.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="moderation_log.html",
        context={
            "title": "Журнал модерації",
            "actions": actions,
        },
    )