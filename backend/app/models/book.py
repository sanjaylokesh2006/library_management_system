from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(13), unique=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_date = Column(Date)
    price = Column(Float)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"