import os
import zipfile


def un_zip(file_name):
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")

    for names in zip_file.namelist():
        zip_file.extract(names, file_name + "_files/")
    zip_file.close()

un_zip("/Users/ming/Downloads/AFG_rrd/igsg0070.22i.Z")