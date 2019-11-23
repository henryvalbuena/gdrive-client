"""Model schema module."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileSchema(Base):
    """Create File Schema Class."""

    __tablename__ = 'files'

    localid = Column('localid', Integer, primary_key=True)
    fileid = Column('fileid', String, unique=True)
    filename = Column('filename', String)
    filesize = Column('filesize', Integer)
