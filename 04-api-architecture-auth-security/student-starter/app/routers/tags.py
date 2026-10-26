"""📌 6일차 실습"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.tag import TagCreate, TagOut
from app.services import tag_service
from app.dependencies import get_current_user

router = APIRouter(prefix="/tags", tags=["태그"])


@router.get("", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """TODO: tag_service.list_tags 호출."""
    raise NotImplementedError


@router.post("", response_model=TagOut, status_code=201)
def create_tag(payload: TagCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    """TODO: tag_service.create_tag 호출."""
    raise NotImplementedError
