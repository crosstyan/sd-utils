import os
import glob
import shutil
from pathlib import Path
from typing import Callable, Optional
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
from psutil import cpu_count
from result import Ok, Err, Result
import argparse
from PIL import Image


def get_parser():
    parser = argparse.ArgumentParser(
        description='Script to prepare datasets for training')
    parser.add_argument('-i', '--src', type=str, help='The source directory', required=True)
    parser.add_argument('-o', '--dst', type=str,
                        help='The destination directory', required=True)
    parser.add_argument('-s', '--size', type=int,
                        help='The size you want to fuck', default=512)
    # parser.add_argument('-q', '--quiet', action=)
    return parser


def guess_pic_name(txt_path: Path):
    possible_suffix = ["png", "jpg", "jpeg"]
    # first check if the extension is pruned
    pic_name = txt_path.stem
    parent = txt_path.parent
    pic = Path(os.path.join(parent, pic_name))
    if pic.exists():
        return pic
    for suffix in possible_suffix:
        #  (including the leading ".")
        p_path = txt_path.with_suffix(".{}".format(suffix))
        if p_path.exists():
            return p_path
    return None

# https://stackoverflow.com/questions/7287996/get-relative-path-from-comparing-two-absolute-paths


def get_relate(p: Path, root: Path, new_root: Path):
    rp = p.relative_to(root)
    return new_root.joinpath(rp)

def kb_to_bytes(kb: int):
    return kb * 1024


def is_small_pic(_txt: Path, pic: Path, file_size: int):
    if file_size < 0:
      return False
    size = pic.stat().st_size
    return size < file_size


def is_small_pic_len(_txt: Path, pic: Path, min_size: int):
    # prevent dumb shit
    if min_size < 0:
      return False
    try:
      img = Image.open(pic)
      w, h = img.size
      return w < min_size or h < min_size
    except:
      return False

# why do I use that Result...
# not Pythonic at all unless you want to write a whole shit
def move_to_dst_if(f: Callable[[Path, Path], bool], txt_path: Path, src: Path, dst: Path, use_relative: bool = True) -> Result[Optional[str], str]:
    pic = guess_pic_name(txt_path)
    if pic is not None:
        if f(txt_path, pic):
            new_path = dst.joinpath(pic.name)
            new_path_txt = dst.joinpath(txt_path.name)
            if use_relative:
                new_path = get_relate(pic, src, dst)
                new_path_txt = get_relate(txt_path, src, dst)
            # hope the parent will not be a file
            if not new_path.parent.exists():
                new_path.parent.mkdir(parents=True)
            shutil.move(pic,  new_path)
            shutil.move(txt_path, new_path_txt)
            return Ok(str(new_path))
        return Ok(None)
    else:
        return Err("Picture is not exist for {}".format(txt_path))


# https://github.com/rustedpy/result
def main():
  args = get_parser().parse_args()
  src = Path(args.src)
  dst = Path(args.dst)
  if not src.is_dir and not src.exists():
    print('Grabber directory not found. ')
    exit(1)
  txts = src.rglob("*.txt")
  func = lambda p_p, t_p: is_small_pic_len(p_p, t_p, args.size)
  for txt in txts:
    res = move_to_dst_if(func, txt, src, dst)
    match res:
      case Ok(val):
        if val != None: 
          pass
          # print("moved to {}".format(val))
      case Err(e):
        pass
        # print(e)


if __name__ == "__main__":
  main()