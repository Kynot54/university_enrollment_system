import logging.config
import boto3
import re

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic_settings import BaseSettings


class Settings(BaseSettings, env_file=".env", extra="ignore"):
    enrollment_database: str
    logging_config: str


settings = Settings()
app = FastAPI()

def get_logger():
    return logging.getLogger(__name__)

def get_db():
    return boto3.resource('dynamodb', endpoint_url=settings.enrollment_database)

def validate_student_id(
    req: Request,
    student_id: int = None,
    db: boto3.session.Session = Depends(get_db)
):
    if student_id is None:
        username = req.headers.get("x-username")
        users = db.Table("students").scan(AttributesToGet=['id', 'username'])["Items"]
        user = next((_ for _ in users if _.get("username") == username), None)
        if user is None:
            raise HTTPException(status_code=404, detail="Student of username " + str(username) + " not found")
        student_id = user["id"]
    else:
        if db.Table("students").get_item(Key={"id": student_id}) is None:
            raise HTTPException(status_code=404, detail="Student of id " + str(id) + " not found")
    return student_id

def validate_section_id(
    section_id: int, 
    db: boto3.session.Session = Depends(get_db)
):
    if db.Table("sections").get_item(Key={"id": section_id}) is None:
        raise HTTPException(status_code=404, detail="Section of id " + str(section_id) + " not found")
    return section_id

def validate_email(
    email : str
):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if not re.fullmatch(regex, email):
        raise HTTPException(status_code=400, detail="Email address is invalid") 
    return email

def validate_web_hook(
    web_hook : str
):
    if not web_hook.startswith("https://") and not web_hook.startswith("http://"):
        raise HTTPException(status_code=400, detail="Web hook URL is invalid") 
    return web_hook


logging.config.fileConfig(settings.logging_config, disable_existing_loggers=False)

from api.services.notifications.notification import router as notification_router
app.include_router(notification_router) 
