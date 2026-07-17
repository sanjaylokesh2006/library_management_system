from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base
from backend.app.models.user import User  # Assuming User model is in models/user.py
from backend.app.models.book import Book  # Assuming Book model is in models/book.py

class BorrowRecord(Base):
    __tablename__ = 'borrow_records'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")

    def __repr__(self):
        return f"<BorrowRecord(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, borrow_date={self.borrow_date}, return_date={self.return_date})>"