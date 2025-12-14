#!env python
import os, shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ecut-file', type=str, required=True, \
   help='name of the file containing the cut-off energy')
parser.add_argument('--pseudo-dir', type=str, required=True, \
   help='name of the directory containing the pseudopotentials')

args = parser.parse_args()
ecut_file = args.ecut_file
pseudo_dir = args.pseudo_dir

LINE_AFTER = '<!-- PAW atomic dataset for'

# Read ecut file
ecut = {}
with open(ecut_file,'r',encoding="utf-8") as f:
  lines = f.readlines()
for ll in lines:
  lgn = ll.strip()
  if len(lgn) > 0:
    if lgn[0] not in ['#']:
      wd = lgn.split()
      try:
        ecuth = float(wd[1])
        ecutm = float(wd[2])
        ecutl = float(wd[3])
        ecut[wd[0]] = [ecutl,ecutm,ecuth]
      except ValueError:
        pass

# Loop over files in pseudo-dir
for root, dirs, files in os.walk(pseudo_dir):
  for ff in files:
    file_fullname = os.path.join(root,ff)
    
#   Look for specie in ecut file
    ff_wd = ff.split('.')
    specie = ff_wd[0].capitalize()
    if len(ff_wd) >=3 :
      ext = ff_wd[-1].lower()
      ext2 = ff_wd[-2].lower()
    else:
      ext = '' ; ext2 = ''
    if ext == 'xml' and ext2 != 'corewf':
      if specie in ecut.keys():
        if len(ecut[specie]) == 3:

          # Read pseudo file
          f_in = open(file_fullname,'r')
          flines = f_in.readlines()
          f_in.close()

#         Copy backup of pseudo file
          shutil.move(file_fullname,file_fullname+'.bak')            

          # Write new version of pseudo file
          f_out = open(file_fullname,'w')
          for fline in flines:
            f_out.write(fline)
            if LINE_AFTER in fline:
              add_line = '<pw_ecut low="%.2f" medium="%.2f" high="%.2f"/>\n' \
                       % (ecut[specie][0],ecut[specie][1],ecut[specie][2])
              f_out.write(add_line) 
          f_out.close()
