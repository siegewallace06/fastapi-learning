from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database located on localhost as root user with password root on 3306 port
DATABASE_URL = "mysql+pymysql://root:root@mysql-fastapi:3306/fastapi_blog"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
