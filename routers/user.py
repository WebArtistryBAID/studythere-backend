import os
import urllib.parse
from datetime import datetime, timezone, timedelta

import requests
from fastapi import APIRouter, Depends
from jose import jwt
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse

from utils import crud
from utils.dependencies import get_db, USER_AGENT

router = APIRouter()


@router.get("/login")
def login_redirect(redirect: str):
    # We are still within the SPA context here, so the redirect is performed by the SPA
    return {
        "target": "https://passport.seiue.com/authorize?response_type=token&client_id=" + os.environ["SEIUE_CLIENT_ID"] +
                  "&school_id=452&redirect_uri=" + urllib.parse.quote(
            os.environ["API_HOST"] + "/login/capture?redirect=" + urllib.parse.quote(redirect, safe=""), safe="")
    }


@router.get("/login/capture", response_class=HTMLResponse)
def login_capture_token(redirect: str):
    # We have been redirected back from SEIUE and is within a separate context from the SPA
    # SEIUE, for some reason, includes the access token in a hashtag, so we must use JavaScript to extract it
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Please wait...</title>
</head>
<body>
    <script>    
        if (location.hash.includes('access_token')) {
            const token = location.hash.replace('#', '')
            const match = token.match(/access_token=([^&]*)/)
            if (match && match[1]) {
                window.location.replace(`""" + os.environ[
        "API_HOST"] + """/login/exchange?token=${encodeURIComponent(match[1])}&redirect=${encodeURIComponent('""" + redirect + """')}`)
            }
        } else {
            window.location.replace('""" + os.environ["API_HOST"] + """/login/exchange?error=token')
        }
    </script>
</body>
</html>
"""


@router.get("/login/exchange")
def login_token_redirect(redirect: str, error: str | None = None, token: str | None = None,
                         db: Session = Depends(get_db)):
    if error is not None or token is None:
        return RedirectResponse(redirect + "?error=" + error, status_code=302)
    # Still in a separate context, but now we redirect back to the SPA with our custom token
    r = requests.get("https://open.seiue.com/api/v3/oauth/me",
                     headers={
                         "Authorization": f"Bearer {token}",
                         "X-School-Id": "452",
                         "User-Agent": USER_AGENT
                     })
    if r.status_code != 200:
        return RedirectResponse(redirect + "?error=profile", status_code=302)
    data = r.json()
    print(data)
    if crud.get_user(db, data["id"]) is None:
        user = crud.create_user(db, data["id"], data["usin"], data["name"], data.get("pinyin"), token, datetime.now(),
                                "")
    else:
        user = crud.update_user(db, crud.get_user(db, data["id"]), data["name"], data.get("pinyin"), token,
                                datetime.now(), "")
    crud.update_schedules_based_on_user(db, user)
    to_encode = {"name": data["name"], "seiueID": data["id"], "eduID": data["usin"], "permissions": user.permissions,
                 "exp": datetime.now(timezone.utc) + timedelta(days=30)}
    encoded = jwt.encode(to_encode, key=os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    return RedirectResponse(
        redirect + "?token=" + urllib.parse.quote(encoded, safe="") + "&name=" + urllib.parse.quote(data["name"],
                                                                                                    safe=""),
        status_code=302)
