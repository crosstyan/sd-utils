import os.path
import re
import tempfile
import argparse
import glob
import zipfile
from pathlib import Path
from random import sample
from enum import Enum
from pprint import pprint
# from tabulate import tabulate
from prettytable import PrettyTable

class TxtType(Enum):
  UNKNOWN = 0
  UNPROCESSED = 1
  PROCESSED = 2
  NO_PICTURE = 3

pwd = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir = str(pwd.joinpath('*')) 

# list all the directory but not the files
dirs = [x for x in glob.glob(root_dir) if os.path.isdir(x)]

delete_suffix = [".jpg", ".png", ".gif", ".jpeg", ".bmp", ".webp"]

def guess_pic_name(txt_path:Path):
  s = txt_path.stem
  possiable_suffixs = ["png", "jpg", "jpeg"]
  # first check if the extension is pruned 
  parent = txt_path.parent
  pic_name = txt_path.stem 
  pic = Path(os.path.join(parent, pic_name)) 
  # if we can find the pic by the name of the txt
  # it's unprocessed
  if pic.exists():
    return (pic, TxtType.UNPROCESSED)
  for suffix in possiable_suffixs:
    p = txt_path.parent
    fn = s + "." + suffix
    p_path = p.joinpath(fn)
    if p_path.exists():
      return (p_path, TxtType.PROCESSED)
  return (None, TxtType.NO_PICTURE)

print("found {} directories".format(len(dirs)))
# t = PrettyTable(['Name', 'States'])
t = PrettyTable(['Name', 'Pic Count'])
counter = 0
for dir in dirs:
  dir = Path(dir)
  # print("{}".format(dir.name))
  txts = list(dir.glob('*.txt'))
  if txts is None or len(txts) == 0:
    print("No txt found in {}".format(dir))
    continue
  # sample_count = 5
  # s = sample(txts, sample_count)
  pics_pathes = list(map(lambda x: guess_pic_name(Path(x))[0], txts))
  t.add_row([dir.name, len(pics_pathes)])
  counter += len(pics_pathes)
  # pics_state = list(map(lambda x: guess_pic_name(Path(x))[1], s))
  # t.add_row([dir.name, pics_state])
t.add_row(["Total", counter])
print(t)

