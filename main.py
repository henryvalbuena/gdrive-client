"""Test file for manual testing and experimenting."""

import os
from pprint import pprint

from interfaces import local_files
from interfaces.log_files import LogFiles

from models.file_schema import FileSchema


# Create temporary testing folder and files
tmp_dir = 'tmp_dir'
os.mkdir(tmp_dir)  # temporary directory
print('Temp directory created\n')
# temporary files
for num in range(5):
    file = f'{tmp_dir}/tmp_file{num}.txt'
    f = open(file, 'w')
    f.close()

# Scan for the files and print to console
files = local_files.get_file_names(tmp_dir)
pprint(files)
print('')
files = local_files.get_dictionary_files(tmp_dir)
pprint(files)
print('')
files = local_files.get_directories(tmp_dir)
pprint(files)

# Remove temporary testing folder and files
for num in range(5):
    file = f'{tmp_dir}/tmp_file{num}.txt'
    os.remove(file)
os.rmdir(tmp_dir)

print('\nFiles and directories removed.\n')


# Create temporary database with table models
db = LogFiles('db/testing.db', FileSchema)
# db.create_table()
# db.create_file('someid124', 'main.txt', 1234)
# file = db.get_file_by_id('someid123')

# print the file created in the database
# pprint(file)
# print(f'filename: {f.filename} fileid: {f.fileid}')

# delete the table
table = db.drop_table(FileSchema)
if table:
    print('Table delete.')
else:
    print('Table not deleted')
print('')
