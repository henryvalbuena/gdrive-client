"""Database interface module."""

from models.file_schema import Base, FileSchema

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# For testing
DEBUG = False


class LogFiles:
    """Database interface.

    Interface to log file id, name, and size in a database.

    Methods:
        create_file: creates a log in the database
        create_files: creates multiple logs in the database
        get_file_by_id: returns an object with the file metadata
        get_files: returns a list of objects with file medatada
        update_file: updates a file based on the file id provided
        remove_file_by_id: removes a file object from the database
        drop: drops a table from the database

    """

    def __init__(self, db, model):
        """Class initialization.

        Initialize LogFiles class with the parameters below.

        Args:
            db: database to create if it doesn't exists
            model: table schema to create if it doesn't exists

        """
        self.model = model
        self.engine = create_engine(f'sqlite:///{db}', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_table(self, model):
        """Create the specified table.

        Creates the specified table from the arguments into the database
        if exists.

        Args:
            model: model name of the schema/table as a string

        """
        self.model = model
        self.Base = Base.metadata.create_all(self.engine)
        if self.Base is None:
            self.Base = Base
            self.Base.metadata.bind = self.engine

    def drop_table(self, model):
        """Drop the specified table.

        Drops the specified table from the arguments into the database
        if exists.

        Args:
            model: model name of the schema/table as a string

        Returns:
            True if the table was found and dropped, else False

        """
        for table in self.Base.metadata.sorted_tables:
            if str(table) == model:
                # table.drop(checkfirst=True)
                table.drop()
                return True
                if DEBUG:
                    print(f'Table {str(model)} has been dropped')
        return False

    def create_file(self, fileid, filename, filesize):
        """Create a file object in the database.

        Logs a file with the passed arguments in the database.

        Args:
            fileid: gdrive file id
            filename: file name
            filesize: file size in bytes

        Raises:
            IntegrityError, OperationalError

        """
        try:
            self.session.add(
                self.model(fileid=fileid, filename=filename, filesize=filesize)
            )
            self.session.commit()
        except OperationalError:
            self.session.rollback()
            raise
        except IntegrityError:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_files(self, file_list):
        """Create multiple file objects in the database.

        Creates multiple files from the file list passed as
        argument.

        Args:
            file_list: list of file objects

        Raises:
            IntegrityError, OperationalError

        """
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
        except OperationalError:
            self.session.rollback()
            raise
        except IntegrityError:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_file_by_id(self, fileid):
        """Get file by id.

        Returns a file object if file id matches. Otherwise, returns None.

        Args:
            fileid: gdrive file id

        Raises:
            NoResultFound, OperationalError

        Returns:
            File object in FileSchema namespace.

        """
        try:
            f = self.session.query(self.model).filter_by(
                fileid=fileid
            ).one()
            return f
        except OperationalError:
            raise
        except NoResultFound:
            raise
        finally:
            self.session.close()

    def get_files(self):
        """Get all the files in the database.

        Returns a list of object files from the database, if found, else an
        empty list.

        Raises:
            OperationalError

        Returns:
            List of files if there's any, otherwise an empty list.

        """
        try:
            f = self.session.query(self.model).all()
            return f
        except OperationalError:
            raise
        finally:
            self.session.close()

    def remove_file_by_id(self, fileid):
        """Remove a file by the id.

        Removes a file from the database if the id macthes. It returns,
        True if succeeds, otherwise, False.

        Args:
            fileid: gdrive file id

        Raises:
            OperationalError, NoResultFound

        """
        try:
            file = self.get_file_by_id(fileid)
            self.session.delete(file)
            self.session.commit()
        except OperationalError:
            self.session.rollback()
            raise
        except NoResultFound:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_file(self, curfileid, fileid, filename, filesize):
        """Update an existing file.

        Updates a file based on the file id if found.

        Args:
            fileid: gdrive file id
            filename: file name
            filesize: file size in bytes

        Raises:
            OperationError, NoResultFound

        """
        try:
            f = self.session.query(FileSchema).filter(
                self.model.fileid == curfileid
            )
            f.update(
                {
                    'fileid': fileid,
                    'filename': filename,
                    'filesize': filesize
                }
            )
            f.one().fileid
            self.session.commit()
        except OperationalError:
            self.session.rollback()
            raise
        except NoResultFound:
            self.session.rollback()
            raise
        finally:
            self.session.close()


if DEBUG:
    DB = 'db/fileids.db'
    lf = LogFiles(DB, FileSchema)
    lf.create_table(FileSchema)
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
    files = lf.get_files()
    for file in files:
        print(file.fileid, file.filename)
