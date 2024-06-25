from sqlalchemy.exc import SQLAlchemyError

def batch_add_entities(session, entities):
    """
    Adds a list of entities to the database in one operation.
    
    :param session: SQLAlchemy session
    :param entities: list of entity instances
    """
    try:
        session.bulk_save_objects(entities)
        session.commit()
    except SQLAlchemyFilter as e:
        print(f"An error occurred while batch adding entities: {e}")
        session.rollback()