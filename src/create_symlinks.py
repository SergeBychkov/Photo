import os, pathlib, shutil
from datetime import datetime, timedelta
from PIL import Image
from PIL.ExifTags import TAGS

import globals as gl
import helpers as hlp
from models import FileInfo


def minus_12_hours_for_Sony_2024(dt_str: str) -> str:
  dt: datetime = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
  dt_right = dt - timedelta(hours=12)
  return dt_right.strftime("%Y:%m:%d %H:%M:%S")


def get_image_datetime(image_path):
  image = Image.open(image_path)
  exif_data = image._getexif()
  if exif_data:
    for tag, value in exif_data.items():
      tag_name = TAGS.get(tag, tag)
      if tag_name == 'DateTimeOriginal':
        return value
  return None


def get_all_images(directory: str) -> list[FileInfo]:
  images = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
        file_path = os.path.join(root, file)
        image_info = FileInfo(path=file_path, name=file, dt=get_image_datetime(file_path))
        images.append(image_info)
  return images


def get_all_videos(directory: str) -> list[FileInfo]:
  videos = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.lower().endswith(".mp4") or file.lower().endswith(".mov") or file.lower().endswith(".mts"):
        file_path = os.path.join(root, file)
        image_info = FileInfo(path=file_path, name=file, dt=None)
        videos.append(image_info)
  return videos


def create_images_symlinks(year_symlink_folder: str, year_folder: str, subfolder: str) -> None:
  images = get_all_images(os.path.join(year_folder, subfolder))
  for image in images:
    orig_datetime = image.dt
    new_datetime = orig_datetime

    if subfolder == "Sony" and ("2024" in year_folder):  # only for Sony 2024!
      if image.name < "DSC04309.JPG":
        new_datetime = minus_12_hours_for_Sony_2024(orig_datetime)

    # orig_for_filename = orig_datetime.replace(":", "_").replace(" ", "__")
    new_for_filename = new_datetime.replace(":", "_").replace(" ", "__")
    file_name = os.path.basename(image.name)
    _, ext = os.path.splitext(file_name)
    if ext == ".jpeg":
      ext = ".jpg"
    symlink_name = os.path.join(year_symlink_folder,
                                new_for_filename + " (" + subfolder + " - " + file_name + ")" + ext)
    pathlib.Path(symlink_name).unlink(missing_ok=True)
    os.symlink(image.path, symlink_name)


def create_videos_symlinks(year_symlink_folder: str, year_folder: str, subfolder: str) -> None:
  videos = get_all_videos(os.path.join(year_folder, subfolder))
  for video in videos:
    file = video.name
    if subfolder != "Sony":
      dt = file[4:8] + "_" + file[8:10] + "_" + file[10:12] + "__" + file[13:15] + "_" + file[15:17] + "_" + file[17:19]
    else:
      dt = file[0:4] + "_" + file[4:6] + "_" + file[6:8] + "__" + file[8:10] + "_" + file[10:12] + "_" + file[12:14]
    file_name = os.path.basename(video.name)
    _, ext = os.path.splitext(file_name)
    symlink_name = os.path.join(year_symlink_folder, dt + " (" + subfolder + " - " + file_name + ")" + ext)
    pathlib.Path(symlink_name).unlink(missing_ok=True)
    os.symlink(video.path, symlink_name)


def create_symlinks(years: list[int]) -> None:
  if not os.path.exists(gl.dir_delete):
    os.makedirs(gl.dir_delete)

  for year in years:
    year_folder = gl.dirs_photo[year]
    print(f"Processing {year_folder} ...")
    parent_folder = os.path.dirname(year_folder)
    year_symlink_folder = os.path.join(parent_folder, os.path.basename(year_folder) + "_links")

    shutil.rmtree(year_symlink_folder, ignore_errors=True)

    year_symlink_video_folder = os.path.join(year_symlink_folder, "Video")
    if not os.path.exists(year_symlink_video_folder):
      os.makedirs(year_symlink_video_folder)

    # exit()

    for subfolder in gl.subfolders:
      create_images_symlinks(year_symlink_folder, year_folder, subfolder)
      create_videos_symlinks(year_symlink_video_folder, year_folder, subfolder)


if __name__ == "__main__":
  if hlp.has_files(gl.dir_delete):
    print(
      f"\nВ папке {gl.dir_delete} имеются файлы.\nЗапустите программу move_files_with_deleted_links.py, чтобы не потерять сделанные удаления линков!\n")
    exit()

  print("\nAdministrator rights are required to create symlinks!\n")

  create_symlinks(gl.years)
  # create_symlinks([2019])

  print("\nDone!")
  # input("Press Enter to continue...")
