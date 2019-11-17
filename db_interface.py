from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///fileids.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class File(Base):
    __tablename__ = 'files'

    id = Column('id', Integer, primary_key=True)
    fileid = Column('fileid', String, unique=True)
    filename = Column('filename', String)
    filesize = Column('filesize', Integer)


Base.metadata.create_all(engine)

# Example data
file_list = [
    {
        'fileid': '78',
        'filename': 'tests.txt',
        'filesize': 12
    },
    {
        'fileid': '21',
        'filename': 'test_a.txt',
        'filesize': 11
    },
    {
        'fileid': '3',
        'filename': 'test0.txt',
        'filesize': 22
    },
    {
        'fileid': '2',
        'filename': 'texts.txt',
        'filesize': 50
    },
]

session.add_all(
    [
        File(
            fileid=fl['fileid'],
            filename=fl['filename'],
            filesize=fl['filesize'])
        for fl in file_list
    ]
)

session.commit()
