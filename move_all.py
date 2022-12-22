import os
from pathlib import Path
import glob
import argparse
import shutil
import logging
import hashlib

parser = argparse.ArgumentParser(description='move all the file into one dir')
parser.add_argument('-i','--src', type=str, help='src', required=True)
parser.add_argument('-o', '--output', type=str, help='output directory', required=True)
args = parser.parse_args()

base_dir = Path(args.src)
out_dir = Path(args.output)
if not base_dir.exists():
  print("path {} does not exist".format(base_dir))
  exit(1)

if not base_dir.is_dir():
  print("path {} is not a directory".format(base_dir))
  exit(1)

if not out_dir.exists():
  print("output path {} does not exist".format(out_dir))
  exit(1)

if not out_dir.is_dir():
  print("output path {} is not a directory".format(out_dir))
  exit(1)

# https://stackoverflow.com/questions/4568580/python-glob-multiple-filetypes
extensions = ("jpg", "png", "gif", "jpeg", "bmp", "webp")

# prompt = args.prompt
grabbed: list[Path] = []
for ext in extensions:
    grabbed.extend(base_dir.rglob("*.{}".format(ext)))

for src in grabbed:
  src_txt = None
  if src.with_suffix(".txt").exists():
    src_txt = src.with_suffix(".txt")
  dst = out_dir / src.name
  if dst.exists():
    h = None
    # calculate a hash for the new file
    with open(src, "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()
    dst = dst.with_name(h).with_suffix(src.suffix)
    logging.warn("{} is already exists. using {}".format(out_dir / src.name, dst))
  if src_txt != None:
    dst_txt = dst.with_suffix(".txt")
    shutil.move(src_txt, dst_txt)
  shutil.move(src, dst)