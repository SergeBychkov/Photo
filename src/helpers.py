import os

import globals as gl


def remove_extended_path_prefix(path: str) -> str:
  if path.startswith('\\\\?\\'):
    return path[4:]
  return path


def get_all_files(directory: str) -> list[str]:
  all_files = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      file_path = os.path.join(root, file)
      if os.path.isfile(file_path):
        all_files.append(file_path)
  return all_files


def get_all_files_in_dirs(dirs: list[str]) -> list[str]:
  result = []
  for folder in dirs:
    result += get_all_files(folder)
  return result


def has_files(directory: str) -> bool:
  """
  Check if the given directory contains any files.

  :param directory: Path to the directory to check.
  :return: True if the directory contains files, False otherwise.
  """
  for root, dirs, files in os.walk(directory):
    if files:
      return True
  return False


def get_all_year_subfolders(year: int) -> list[str]:
  result = []
  dir = gl.dirs_photo[year]
  for subfolder in gl.subfolders:
    subfolder_path = dir + "\\" + subfolder
    if os.path.exists(subfolder_path):
      result.append(subfolder_path)
  return result



def delete_all_files_in_directory(directory: str) -> None:
  for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        os.rmdir(file_path)
    except Exception as e:
      print(f"Не удалось удалить {file_path}. Причина: {e}")
