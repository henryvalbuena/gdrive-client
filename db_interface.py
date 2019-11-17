from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, OperationalError

from models import FileSchema, Base

# For testing
DEBUG = False


class LogFiles:
    def __init__(self, model):
        self.model = model
        self.engine = create_engine('sqlite:///fileids.db', echo=DEBUG)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = Base.metadata.create_all(self.engine)
        if self.Base is None:
            self.Base = Base
            self.Base.metadata.bind = self.engine

    def create_file(self, fileid, filename, filesize):
        try:
            self.session.add(
                self.model(fileid=fileid, filename=filename, filesize=filesize)
            )
            self.session.commit()
        except IntegrityError:
            print('Duplicate values')
        except OperationalError:
            print('Db has no tables')
        finally:
            self.session.close()

    def create_files(self, file_list):
        try:
            self.session.add_all(
                [
                    self.model(
                        fileid=fl['fileid'],
                        filename=fl['filename'],
                        filesize=fl['filesize'])
                    for fl in file_list
                ]
            )
            self.session.commit()
        except IntegrityError:
            print('Duplicate values')
        except OperationalError:
            print('Db has no tables')
        finally:
            self.session.close()

    def get_file_by_id(self, fileid):
        try:
            f = list(self.session.query(self.model).filter(
                self.model.fileid == fileid
                ))[0]
            if DEBUG:
                print(f'name: {f.filename} id: {f.fileid} size: {f.filesize}')
            return f
        except OperationalError:
            print('Db has no tables')
        finally:
            self.session.close()

    def get_files(self):
        try:
            res = self.session.query(self.model)
            files = list()
            for f in res:
                if DEBUG:
                    s = f'name: {f.filename} id: {f.fileid} size: {f.filesize}'
                    print(s)
                files.append(f)
            return files
        except OperationalError:
            print('Db has no tables')
        finally:
            self.session.close()

    def drop(self, model):
        for table in self.Base.metadata.sorted_tables:
            if str(table) == model:
                table.drop(checkfirst=True)
                return True
                if DEBUG:
                    print(f'Table {str(model)} has been dropped')
        return False


lf = LogFiles(FileSchema)
lf.create_files(
    [
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
)
lf.get_files()
# lf.drop(None)
