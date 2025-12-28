from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Note
from routes.user_routes import get_current_user
from sqlalchemy import or_
from fastapi import Query
from schemas import NoteCreate


router = APIRouter(prefix="/notes", tags=["Notes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_note(note: NoteCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content, user_id=user.id)
    db.add(new_note)
    db.commit()
    return {"msg": "Note created"}

@router.get("/")
def get_notes(
    search: str = "",
    skip: int = 0,
    limit: int = 5,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Note).filter(
        Note.user_id == user.id,
        or_(Note.title.contains(search), Note.content.contains(search))
    ).offset(skip).limit(limit).all()

@router.delete("/{note_id}")
def delete_note(note_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"msg": "Note deleted"}
