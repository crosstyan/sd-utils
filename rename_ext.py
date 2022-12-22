from pathlib import Path
import glob
import os
import pandas as pd
from pprint import pprint
import shutil

# base_dir = "C:/Users/cross/Desktop/Grabber"
# base_dir = "C:\\Users\\cross\\Desktop\\Shion"
pwd = Path(os.path.dirname(os.path.realpath(__file__))) 
# folder_list = ["mankai_kaika", "middle_finger", "mika", "misc", "ogipote", "paindude", "XP2"]
# folder_list = ["XP"]
# input_folder = pwd / "XP"
delete_suffix = [".jpg", ".png", ".gif", ".jpeg", ".bmp", ".webp"]

def handle_folder(input_dir:str, recursive: bool = False):
  base_dir = Path(input_dir)
  if not base_dir.is_dir():
    return
  if not base_dir.exists():
    print(f"directory {base_dir} not found. ")
    return
  txts = list(base_dir.glob('**/*.txt') if recursive else base_dir.glob('*.txt')) 
  rename_filename(txts)

# a list of Path
def rename_filename(files: list[Path]):
    for file in files:
        p = Path(file)
        parent = p.parent
        s = p.stem
        pic = (parent / s)
        if pic.exists():
          new_txt_name = pic.with_suffix(".txt")
          if not new_txt_name.exists():
            p.rename(new_txt_name)
          else:
            p.unlink()

def correct_artists_name(txt: str) -> str:
  strange_artists = {
    "aaaa+aaaa (quad-a)": "aaaa",
    "hagi (ame hagi)": "hagi",
    "muk (monsieur)": "muk",
    "asou (asabu202)": "asou",
    "chou (meteorite3)": "chou",
    "shion (mirudakemann)": "shion",
  }
  # I assume you only get one artist
  for k, v in strange_artists.items():
    if k in txt:
      replaced = txt.replace(k, v)
      if replaced is not None:
        return replaced
  # can't find any strange artist
  return txt

# rename_filename(texts)
def read_authors(files: list[str]) -> dict[str, int]:
    result = {}
    for file in files:
        with open(file, "r") as f:
            l = f.readline()
            by = l.split("by")[-1]
            by = by.strip()
            result[by] = result.get(by, 0) + 1
    return result

def print_ranking(authors: dict[str, int]):
  df = pd.DataFrame(authors.items(), columns=["Author", "Count"])
  # filter out the author with less than 10 images
  d = df[df["Count"] > 5].sort_values("Count", ascending=False)
  print(d)

def do_correct(files: list[str]):
  for file in files:
    old = ""
    l = ""
    with open(file, "r") as f:
      old = f.readline()
    with open(file, "w") as f:
      l = correct_artists_name(old)
      f.write(l)


handle_folder(pwd, True)
# do_correct(texts)
# authors = read_authors(texts)
# print_ranking(authors)