from contextlib import contextmanager
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import DATABASE_URL

from threading import local

metadata = MetaData()
thread_local = local()

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    echo=True,  # Установите False в production
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(metadata=metadata)


@contextmanager
def get_db():
    db = session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
