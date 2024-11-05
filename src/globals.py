import os

years = [2019, 2022, 2024]
dir_base = r"F:\Photo_Boise"
dir_delete = dir_base + r"\__for_delete"
subfolders = ["Sony", "Serg", "Gala", "Vova", "Nina"]
dirs_photo = {year: (dir_base + r"\_From_Boise_" + str(year)) for year in years}
dirs_link = {year: (dir_base + r"\_From_Boise_" + str(year) + "_links") for year in years}

dir_links_deleted_from_original = os.path.join(dir_base,  "__deleted_from_original_links")



if not os.path.exists(dir_delete):
  os.makedirs(dir_delete)
if not os.path.exists(dir_links_deleted_from_original):
  os.makedirs(dir_links_deleted_from_original)