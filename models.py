from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileSchema(Base):
    __tablename__ = 'files'

    id = Column('id', Integer, primary_key=True)
    fileid = Column('fileid', String, unique=True)
    filename = Column('filename', String)
    filesize = Column('filesize', Integer)


class TempFileSchema(Base):
    __tablename__ = 'test_files'

    id = Column('id', Integer, primary_key=True)
    fileid = Column('fileid', String, unique=True)
    filename = Column('filename', String)
    filesize = Column('filesize', Integer)
