from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, session_maker
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError # Import SQLAlchemyError for error handling

# Load environment variables
load_dotenv()

# Retrieve DATABASE_URI from .env
DATABASE_URI = os.getenv('DATABASE_URI')

# Create engine
try:
    engine = create_engine(DATABASE_URI)
except SQLAlchemyError as e:
    print(f"An error occurred while connecting to the database: {e}")
    # Depending on the application, you might want to exit or handle this differently.
    
# Setup a SessionLocal class
try:
    # The name `scoped_ipfs_session_factory` seems to be a typo or project-specific. Replacing with `scoped_session`.
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
except SQLAlchemyError as e:
    print(f"An error occurred while setting up the session factory: {e}")

# Example Usage
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()

# Example function to demonstrate error handling in a database operation
def example_database_operation():
    db_session = next(get_db(), None)
    if db_session is None:
        print("Failed to create a database session.")
        return
    
    try:
        # Your database operations here, e.g., querying, adding instances
        # Example: result = db_session.query(MyModel).filter_by(name="example").first()
        pass
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        # Make sure to rollback in case of an error to avoid incomplete database transactions
        db_session.rollback()
    finally:
        db_session.close()