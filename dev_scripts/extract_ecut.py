#!env python
import os

generic_name = "RUN2000"
#generic_name = "RUN2000-SP"

Ha_list=['20Ha','20Ha']
#Ha_list=['10Ha','12Ha','15Ha','175Ha','20Ha','25Ha','40Ha']

delta_suf='delta.txt'

dict_list=[]
spec_list=[]
for i, Ha_suf in enumerate(Ha_list):

  my_dict = {}
  my_spec = []

  filename=generic_name+'_'+Ha_suf+'_'+delta_suf
  with open(filename,'r',encoding="utf-8") as f:
    lines = f.readlines()

  for lgn in lines:
    if lgn[0:2] not in ['# ','--','np']:
      wd = lgn.split()
      my_dict[wd[0]] = float(wd[3])
      my_spec.append(wd[0])
  
  dict_list.append(my_dict)
  if len(spec_list) == 0: spec_list = my_spec

f = open(generic_name+"_delta_ecut.txt",'w',encoding="utf-8")

tit = '#Ecut'+' '*(6-len(Ha_list[0]))+Ha_list[0]
for Ha_suf in Ha_list[1:]:
  tit += ' '*(9-len(Ha_suf))+Ha_suf
f.write(tit+"\n\n") 

for sp in spec_list:
  ref = dict_list[-1][sp]
  lgn = ' '*(2-len(sp))+sp
  for dic in dict_list:
    lgn += "  %7.3f" % (abs(dic[sp] - ref))
  f.write(lgn+'\n')
f.close()

f = open(generic_name+"_ecut.txt",'w',encoding="utf-8")

tit = '#Sp   ecut_high  ecut_medium     ecut_low'
f.write(tit+"\n\n") 

ecut_list =[float(s.replace('Ha','')) if s != '175Ha' else 17.5 for s in reversed(Ha_list)]
for sp in spec_list:
  ecut_h = 40
  ecut_m = 40
  ecut_l = 40 
  ref = dict_list[-1][sp]
  for i, dic in enumerate(reversed(dict_list)):
    if abs(dic[sp] - ref) < 1.0: ecut_h = ecut_list[i]
    if abs(dic[sp] - ref) < 2.0: ecut_m = ecut_list[i]
    if abs(dic[sp] - ref) < 5.0: ecut_l = ecut_list[i]
  stg = ' '*(2-len(sp))+sp
  stg += '         %4.1f         %4.1f         %4.1f' %(ecut_h,ecut_m,ecut_l)
  f.write(stg+'\n')
f.close()
