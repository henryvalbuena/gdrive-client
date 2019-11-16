from sqlalchemy import create_engine, MetaData, Table, Column, \
    Integer, String


engine = create_engine('sqlite:///fileids.db', echo=True)
meta = MetaData()

files = Table(
    'files', meta,
    Column('id', Integer, primary_key=True),
    Column('fileid', String, unique=True),
    Column('filename', String),
    Column('filesize', Integer),
)
meta.create_all(engine)
insert = files.insert().values(
    fileid='12345',
    filename='test1.txt',
    filesize=999)
conn = engine.connect()
result = conn.execute(insert)
