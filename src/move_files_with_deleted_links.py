import os
import globals as gl
import helpers as hlp



def get_files_with_existent_links(links: list[str]) -> list[str]:
  result = []
  for  link in links:
    if os.path.islink(link):
      real_file_path = os.readlink(link)
      real_file_path = hlp.remove_extended_path_prefix(real_file_path)
      if os.path.exists(real_file_path):
        result.append(real_file_path)
      else:
        print(f"Реальный файл '{real_file_path}' не существует.")
    else:
     print(f"'{link}' не является символической ссылкой.")
  return result



def move_with_deleted_links(year: int) -> None:
  print(gl.dirs_photo[year])
  subdirs = hlp.get_all_year_subfolders(year)
  all_files = hlp.get_all_files_in_dirs(subdirs)
  all_links = hlp.get_all_files(gl.dirs_link[year])
  print(f"files: {len(all_files)}")
  print(f"links: {len(all_links)}")
  if len(all_files) - len(all_links) > 100:
    print("Файлов для удаления слишком много, операция отменяется!\n")
    return
  if len(all_files) == len(all_links):
    print("Количества файлов и линков совпадают, операция отменяется!\n")
    return
  print("Файлов для удаления: ", len(all_files) - len(all_links))
  files_with_existent_links = get_files_with_existent_links(all_links)
  #print(f"files_with_existent_links: {len(files_with_existent_links)}")
  files_for_move = list(set(all_files) - set(files_with_existent_links))
  n_renamed = 0
  for file in files_for_move:
    _, tail = os.path.splitdrive(file)
    tail = tail.replace('\\', '_')
    new_name = os.path.join(gl.dir_delete, tail)
    #print(file, " -- ", tail, " -- ", new_name)
    if os.path.exists(new_name):
      continue
    os.rename(file, new_name)
    n_renamed += 1
  print(f"Перемещено файлов: {n_renamed}\n")



if __name__ == "__main__":
  for year in gl.years:
    move_with_deleted_links(year)

  print("\nDone!")
  input("Press Enter to continue...")