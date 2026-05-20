"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from .models import Base


class Database:
    """Database connection manager"""
    
    def __init__(self, database_url: str = "sqlite:///quantity_surveying.db"):
        """
        Initialize database connection
        
        Args:
            database_url: SQLAlchemy database URL
        """
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._session: Optional[Session] = None
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
        print("Database tables created successfully")
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(bind=self.engine)
        print("Database tables dropped")
    
    def get_session(self) -> Session:
        """Get database session"""
        if self._session is None:
            self._session = self.SessionLocal()
        return self._session
    
    def close_session(self):
        """Close database session"""
        if self._session:
            self._session.close()
            self._session = None
    
    def __enter__(self):
        """Context manager entry"""
        return self.get_session()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_session()


# Singleton instance
_db_instance: Optional[Database] = None


def get_database(database_url: str = "sqlite:///quantity_surveying.db") -> Database:
    """
    Get database singleton instance
    
    Args:
        database_url: SQLAlchemy database URL
        
    Returns:
        Database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(database_url)
    return _db_instance
