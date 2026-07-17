from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app import schemas, crud
from backend.app.database import get_db
from backend.app.security import get_current_user

router = APIRouter()

@router.post("/borrow/", response_model=schemas.Borrow)
def borrow_book(borrow: schemas.BorrowCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Borrow a book.
    
    :param borrow: The details of the book to be borrowed.
    :param db: Database session dependency.
    :param current_user: Currently authenticated user.
    :return: Details of the borrowed book.
    """
    return crud.borrow_book(db, borrow=borrow, user_id=current_user.id)

@router.post("/return/", response_model=schemas.Borrow)
def return_book(borrow_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Return a borrowed book.
    
    :param borrow_id: ID of the borrowed book to be returned.
    :param db: Database session dependency.
    :param current_user: Currently authenticated user.
    :return: Details of the returned book.
    """
    return crud.return_book(db, borrow_id=borrow_id, user_id=current_user.id)

@router.get("/borrowed_books/", response_model=list[schemas.Borrow])
def get_borrowed_books(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a list of all books currently borrowed by the authenticated user.
    
    :param current_user: Currently authenticated user.
    :param db: Database session dependency.
    :return: List of borrowed books.
    """
    return crud.get_borrowed_books_by_user(db, user_id=current_user.id)

@router.get("/borrow_history/", response_model=list[schemas.Borrow])
def get_borrow_history(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a list of all books borrowed by the authenticated user in the past.
    
    :param current_user: Currently authenticated user.
    :param db: Database session dependency.
    :return: List of borrow history.
    """
    return crud.get_borrow_history_by_user(db, user_id=current_user.id)