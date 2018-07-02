import re

# Function sorting by digits independent from length
def natural_sort(l): 
  convert = lambda text: int(text) if text.isdigit() else text.lower() 
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
  return sorted(l, key = alphanum_key)

# cut a list of configuration based on indices
def cut_range(lst, rnge):
  # the indices pointing to first and last index
  #TODO: think about list comprehension
  #e = [i for i,s in enumerate(lst) if]
  b, e = 0, 0
  for i, s in enumerate(lst):
  # s is padded with cnfg, exclude from comparison for identity checking
    if rnge[0] == s[4:]:
      b = i
    if rnge[1] == s[4:]:
      e = i
  res = lst[b:e+2]
  #return res[0::int(rnge[2])]
  return res[0::2]

