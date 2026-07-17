from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud import book_crud
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

class BookService:
    def __init__(self, db: Session):
        self.db = db

    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Retrieve a book by its ID.

        Args:
            book_id (int): The ID of the book to retrieve.

        Returns:
            Optional[Book]: The retrieved book or None if not found.
        """
        return await book_crud.get_book_by_id(self.db, book_id=book_id)

    async def get_books(self) -> List[Book]:
        """
        Retrieve all books.

        Returns:
            List[Book]: A list of all books.
        """
        return await book_crud.get_books(self.db)

    async def create_book(self, book_in: BookCreate) -> Book:
        """
        Create a new book.

        Args:
            book_in (BookCreate): The data to create the book with.

        Returns:
            Book: The created book.
        """
        return await book_crud.create_book(self.db, book_in=book_in)

    async def update_book(self, book_id: int, book_in: BookUpdate) -> Optional[Book]:
        """
        Update an existing book.

        Args:
            book_id (int): The ID of the book to update.
            book_in (BookUpdate): The data to update the book with.

        Returns:
            Optional[Book]: The updated book or None if not found.
        """
        return await book_crud.update_book(self.db, book_id=book_id, book_in=book_in)

    async def delete_book(self, book_id: int) -> bool:
        """
        Delete a book by its ID.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            bool: True if the book was deleted, False otherwise.
        """
        return await book_crud.delete_book(self.db, book_id=book_id)