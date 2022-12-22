import os
from pathlib import Path
import glob
import argparse

parser = argparse.ArgumentParser(description='add tags to non-tagged files')
parser.add_argument('-t','--prompt', type=str, help='tag to add', required=True)
parser.add_argument('-p','--path', type=str, help='directory to add tags', required=True)
args = parser.parse_args()

base_dir = Path(args.path)
if not base_dir.exists():
  print("path {} does not exist".format(base_dir))
  exit(1)
if not base_dir.is_dir():
  print("path {} is not a directory".format(base_dir))
  exit(1)

# https://stackoverflow.com/questions/4568580/python-glob-multiple-filetypes
extensions = ("jpg", "png", "gif", "jpeg", "bmp", "webp")


prompt = args.prompt
grabbed: list[Path] = []
for ext in extensions:
    grabbed.extend(base_dir.glob("*.{}".format(ext)))

for f in grabbed:
    txt = f.with_suffix(".txt")
    if not txt.exists():
      print("No txt file for {}".format(f))
      # with open(txt, 'w') as f:
      #   f.write(prompt)
    else:
      pass
      # print("Found txt file for {}".format(f))
