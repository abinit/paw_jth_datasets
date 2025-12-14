#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#Usage: build_delta.py file_to_analyse txt_file_to_append
import sys
import os

my_eos_file = sys.argv[1]
my_txt_file = sys.argv[2]

if not os.path.exists(my_txt_file):
  fo=open(my_txt_file,"wb")
  fo.write(b"# Abinit version 10 -- calculations by F.Jollet and M. Torrent")
  fo.write(b"\n\n")
else:
  fo=open(my_txt_file,"ab")

sp=my_eos_file.split('.')[0]

with open(my_eos_file, "r") as fi:
  lines = fi.readlines()

fo.write((sp+"  "+lines[2]).encode('utf-8'))
fo.close()
