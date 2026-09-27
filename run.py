from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.users.urls import users_bp
from app.users.services import get_all_surveys
from app.utils.excel import surveys_to_xlsx
from app.utils.exceptions import error_handlers
from db import init_db
from db.session import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(app)
    yield


app = FastAPI(lifespan=lifespan)

error_handlers(app)

app.include_router(users_bp)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def url_for(name: str, filename: str | None = None, **kwargs):
    if name == "static" and filename:
        return f"/static/{filename}"
    return app.url_path_for(name, **kwargs)


templates.env.globals["url_for"] = url_for


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/anketa", response_class=HTMLResponse)
def view_surveys(request: Request, db: Session = Depends(get_db)):
    surveys = get_all_surveys(db)
    return templates.TemplateResponse(
        "surveys.html",
        {"request": request, "surveys": surveys},
    )


@app.get("/anketa/export.xlsx")
def export_surveys_xlsx(db: Session = Depends(get_db)):
    surveys = get_all_surveys(db)
    buffer = surveys_to_xlsx(surveys)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=anketa.xlsx"},
    )


if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=5000, reload=True)