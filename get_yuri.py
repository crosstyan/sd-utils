import os
import glob
import shutil
from pathlib import Path
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
from psutil import cpu_count

pwd = Path(os.path.dirname(os.path.realpath(__file__))) 
# src_dir = pwd / '.'
# yuri_dir = pwd / ".." / "ng"
src_dir = pwd / "XP3"
yuri_dir = pwd / "dikko_t"

words = ["dikko"]

def guess_pic_name(txt_path:Path):
  possiable_suffixs = ["png", "jpg", "jpeg"]
  # first check if the extension is pruned 
  pic_name = txt_path.stem 
  parent = txt_path.parent
  pic = Path(os.path.join(parent, pic_name)) 
  if pic.exists():
    return pic
  for suffix in possiable_suffixs:
    #  (including the leading ".")
    p_path = txt_path.with_suffix(".{}".format(suffix))
    if p_path.exists():
      return p_path
  return None

def kb_to_bytes(kb:int):
  return kb * 1024
  
def fuck_small_size(text:str):
  text = Path(text)
  l = None
  with open(text, 'r') as f:
    l = f.readline()
  pic = guess_pic_name(text)
  if pic is not None:
    size = pic.stat().st_size
    if size < kb_to_bytes(30):
        tqdm.write('Moving to {}'.format(yuri_dir.joinpath(pic.name)))
        shutil.move(pic,  yuri_dir.joinpath(pic.name))
        shutil.move(text, yuri_dir.joinpath(text.name))


def detect(text:str):
  text = Path(text)
  l = None
  with open(text, 'r') as f:
    l = f.readline()
  for word in words:
    if word in l:
      pic = guess_pic_name(text)
      if pic is not None:
        tqdm.write('Moving to {}'.format(yuri_dir.joinpath(pic.name)))
        shutil.move(pic,  yuri_dir.joinpath(pic.name))
        shutil.move(text, yuri_dir.joinpath(text.name))
        # print("Moved {} and {} to folder".format(pic, text))
        break
      else:
        # print("No file found for {}, get {}".format(text, pic))
        break
  

if __name__ == "__main__":
  if not src_dir.is_dir and not src_dir.exists():
    print('Grabber directory not found. ')
    exit(1)

  if not yuri_dir.exists():
    yuri_dir.mkdir(parents=True)
    print('Directory created: {}'.format(yuri_dir))
  # txts = txts = os.path.join(src_dir, "**", "*.txt")
  txts = txts = os.path.join(src_dir, "*.txt")
  texts = glob.glob(txts)
  u_count = cpu_count()
  process_map(detect, texts, max_workers=u_count)
  # process_map(fuck_small_size, texts, max_workers=u_count)