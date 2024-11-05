import os
from collections import Counter

import globals as gl
from models import FileInfo
import helpers as hlp


def compare_with_original(dir_orig: str, dir_curr: str) -> int:
  files_orig = [FileInfo(path=file, name=os.path.basename(file),) for file in hlp.get_all_files(dir_orig)]
  files_curr =  [FileInfo(path=file, name=os.path.basename(file)) for file in hlp.get_all_files(dir_curr)]
  names_curr = {file.name for file in files_curr}
  files_diff = {file for file in files_orig if file.name not in names_curr}

  print("Original: ", dir_orig)
  print("Current : ", dir_curr)
  print(f"Files in original but not in current ({len(files_diff)}):")

  counter = Counter([file.name for file in files_orig])
  duplicates = [item for item, count in counter.items() if count > 1]
  if len(duplicates) > 0:
    print("Duplicates in original:")
    for file in duplicates:
      print(file)
  else:
    print("Duplicates in original are missing!")
  print()

  for file in files_diff:
    _, tail = os.path.splitdrive(file.path)
    tail = tail.replace('\\', '_')
    symlink_name = os.path.join(gl.dir_links_deleted_from_original, tail)
    #print(symlink_name)
    os.symlink(file.path, symlink_name)
  return len(files_diff)


if __name__ == '__main__':
  dir_orig = r"F:\_From_Boise_2024_original"
  dir_curr = r"F:\Photo_Boise\_From_Boise_2024"

  hlp.delete_all_files_in_directory(gl.dir_links_deleted_from_original)

  n_diff = 0
  for subfolder in gl.subfolders:
    n_diff += compare_with_original(os.path.join(dir_orig, subfolder), os.path.join(dir_curr, subfolder))
  print(f"Total differences: {n_diff}")
  print(f"Links to files deleted from the original are created in the folder {gl.dir_links_deleted_from_original}.")
  input("\nPress Enter to continue...")