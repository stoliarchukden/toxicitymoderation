from fastapi import Request
from fastapi.responses import RedirectResponse


def require_login(request: Request):
    user = request.session.get("user")

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    return None