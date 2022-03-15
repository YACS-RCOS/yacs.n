import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = os.environ.get('DB_NAME', 'yacs')
DB_USER = os.environ.get('DB_USER', None)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', None)
DB_PASS = os.environ.get('DB_PASS', None)

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__=="__main__":
    #   Handly for waiting until database is online.
    #   Will wait 1 second after each connection attempt,
    #   total 5 attempts. Throws an exception if all tries 
    #   fail.
    import time

    is_online = False

    for i in range(5):
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            is_online = True
            break
        except Exception as err:
            print(err)
            
        time.sleep(1)
    
    if not is_online:
        raise Exception("Database not connected")