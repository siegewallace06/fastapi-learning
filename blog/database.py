from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database located on localhost as root user with password root on 3306 port
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/fastapi_blog"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
