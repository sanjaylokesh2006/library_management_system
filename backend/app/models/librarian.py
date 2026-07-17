from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Librarian(Base):
    __tablename__ = 'librarians'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f'<Librarian(username={self.username}, email={self.email})>'

    @property
    def full_name(self) -> str:
        """Return the full name of the librarian."""
        return self.username

    async def authenticate(self, password: str) -> bool:
        """Check if the provided password is correct."""
        # This should be replaced with a secure password hashing and verification mechanism
        return self.hashed_password == password

    async def has_permission(self, permission: str) -> bool:
        """Check if the librarian has the specified permission."""
        # Implement permission checking logic here
        return self.is_superuser or permission in ['manage_books', 'manage_users']