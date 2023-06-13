import os

import pandas as pd

# read_path_name = input("Select your read_path :")
read_path_name = "E:\WorkSpace\pyWorkSpace\pyProject\detection"
las_files = os.listdir(read_path_name)
print("The file list is:", las_files)
index = 0
for item in las_files:
    if not item.endswith(".las"):
        print("-------------------------------")
        print("Now the file isnt las file: ", item)
        continue

    index = index + 1
    case_name = item.strip('.las')
    print("-------------------------------")
    print("Now the files being processed are of: ", case_name)

    original_data = pd.read_csv(os.path.join(read_path_name, item), header=0)
    data = original_data.to_numpy()

    column_name = original_data.columns.values
    column_names = column_name[0].split()

    wash_data = []
    wash_data.append(column_names)

    print("Begin transferring...")
    for idx in range(len(data)):
        data[idx][0] = (data[idx][0].split())
        las_file_washed = [float(x) for x in data[idx][0]]
        wash_data.append(las_file_washed)
    print("Finish transferring!")

    print("Begin writing...")
    pandata = pd.DataFrame(wash_data)
    pandata.to_csv(os.path.join(read_path_name, case_name + "_las.csv"), header=False)
    print(f"Finish writing {index} / {len(las_files)}.")
