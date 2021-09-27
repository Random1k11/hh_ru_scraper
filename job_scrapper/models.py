import datetime

from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, Text, Boolean
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("DB_CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Vacancy(Base):
    __tablename__ = "vacancy"

    id = Column(Integer, primary_key=True)
    title = Column('title', String(256))
    salary = Column('salary', String(256), nullable=True)
    company = Column('company', String(256))
    company_link = Column('company_link', Text(), nullable=True)
    location = Column('location', Text(), nullable=True)
    employment_mode = Column('employment_mode', String(256), nullable=True)
    description = Column('description', Text(), nullable=True)
    tags = Column('tags', Text(), nullable=True)
    creation_time = Column('creation_time', Text(), nullable=True)
    link = Column('link', Text())
    platform = Column('platform', String(256))
    scrapped_at = Column(Date, default=datetime.datetime.now)
    posted = Column(Boolean, default=False)
