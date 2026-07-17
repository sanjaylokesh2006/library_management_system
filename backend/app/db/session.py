from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Database URL configuration
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a session class bound to this engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()

def get_db() -> Session:
    """
    Dependency function to provide a database session.
    
    Yields:
        Session: A SQLAlchemy session instance.
        
    Raises:
        Exception: If an error occurs while creating the session.
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        raise Exception("Failed to create database session") from e
    finally:
        if db:
            db.close()

# Example usage of the get_db dependency in a FastAPI route
from fastapi import Depends, HTTPException

async def read_items(db: Session = Depends(get_db)):
    """
    Endpoint to fetch items from the database.
    
    Args:
        db (Session): The database session provided by the dependency injection.
        
    Returns:
        List[Item]: A list of item objects fetched from the database.
        
    Raises:
        HTTPException: If no items are found or an error occurs.
    """
    try:
        items = db.query(Item).all()
        if not items:
            raise HTTPException(status_code=404, detail="Items not found")
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# Example model definition (assuming Item is a SQLAlchemy ORM model)
from sqlalchemy import Column, Integer, String

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# Example migration command (to be run in the Alembic environment)
# alembic revision --autogenerate -m "create items table"