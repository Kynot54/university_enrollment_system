import boto3
from fastapi import APIRouter, Depends, HTTPException
from api.services.notifications.main import (
    get_db, validate_student_id, validate_section_id, validate_email, validate_web_hook
)
from share.notifications.notifications import (
    addSubscription, listSubscriptions, removeSubscription, is_student_subscribed
)

router = APIRouter()

@router.post("/notify/subscribe")
def subscribe_student(
    email: str | None = None,
    web_hook: str | None = None,
    section_id: int = Depends(validate_section_id),
    student_id: int = Depends(validate_student_id)
):
    if email:
        email = validate_email(email)

    if web_hook:
        web_hook: validate_web_hook(web_hook)
    
    addSubscription(str(student_id), str(section_id), email, web_hook)

    return {"details": f"Student of ID #: {str(student_id)}, subscribed to section #{str(section_id)}"}


@router.get("/notify/subscriptions")
def list_student_subscriptions(
    student_id: int = Depends(validate_student_id),
    db: boto3.session.Session = Depends(get_db)
):
    subscriptions = listSubscriptions(student_id)

    if not subscriptions:
        raise HTTPException(status_code=404, detail="Student is not subscribed to any classes") 
    
    subscription_list = []

    for section in subscriptions:
        subscription_list.append({"section_id": section.decode("utf-8")})
    
    return {"subscriptions": subscription_list}

@router.delete("/notify/unsubscribe")
def unsubscribe_student(
    student_id: int = Depends(validate_student_id),
    section_id: int = Depends(validate_section_id),
    db: boto3.session.Session = Depends(get_db)
):
    if not is_student_subscribed(student_id, section_id):
        raise HTTPException(status_code=404, detail="Student is not subscribed to this class") 

    removeSubscription(str(student_id), str(section_id))

    return {"details": f"Student of ID #: {str(student_id)}, unsubscribed from section #{str(section_id)}"}
