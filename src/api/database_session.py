from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import Constants

engine = create_engine(f"postgresql://{Constants.DB_USER}:{Constants.DB_PASS}@{Constants.DB_HOST}/{Constants.DB_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__=="__main__":
    """ Handly for waiting until database is online.
        Will wait 1 second after each connection attempt,
        total 5 attempts. Throws an exception if all tries 
        fail.
    """
    import time

    is_online = False

    for i in range(5):
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            is_online = True
            break
        except Exception:
            pass
            
        time.sleep(1)
    
    if not is_online:
        raise Exception("Database not connected")