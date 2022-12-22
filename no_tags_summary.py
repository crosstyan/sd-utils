import os
from pathlib import Path
import glob
import argparse


parser = argparse.ArgumentParser(
    description='Script to prepare datasets for training')
parser.add_argument('-i', '--src', type=str, help='The source directory', required=True)
args = parser.parse_args()
src = Path(args.src)
# https://stackoverflow.com/questions/4568580/python-glob-multiple-filetypes

# dirs = [x for x in src.glob("*") if src.is_dir()]

# def no_txt_counter(dir:Path):
#   extensions = ("jpg", "png", "gif", "jpeg", "bmp", "webp")
#   grabbed: list[Path] = []
#   for ext in extensions:
#       grabbed.extend(dir.glob("*.{}".format(ext)))
#   counter = 0
#   for f in grabbed:
#       txt = f.with_suffix(".txt")
#       if not txt.exists():
#         print("No txt file for {}".format(f))
#         counter += 1
#         # with open(txt, 'w') as f:
#         #   f.write(prompt)
#       else:
#         pass
#         # print("Found txt file for {}".format(f))
#   return counter

# counters = map(no_txt_counter, dirs)

# for dir, counter in zip(dirs, counters):
#   if counter != 0:
#     print("no txt found in {}: {}".format(dir, counter))
