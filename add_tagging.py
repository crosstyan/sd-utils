import os
from pathlib import Path

pwd = os.path.dirname(os.path.realpath(__file__))
src_dir = Path(os.path.join(pwd, 'potg'))

if not src_dir.exists():
  print('directory not found. ')
  exit(1)

texts = src_dir.glob('*.txt')

remove_words = []
# remove_words = ["pussy", "vagina", "closeup", "anonymous"]
# remove_words = ["pussy", "vagina", "closeup", "anonymous"]
# add_words = ["photorealistic", "photo", "realistic", "pussy", "vagina", "closeup"]
add_words = ["by potg"]
sep = " "

for txt in texts:
  ws = None
  new_ws = None
  with open(txt, 'r') as f:
    ws = f.readline().split(sep)
  for w in remove_words:
    # I'm not using commma as seperator
    ws = [x for x in ws if x != w]
  ws = add_words + ws
  new_l = sep.join(ws)
  with open(txt, 'w') as f:
    f.write(new_l)



  
