import glob
import os

os.chdir(r"F:\mxy\department\国遥\数据\geonames")
file_list = glob.glob("*")
for i in file_list:
    print("++++++++++++++++++++++++++++++++++")
    print(i)
    print("==================================")
    splitext = os.path.splitext(i)
    print(splitext[0])
    print(splitext[1])
