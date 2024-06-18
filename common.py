import pathlib
import os

def file_cleaner():
    #remove files txt to cleanup

    dir_name = pathlib.Path().resolve()
    #dir_name = "/Users/ben/downloads/"
    get_file_in_directory = os.listdir(dir_name)
    for item in get_file_in_directory:
        if item.endswith(".txt"):
            if(item != "final_result.txt"):
                os.remove(os.path.join(dir_name, item))
        elif item.endswith(".dat"):
                os.remove(os.path.join(dir_name, item))