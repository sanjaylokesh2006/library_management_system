from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import schemas, crud
from backend.app.database import get_db

router = APIRouter()

@router.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book in the database.
    """
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    return crud.create_book(db=db, book=book)

@router.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of books from the database.
    """
    return crud.get_books(db=db, skip=skip, limit=limit)

@router.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single book by its ID.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """
    Update an existing book in the database.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db=db, db_obj=db_book, book=book)

@router.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book from the database.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.delete_book(db=db, db_obj=db_book)