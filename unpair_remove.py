import os
from pathlib import Path

pwd = os.path.dirname(os.path.realpath(__file__))
src_dir = Path(pwd)

if not src_dir.exists():
  print('directory not found. ')
  exit(1)


types = ['jpg', 'png', 'jpeg', 'gif', 'webp', 'bmp', 'mp4'] # the tuple of file types
texts = src_dir.glob("**/*.txt")
for txt in texts:
  remove_flag = True
  for type in types:
    possible_pic = txt.with_suffix("." + type)
    # if any of the possible pic exists, then we don't need to remove the txt
    if possible_pic.exists():
      remove_flag = False
      break
    # if we reach the end of the loop, then we can remove the txt
  if remove_flag:
    print("removing {}".format(txt))
    txt.unlink()
