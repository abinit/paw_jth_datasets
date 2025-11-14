#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from __future__ import print_function, division
import sys
import os
import re
import json
import shutil
import hashlib
import tarfile
from lxml import etree
from collections import OrderedDict

info_filename        = "dataset_info.txt"
readme_filename      = "README.md"
comment_filename     = "Comments"
atomicdata_folder    = "ATOMICDATA"
input_xml_lines_def  = ['XMLOUT\n','default\n']
input_upf_lines_def  = ['UPFOUT\n','default\n']
indexhtml_filename   = "index.html"
globalindex_template = "index-table.html"
specie_html_template = "index-specie.html" 
jth_short_name       = "JTH"
github_link          = "https://github.com/abinit/paw_jth_datasets"
github_subfolder     = "pseudos"
github_folder_def    = "/Users/torrentm/WORK/JTH-TABLE/GITHUB/paw_jth_datasets/pseudos"
link_to_error404     = "https://abinit.github.io/404"
website_template     = "/Users/torrentm/WORK/JTH-TABLE/GITHUB/paw_jth_datasets/jth_website_template"
last_modif_date      = "nov. 1, 2025"
web_master           = "M. Torrent, F. Jollet"

shell_name = ('s','p','d','f','g')
shell_charge = (2,6,10,14,18)
shell_core = ([1,0],[2,0],[2,1],[3,0],[3,1],[4,0],[3,2],[4,1],[5,0],[4,2],[5,1], \
              [6,0],[4,3],[5,2],[6,1],[7,0],[5,3],[6,2],[7,1],[8,0],[5,4],[6,3],[7,2])
rare_gas= (['1s2','He'], \
           ['1s2 2s2 2p6','Ne'], \
           ['1s2 2s2 2p6 3s2 3p6','Ar'], \
           ['1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6','Kr'], \
           ['1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6','Xe'], \
           ['1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6','Rn'])

dojo_info_def = {"pp_type": "PAW",
                 "description": "Standard table designed for GS applications", 
                 "xc_name": "unknown",
                 "references": ["Comp. Phys. Comm. 185, 1246 (2014)"],
                 "authors": ["F. Jollet", "M. Torrent", "N. Holzwarth"],
                 "dojo_dir": "unknown" } 

atom_info_def = {"basename": None, "Z_val": None, "l_max": None, "md5": None,
                 "dfact_meV": None, "dfactprime_meV": None, "tags": [],
                 "hints": {"high": {"ecut": None}, "low": {"ecut": None}, "normal": {"ecut": None}}}

specie = {  "H": ("Hydrogen", "1"),       "He": ("Helium", "2"),        "Li": ("Lithium", "3"),
           "Be": ("Berylium", "4"),        "B": ("Boron", "5"),          "C": ("Carbon", "6"),
            "N": ("Nitrogen", "7"),        "O": ("Oxygen", "8"),         "F": ("Fluorine", "9"),
           "Ne": ("Neon", "10"),          "Na": ("Sodium", "11"),       "Mg": ("Magnesium", "12"),
           "Al": ("Aluminum", "13"),      "Si": ("Silicon", "14"),       "P": ("Phosphorus", "15"),
            "S": ("Sulfur", "16"),        "Cl": ("Chlorine", "17"),     "Ar": ("Argon", "18"),
            "K": ("Potassium", "19"),     "Ca": ("Calcium", "20"),      "Sc": ("Scandium", "21"),
           "Ti": ("Titanium", "22"),       "V": ("Vanadium", "23"),     "Cr": ("Chromium", "24"),
           "Mn": ("Manganese", "25"),     "Fe": ("Iron", "26"),         "Co": ("Cobalt", "27"),
           "Ni": ("Nickel", "28"),        "Cu": ("Copper", "29"),       "Zn": ("Zinc", "30"),
           "Ga": ("Gallium", "31"),       "Ge": ("Germanium", "32"),    "As": ("Arsenic", "33"),
           "Se": ("Selenium", "34"),      "Br": ("Bromine", "35"),      "Kr": ("Krypton", "36"),
           "Rb": ("Rubidium", "37"),      "Sr": ("Strontium", "38"),     "Y": ("Yttrium", "39"),
           "Zr": ("Zirconium", "40"),     "Nb": ("Niobium", "41"),      "Mo": ("Molybdenum", "42"),
           "Tc": ("Technetium", "43"),    "Ru": ("Ruthenium", "44"),    "Rh": ("Rhodium", "45"),
           "Pd": ("Palladium", "46"),     "Ag": ("Silver", "47"),       "Cd": ("Cadmium", "48"),
           "In": ("Indium", "49"),        "Sn": ("Tin", "50"),          "Sb": ("Antimony", "51"),
           "Te": ("Tellurium", "52"),      "I": ("Iodine", "53"),       "Xe": ("Xenon", "54"),
           "Cs": ("Cesium", "55"),        "Ba": ("Barium", "56"),       "La": ("Lanthanum", "57"),
           "Ce": ("Cerium", "58"),        "Pr": ("Praseodymium", "59"), "Nd": ("Neodynium", "60"),
           "Pm": ("Promethium", "61"),    "Sm": ("Samarium", "62"),     "Eu": ("Europium", "63"),
           "Gd": ("Gadolinium", "64"),    "Tb": ("Terbium", "65"),      "Dy": ("Dysprosium", "66"),
           "Ho": ("Holmium", "67"),       "Er": ("Erbium", "68"),       "Tm": ("Thulium", "69"),
           "Yb": ("Ytterbium", "70"),     "Lu": ("Lutetium", "71"),     "Hf": ("Hafnium", "72"),
           "Ta": ("Tantalum", "73"),       "W": ("Tungsten", "74"),     "Re": ("Rhenium", "75"),
           "Os": ("Osmium", "76"),        "Ir": ("Iridium", "77"),      "Pt": ("Platinum", "78"),
           "Au": ("Gold", "79"),          "Hg": ("Mercury", "80"),      "Tl": ("Thallium", "81"),
           "Pb": ("Lead", "82"),          "Bi": ("Bismuth", "83"),      "Po": ("Polonium", "84"),
           "At": ("Astatine", "85"),      "Rn": ("Radon", "86"),        "Fr": ("Francium", "87"),
           "Ra": ("Radium", "88"),        "Ac": ("Actinium", "89"),     "Th": ("Thorium", "90"),
           "Pa": ("Protactinium", "91"),   "U": ("Uranium", "92"),      "Np": ("Neptunium", "93"),
           "Pu": ("Plutonium", "94"),     "Am": ("Americium", "95"),    "Cm": ("Curium", "96"),
           "Bk": ("Berkelium", "97"),     "Cf": ("Californium", "98"),  "Es": ("Einsteinium", "99"),
           "Fm": ("Fermium", "100"),      "Md": ("Mendelevium", "101"), "No": ("Nobelium", "102"),
           "Lr": ("Lawrencium", "103"),   "Rf": ("Unniquadium", "104"), "Db": ("Unnilpentium", "105"),
           "Sg": ("Unnilhexium", "106"),  "Bh": ("Unnilsptium", "107"), "Hs": ("Unniloctium", "108"),
           "Mt": ("Unnilennium", "109"), "Uun": ("Ununnilium", "110"), "Uuu": ("Unununium", "111"),
          "Uub": ("Ununbium", "112") }

#sys.tracebacklimit = 0


#--------------------------------------------------------------------------------
# MAIN ROUTINES

#=========================================
def main_create_github_from_table(table_folder,github_folder=github_folder_def):
  """Read data in table_folder and create github_folder structure"""

# Read table info
  table_name = table_name_from_string(os.path.split(table_folder)[1])
  table_version = table_version_from_string(table_name)
  github_table_folder = os.path.join(github_folder,table_name)
  github_table_link  = github_link+"/raw/main/"+github_subfolder+"/"+table_name
  table_link_to_pdf  = link_to_error404
  ddb_info_filename = None

# Create github destination directory
  if not exists_case_sensitive(github_table_folder): os.makedirs(github_table_folder,exist_ok=True)

# Create specie directories in destination folder
  for sp_name in specie.keys():
    fname=os.path.join(github_table_folder,sp_name)
    if not exists_case_sensitive(fname): os.makedirs(fname,exist_ok=True)

# Explore root directory
  for root, dirs, files in os.walk(table_folder):
    for file_name in files:
      file_bodyname, file_ext = os.path.splitext(file_name)
      file_fullname = os.path.join(root,file_name)
      file_specie = specie_from_filename(file_name)
      if os.path.isfile(file_fullname):

        if file_specie in specie.keys():
          dir_dest = os.path.join(github_table_folder,file_specie)
   
#         Process XML file(s)
          if file_ext == '.xml' or file_ext == ".XML":
            if string_is_in_file(["<paw_dataset version=","<paw_setup version="],file_fullname):
              #Copy file
              shutil.copy2(file_fullname,dir_dest)
              #Create input file
              pawdt = paw_dataset(xml_filename=file_fullname)
              file_input_dest = os.path.join(github_table_folder,file_specie,file_bodyname+".atompaw.input")
              upf_name1=os.path.join(root,file_bodyname + ".upf")
              upf_name2=os.path.join(root,file_bodyname + ".UPF")
              if isfile_case_sensitive(upf_name1): pawdt.read_from_upf(upf_name1)
              if isfile_case_sensitive(upf_name2): pawdt.read_from_upf(upf_name2)
              merged_input_file=pawdt.merge_xml_upf_input()
              if len(merged_input_file) > 0:
                finput = open(file_input_dest,'w')
                finput.write("".join(merged_input_file))
                finput.close()

#         Process UPF file(s)
          elif file_ext == '.upf' or file_ext == ".UPF":
            if string_is_in_file(["<UPF version="],file_fullname):
              shutil.copy2(file_fullname,dir_dest)

#       Process PDF file(s)
        if file_ext == '.pdf':
          table_link_to_pdf = os.path.join(github_table_link,table_name+".pdf")
          file_dest = os.path.join(github_table_folder,table_name+'.pdf')
          shutil.copy2(file_fullname,file_dest)

#       Process "Comments" file
        if file_name == comment_filename:
          ddb_info_filename = os.path.join(github_table_folder,info_filename)
          infofile_from_commentfile(file_fullname,ddb_info_filename)

# Initialize database from info file
  if ddb_info_filename is not None:
    ddb = database_info(txt_filename=ddb_info_filename)
  else:
    raise ValueError("No Comments file found in table_folder!")

# Make tmp dir
  tmp_dir = os.path.join(github_folder,"tmp")
  if isdir_case_sensitive(tmp_dir): shutil.rmtree(tmp_dir,ignore_errors=True)
  os.makedirs(tmp_dir,exist_ok=True)

# Initialize txt file(s) data
  file_txt={}
  for cat in ddb.category_list:
    file_txt[cat] = ""

# Initialize json file(s) data
  file_json={} 
  for cat in ddb.category_list:
    file_json[cat] = {"dojo_info":dojo_info_def.copy(),"pseudo_metadata":{}}

# Explore directories
  for dir_name in os.listdir(github_table_folder):
    dir_fullname = os.path.join(github_table_folder,dir_name)
    if isdir_case_sensitive(dir_fullname):

#     Manage README file
      #if exists_case_sensitive(readme_filename): os.remove(readme_filename)
      file_readme = open(os.path.join(dir_fullname,readme_filename), 'w')
      readme_is_empty = True
      
#     Explore atom
      for iat,atom in enumerate(ddb.atom_list):
        if dir_name == atom:

#         Retrieve dataset info
          pawdt_info = ddb.info_list[iat]
          basename = pawdt_info[1]
          file_base, file_ext = os.path.splitext(basename) 
          pawdt = paw_dataset()

#         Process XML
          for f_ext in ['.xml','.XML']:
            pawdt_path_xml = os.path.join(dir_fullname,file_base+f_ext)
            if isfile_case_sensitive(pawdt_path_xml):
              pawdt.read_from_xml(xml_filename=pawdt_path_xml)
              #Store file for tarball
              xc_dir = os.path.join(tmp_dir,jth_short_name+"-v"+table_version+"-"+pawdt.xc_type+"-"+pawdt.xc_name+"-atomicdata")
              if len(pawdt.xc_name)>0 and pawdt.xc_name not in ddb.xc_names:
                ddb.xc_names.append(pawdt.xc_name)
                os.makedirs(xc_dir,exist_ok=True)
              shutil.copy2(pawdt_path_xml,xc_dir)            

#         Process UPF
          for f_ext in ['.upf','.UPF']:
            pawdt_path_upf = os.path.join(dir_fullname,file_base+f_ext)
            if isfile_case_sensitive(pawdt_path_upf):
              pawdt.read_from_upf(upf_filename=pawdt_path_upf)
              #Store file for tarball
              xc_dir = os.path.join(tmp_dir,jth_short_name+"-v"+table_version+"-"+pawdt.xc_type+"-"+pawdt.xc_name+"-atomicdata")
              if len(pawdt.xc_name)>0 and pawdt.xc_name not in ddb.xc_names:
                ddb.xc_names.append(pawdt.xc_name)
                os.makedirs(xc_dir,exist_ok=True)
              shutil.copy2(pawdt_path_upf,xc_dir)            

#         Process atompaw.input
          f_ext = '.atompaw.input'
          pawdt_path_inp = os.path.join(dir_fullname,file_base+f_ext)
          if isfile_case_sensitive(pawdt_path_inp):
            pawdt.inp_file_name = os.path.split(pawdt_path_inp)[-1]
          
#         Read other dataset info
          pawdt.read_from_info(dataset_info=pawdt_info)

#         Check atom vs symbol
          if atom != pawdt.symbol:
            raise ValueError("Inconsistency atom=%s and symbol=%s!" % (atom, pawdt.symbol))

#         Store dataset info into txt string
          if pawdt.category != "unknown":
            file_txt[pawdt.category] += pawdt.symbol+"/"+pawdt.xml_file_name+"\n"

#         Store dataset info into json string
          if pawdt.category != "unknown":
            file_json[pawdt.category]["pseudo_metadata"][atom] = pawdt.set_pseudodojo_dict()

#         Write header in README file
          if readme_is_empty:
            file_readme.write("### JTH PAW atomic dataset(s) for element "+atom+"\n")
            file_readme.write("  \n")
            file_readme.write("_These atomic data have been carefully tested against ") 
            file_readme.write("all-electron calculations and other available atomic datasets")
            if table_link_to_pdf != link_to_error404:
              file_readme.write(" (some reference results are given [here]("+table_link_to_pdf+")).")
            file_readme.write("_\n_They are recommended for use, although they have to be tested ")
            file_readme.write("again by users._  \n")
            readme_is_empty = False

#         Write dataset info in README file
          file_readme.writelines(pawdt.markdown_lines(github_table_link))

#     Close README file
      file_readme.close()

# Write txt file(s)
  for cat,stg in file_txt.items():
    ftxt_name = os.path.join(github_table_folder,cat)+'.txt'
    #if exists_case_sensitive(ftxt_name): os.remove(ftxt_name)
    ftxt = open(ftxt_name, 'w')
    ftxt.write(stg)
    ftxt.close()

# Write json file(s)
  for cat,dic in file_json.items():
    fjson_name = os.path.join(github_table_folder,cat)+'.djson'
    #if exists_case_sensitive(fjson_name): os.remove(fjson_name)
    fjson = open(fjson_name, 'w')
    dic["dojo_info"]["dojo_dir"] = ddb.name
    dic["dojo_info"]["xc_name"]  = "/".join(ddb.xc_names)
    dic["pseudo_metadata"] = OrderedDict(sorted(dic["pseudo_metadata"].items(), key=lambda x: x[1]["Z_val"]))
    json.dump(dic,fjson,indent=1,separators=(",",": "))
    fjson.close()

# Build tarball(s) with entire table
  for root, dirs, files in os.walk(tmp_dir):
    for dir_name in dirs:
      tar_name = os.path.join(github_table_folder,dir_name)+'.tar.gz'
      if isfile_case_sensitive(tar_name): os.remove(tar_name)
      tarf = tarfile.open(name=tar_name, mode='x:gz')
      tarf.add(os.path.join(root,dir_name),arcname=dir_name)
      tarf.close()

# Remove tmp dir
  shutil.rmtree(tmp_dir,ignore_errors=True)

#=========================================
def main_create_html_from_table(table_folder,html_folder):
  """Read data in table_folder and create html_folder structure"""

# Table info
  table_name = table_name_from_string(os.path.split(table_folder)[1])
  table_version = table_version_from_string(table_name)
  ddb_info_filename = None
  ddb = database_info()

# Create github destination directory
  if not exists_case_sensitive(html_folder): os.makedirs(html_folder,exist_ok=True)

# Copy website template into destination directory
  pdf_name = None
  table_pdf_found = "none"
  only_index=True if len(os.listdir(html_folder)) > 0 else False
  for root, dirs, files in os.walk(table_folder):
    for ff in files:
      if isfile_case_sensitive(os.path.join(root,ff)) and os.path.splitext(ff)[-1].lower() == ".pdf":
        table_pdf_found = os.path.join(root,ff) ; break
  existing_pdf_found = "none"
  for root, dirs, files in os.walk(os.path.join(html_folder,atomicdata_folder)):
    for ff in files:
      if isfile_case_sensitive(os.path.join(root,ff)) and os.path.splitext(ff)[-1].lower() == ".pdf":
        existing_pdf_found = os.path.join(root,ff) ; break
  if existing_pdf_found != "none":
    pdf_name = os.path.basename(existing_pdf_found)
  elif table_pdf_found != "none":
    pdf_name = table_name+".pdf"
  else:
    pdf_name = None
  if existing_pdf_found != "none" or table_pdf_found != "none":
    copy_html_template(html_folder,only_index_specie=only_index, \
                       pdf_table_path=os.path.join("..","..",atomicdata_folder,pdf_name))
    if table_pdf_found != "none":
      shutil.copy2(table_pdf_found,os.path.join(html_folder,atomicdata_folder,pdf_name))            
  else:
    copy_html_template(html_folder,only_index_specie=only_index)

# Make tmp dir
  tmp_dir = os.path.join(html_folder,"tmp")
  if isdir_case_sensitive(tmp_dir): shutil.rmtree(tmp_dir,ignore_errors=True)
  os.makedirs(tmp_dir,exist_ok=True)

# Explore root directory and copy files to destination
  for root, dirs, files in os.walk(table_folder):
    for file_name in files:
      file_bodyname, file_ext = os.path.splitext(file_name)
      file_fullname = os.path.join(root,file_name)
      file_specie = specie_from_filename(file_name)
      if isfile_case_sensitive(file_fullname):

        if file_specie in specie.keys():
          specie_dirname=os.path.join(atomicdata_folder,"%03d-%s" % (int(specie[file_specie][1]),file_specie.lower()))
          specie_dir_dest = os.path.join(html_folder,specie_dirname)

#         Process XML file(s)
          if file_ext == '.xml' or file_ext == ".XML":
            if string_is_in_file(["<paw_dataset version=","<paw_setup version="],file_fullname):
              pawdt = paw_dataset(xml_filename=file_fullname)
              #Store file for tarball
              xc_dir = os.path.join(tmp_dir,jth_short_name+"-v"+table_version+"-"+pawdt.xc_type+"-"+pawdt.xc_name+"-atomicdata")
              if len(pawdt.xc_name)>0 and pawdt.xc_name not in ddb.xc_names:
                ddb.xc_names.append(pawdt.xc_name)
                os.makedirs(xc_dir,exist_ok=True)
              shutil.copy2(file_fullname,xc_dir)            
              #Copy file
              shutil.copy2(file_fullname,specie_dir_dest)                           
              #Create input file
              file_input_dest = os.path.join(specie_dir_dest,file_bodyname+".atompaw.input")
              upf_name1=os.path.join(root,file_bodyname + ".upf")
              upf_name2=os.path.join(root,file_bodyname + ".UPF")
              if isfile_case_sensitive(upf_name1): pawdt.read_from_upf(upf_name1)
              if isfile_case_sensitive(upf_name2): pawdt.read_from_upf(upf_name2)
              merged_input_file=pawdt.merge_xml_upf_input()
              if len(merged_input_file) > 0:
                finput = open(file_input_dest,'w')
                finput.write("".join(merged_input_file))
                finput.close()

#         Process UPF file(s)
          elif file_ext == '.upf' or file_ext == ".UPF":
            if string_is_in_file(["<UPF version="],file_fullname):
              pawdt = paw_dataset(upf_filename=file_fullname)
              #Store file for tarball
              xc_dir = os.path.join(tmp_dir,jth_short_name+"-v"+table_version+"-"+pawdt.xc_type+"-"+pawdt.xc_name+"-atomicdata")
              if len(pawdt.xc_name)>0 and pawdt.xc_name not in ddb.xc_names:
                ddb.xc_names.append(pawdt.xc_name)
                os.makedirs(xc_dir,exist_ok=True)
              shutil.copy2(file_fullname,xc_dir)            
              #Copy file
              shutil.copy2(file_fullname,specie_dir_dest)

#       Process table PDF file
        if file_ext == '.pdf' and len(os.path.split(file_bodyname)[0]) == 0:
          file_dest = os.path.join(html_folder,atomicdata_folder,table_name+'.pdf')
          shutil.copy2(file_fullname,file_dest)

#       Process "Comments" file
        if file_name == comment_filename:
          ddb_info_filename = os.path.join(tmp_dir,info_filename)
          infofile_from_commentfile(file_fullname,ddb_info_filename)

# Initialize database from info file
  if ddb_info_filename is not None:
    ddb.read_from_txt(txt_filename=ddb_info_filename)
  else:
    raise ValueError("No Comments file found in table_folder!")

# Explore destination (html) directory and build index.html files
  for root, dirs, files in os.walk(os.path.join(html_folder,atomicdata_folder)):
    for dir_name in dirs:
      dir_fullname = os.path.join(root,dir_name)
      dir_specie = specie_from_dirname(dir_name)

#     Search all relevant files in directory
      file_list = {}
      for ff in os.listdir(dir_fullname):
        ff_name, ff_ext = os.path.splitext(ff)
        ff_name = os.path.split(ff_name)[-1]
        if ff_ext == ".input" and os.path.splitext(ff_name)[1] == ".atompaw":
          ff_name = os.path.splitext(ff_name)[0] ; ff_ext = ".atompaw.input"
        if ff_ext in (".xml",".XML",".upf",".UPF",".atompaw.input"):
          if ff_name in file_list.keys():
            file_list[ff_name].append(ff_ext)
          else:
            file_list[ff_name] = [ff_ext]

#     Modify index.html file
      html_lines = []
      for dtset in file_list.keys():
        if file_list[dtset]:
      
#         Retrieve dataset info from different xml/upf files
          pawdt = paw_dataset()
          for f_ext in file_list[dtset]:
            if f_ext.lower() == ".xml":
              pawdt.read_from_xml(xml_filename=os.path.join(dir_fullname,dtset+f_ext))
            if f_ext.lower() == ".upf":
              pawdt.read_from_upf(upf_filename=os.path.join(dir_fullname,dtset+f_ext))
            if f_ext.lower() == ".atompaw.input":
              pawdt.inp_file_name = dtset+f_ext
          if pawdt.xml_file_name in ddb.filename_list:
            pawdt_info = ddb.info_list[ddb.filename_list.index(pawdt.xml_file_name)]
            pawdt.read_from_info(dataset_info=pawdt_info)
          if pawdt.upf_file_name in ddb.filename_list:
            pawdt_info = ddb.info_list[ddb.filename_list.index(pawdt.upf_file_name)]
            pawdt.read_from_info(dataset_info=pawdt_info)

#         Define content to write in index.html file
          html_lines += pawdt.html_lines(".")

#     Write new lines in index.html, if any
      if len(html_lines)>0:
        fname = os.path.join(dir_fullname,indexhtml_filename)
        #Delete "Not available" line if present
        file_delete_lines(fname,line_list=["ot available"])
        #Write new lines
        file_add_lines(fname,line_before="INSERT HERE PAW DATASETS - BOTTOM",line_list=html_lines)

# Build tarball(s) with entire table
  for root, dirs, files in os.walk(tmp_dir):
    for dir_name in dirs:
      tar_name = os.path.join(html_folder,atomicdata_folder,dir_name)+'.tar.gz'
      if isfile_case_sensitive(tar_name): os.remove(tar_name)
      tarf = tarfile.open(name=tar_name, mode='x:gz')
      tarf.add(os.path.join(root,dir_name),arcname=dir_name)
      tarf.close()

# Modify global index file
  tarball_src_folder = os.path.join(html_folder,atomicdata_folder)
  tarball_folder_link = atomicdata_folder
  modify_global_index(ddb,table_name,pdf_name,html_folder,tarball_src_folder, \
                      tarball_folder_link,reset_tarbal=True)

# Remove tmp dir
  shutil.rmtree(tmp_dir,ignore_errors=True)


#=========================================
def main_create_inputs_from_table(table_folder,inputs_folder,add_corewf=False):
  """Read data in table_folder and create a folder containing all Atompaw inputs"""

# Read table info
  table_name = table_name_from_string(os.path.split(table_folder)[1])
  table_version = table_version_from_string(table_name)
  inputs_table_folder = os.path.join(inputs_folder,table_name)

# Create github destination directory
  if not exists_case_sensitive(inputs_table_folder): os.makedirs(inputs_table_folder,exist_ok=True)

# Create specie directories in destination folder
  for sp_name in specie.keys():
    fname=os.path.join(inputs_table_folder,sp_name)
    if not exists_case_sensitive(fname): os.makedirs(fname,exist_ok=True)

# Explore root directory
  for root, dirs, files in os.walk(table_folder):
    for file_name in files:
      file_bodyname, file_ext = os.path.splitext(file_name)
      file_fullname = os.path.join(root,file_name)
      file_specie = specie_from_filename(file_name)
      if os.path.isfile(file_fullname):

        if file_specie in specie.keys():
          dir_dest = os.path.join(inputs_table_folder,file_specie)

#         Process XML file
          if file_ext == ".xml" or file_ext == ".XML":
            if string_is_in_file(["<paw_dataset version=","<paw_setup version="],file_fullname):
              pawdt = paw_dataset(xml_filename=file_fullname)
              upf_name1=os.path.join(root,file_bodyname + ".upf")
              upf_name2=os.path.join(root,file_bodyname + ".UPF")
              if isfile_case_sensitive(upf_name1): pawdt.read_from_upf(upf_name1)
              if isfile_case_sensitive(upf_name2): pawdt.read_from_upf(upf_name2)
              merged_input_file=pawdt.merge_xml_upf_input(add_corewf=add_corewf)
              file_input_dest = os.path.join(dir_dest,file_bodyname+".atompaw.input")
              if len(merged_input_file) > 0:
                finput = open(file_input_dest,'w')
                finput.write("".join(merged_input_file))
                finput.close()

#         Process UPF file, if XML file does not exist
          if file_ext == ".upf" or file_ext == ".UPF":
            if string_is_in_file(["<UPF version="],file_fullname):
              xml_name1=os.path.join(root,file_bodyname + ".xml")
              xml_name2=os.path.join(root,file_bodyname + ".XML")
              if not isfile_case_sensitive(xml_name1) and not isfile_case_sensitive(xml_name2):
                pawdt = paw_dataset(upf_filename=file_fullname)
                file_input_dest = os.path.join(dir_dest,file_bodyname+".atompaw.input")
                if len(pawdt.input_file_upf) > 0:
                  finput = open(file_input_dest,'w')
                  finput.write("".join(pawdt.input_file_upf))
                  finput.close()


#=========================================
def main_create_html_from_github(html_folder,github_table_folder,with_subdirs=False):
  """Read data in github_table_folder and create html_folder structure"""
# Option:
#   with_subdirs: False = creates ATOMIDATA/xxx-yy.html files
#                 True  = creates ATOMICDATA/xxx-yy/index.html files

# Table info
  table_name = table_name_from_string(os.path.split(github_table_folder)[1])
  table_version = table_version_from_string(table_name)
  github_table_link  = github_link+"/raw/main/"+github_subfolder+"/"+table_name

# Create github destination directory
  if not exists_case_sensitive(html_folder): os.makedirs(html_folder,exist_ok=True)

# Copy website template into destination directory
  table_pdf_found = False ; table_pdf_name = None
  if len(os.listdir(html_folder)) == 0:
    table_pdf_found = isfile_case_sensitive(os.path.join(github_table_folder,table_name+".pdf"))
    table_pdf_name = table_name+".pdf" if table_pdf_found else None
    if table_pdf_found:
      copy_html_template(html_folder,with_subdirs=with_subdirs, \
           pdf_table_path=os.path.join(github_table_link,table_name+".pdf"))
    else:
      copy_html_template(html_folder,with_subdirs=with_subdirs)
 
# Initialize database from info file
  ddb_info_filename = os.path.join(github_table_folder,info_filename)
  if isfile_case_sensitive(ddb_info_filename):
    ddb = database_info(txt_filename=ddb_info_filename)
  else:
    raise ValueError("No DDB file found in github_table_folder!")

# Explore root directory
  for root, dirs, files in os.walk(github_table_folder):
    for dir_name in dirs:
      dir_fullname = os.path.join(root,dir_name)
      dir_specie = specie_from_dirname(dir_name)

      if dir_specie in specie.keys():
        if with_subdirs:
          specie_dir_dest=os.path.join(html_folder,atomicdata_folder,"%03d-%s" % \
                          (int(specie[dir_specie][1]),dir_specie.lower()))
          specie_indexfile_dest=indexhtml_filename
        else:
          specie_dir_dest=os.path.join(html_folder,atomicdata_folder)
          specie_indexfile_dest="%03d-%s.html" % (int(specie[dir_specie][1]),dir_specie.lower())

#       Search all relevant files in directory
        file_list = {}
        for ff in os.listdir(dir_fullname):
          ff_name, ff_ext = os.path.splitext(ff)
          ff_name = os.path.split(ff_name)[-1]
          if ff_ext == ".input" and os.path.splitext(ff_name)[1] == ".atompaw":
            ff_name = os.path.splitext(ff_name)[0] ; ff_ext = ".atompaw.input"
          if ff_ext in (".xml",".XML",".upf",".UPF",".atompaw.input"):
            if ff_name in file_list.keys():
              file_list[ff_name].append(ff_ext)
            else:
              file_list[ff_name] = [ff_ext]

#       Modify index.html file
        html_lines = []
        for dtset in file_list.keys():
          if file_list[dtset]:

#           Retrieve dataset info from different xml/upf files
            pawdt = paw_dataset()
            for f_ext in file_list[dtset]:
              if f_ext.lower() == ".xml":
                pawdt.read_from_xml(xml_filename=os.path.join(dir_fullname,dtset+f_ext))
              if f_ext.lower() == ".upf":
                pawdt.read_from_upf(upf_filename=os.path.join(dir_fullname,dtset+f_ext))
              if f_ext.lower() == ".atompaw.input":
                pawdt.inp_file_name = dtset+f_ext
            if pawdt.xml_file_name in ddb.filename_list:
              pawdt_info = ddb.info_list[ddb.filename_list.index(pawdt.xml_file_name)]
              pawdt.read_from_info(dataset_info=pawdt_info)
            if pawdt.upf_file_name in ddb.filename_list:
              pawdt_info = ddb.info_list[ddb.filename_list.index(pawdt.upf_file_name)]
              pawdt.read_from_info(dataset_info=pawdt_info)
            if len(pawdt.xc_name)>0 and pawdt.xc_name not in ddb.xc_names:
              ddb.xc_names.append(pawdt.xc_name)

#           Define content to write in index.html file
            html_lines += pawdt.html_lines(os.path.join(github_table_link,dir_specie))

#       Write new lines in index.html, if any
        if len(html_lines)>0:
          fname = os.path.join(specie_dir_dest,specie_indexfile_dest)
          #Delete "Not available" line if present
          file_delete_lines(fname,line_list=["ot available"])
          #Write new lines
          file_add_lines(fname,line_before="INSERT HERE PAW DATASETS - BOTTOM",line_list=html_lines)

# Modify global index file
  tarball_src_folder = github_table_folder
  tarball_folder_link = github_table_link
  modify_global_index(ddb,table_name,table_pdf_name,html_folder,tarball_src_folder,\
                      tarball_folder_link,with_subdirs=with_subdirs)


#--------------------------------------------------------------------------------
# CLASSES

#=========================================
class paw_dataset:
  """A class for the paw datasets"""

#-----------------------------------------
# Set default values
  def __init__(self,xml_filename=None,upf_filename=None,dataset_info=[]):

    self.xml_file_name   = "unknown"
    self.upf_file_name   = "unknown"
    self.inp_file_name   = "unknown"
    self.file_xml_md5    = None
    self.file_upf_md5    = None
    self.symbol          = None
    self.category        = "unknown"
    self.status          = "unknown"
    self.lmax            = None
    self.charge          = None
    self.core            = None
    self.vale            = None
    self.ecut_low        = None
    self.ecut_medium     = None
    self.ecut_high       = None
    self.xc_type         = "unknown"
    self.xc_name         = "unknown"
    self.gen_type        = "unknown"
    self.gen_name        = "unknown"
    self.rpaw            = None
    self.delta           = None
    self.delta1          = None
    self.valence         = []
    self.comment         = []
    self.input_file_xml  = []
    self.input_file_upf  = []
    self.input_xml_lines = None
    self.input_upf_lines = None
    self.estruct_short   = "unknown"

    if xml_filename is not None:
      self.read_from_xml(xml_filename)

    if upf_filename is not None:
      self.read_from_upf(upf_filename)

    if dataset_info != []:
      self.read_from_info(dataset_info)

#-----------------------------------------
# Print object
  def __str__(self):
    stg= 'Object of type paw_dataset:\n' \
     + '  XML file_name = '+ self.xml_file_name+'\n' \
     + '  UPF file_name = '+ self.upf_file_name+'\n' \
     + '  INP file_name = '+ self.inp_file_name+'\n' \
     + '  XML md5   = '+ (self.file_xml_md5 if self.file_xml_md5 is not None else "None") +'\n' \
     + '  UPF md5   = '+ (self.file_upf_md5 if self.file_upf_md5 is not None else "None") +'\n' \
     + '  generator = ('+ self.gen_type+', '+self.gen_name+')\n' \
     + '  xc        = ('+ self.xc_type+', '+self.xc_name+')\n' \
     + '  symbol    = '+ (self.symbol if self.symbol is not None else "None") +'\n' \
     + '  charge    : tot='+ (str(self.charge) if self.charge is not None else "None") \
     + ', core='+ (str(self.core) if self.core is not None else "None") \
     + ', val='+ (str(self.vale) if self.vale is not None else "None") +'\n' \
     + '  rpaw      = '+ (str(self.rpaw) if self.rpaw is not None else "None") +'\n' \
     + '  delta[1]  = ('+ (str(self.delta) if self.delta is not None else "None") +', ' \
                        + (str(self.delta1) if self.delta1 is not None else "None") +')\n' \
     + '  ecut      = ('+ (str(self.ecut_low) if self.ecut_low is not None else "None") + ', ' \
                        + (str(self.ecut_medium) if self.ecut_medium is not None else "None") +', ' \
                        + (str(self.ecut_high) if self.ecut_high is not None else "None") +')\n'
    stg += '  valence:\n'
    for vv in self.valence:
      stg += '    n='+str(vv[0])+', l='+str(vv[1])
      stg += ', e='+str(vv[2])+', f='+str(vv[3])+'\n'
    stg += '  comment:\n'
    for cm in self.comment:
      stg += '    ['+str(cm)+']\n'
    stg += '  input file (XML):\n'
    for ip in self.input_file_xml:
      stg += '    | '+str(ip)
    stg += '  input file (UPF):\n'
    for ip in self.input_file_upf:
      stg += '    | '+str(ip)
    stg += '  input_xml_lines:\n'
    if self.input_xml_lines is not None:
      stg += '    ['+str(self.input_xml_lines[0])+', '+str(self.input_xml_lines[1])+']\n'
    stg += '  input_upf_lines:\n'
    if self.input_upf_lines is not None:
      stg += '    ['+str(self.input_upf_lines[0])+', '+str(self.input_upf_lines[1])+']\n'

    return stg

#-----------------------------------------
# Read properties from XML file
  def read_from_xml(self,xml_filename):
  
#   Check presence of input file
    if not isfile_case_sensitive(xml_filename):
      raise ValueError("File "+xml_filename+" does not exist!")

#   Get MD5 checksum of XML sile
    self.file_xml_md5 = hashlib.md5(open(xml_filename,'rb').read()).hexdigest()

#   Read input file
    if self.input_file_xml == []:
      fxml = open(xml_filename,'r')
      flines = fxml.readlines()
      fxml.close()

#   Get input file
    if self.input_file_xml == []:
      try:
        ind1 = flines.index("<!-- Program:  atompaw - input data follows: \n")
        ind2 = flines.index(" Program:  atompaw - input end -->\n")
        self.input_file_xml = flines[ind1+1:ind2]
      except:
        self.input_file_xml = []

#   Read XML options in input file
    if len(self.input_file_xml) > 0:
      index_xml = next((i for i,stg in enumerate(self.input_file_xml) if 'xmlout' in stg.lower()), None)
      self.input_xml_lines = self.input_file_xml[index_xml:index_xml+2]

#   Read content of the file and fill object
    self.xml_file_name = os.path.split(xml_filename)[-1]
    tree = etree.parse(xml_filename)
    
#   Get atom data
    atom = tree.xpath("atom")[0]
    if self.symbol is None: self.symbol = atom.get("symbol")
    if self.charge is None: self.charge = float(atom.get("Z"))
    if self.vale is None: self.vale = float(atom.get("valence"))
    if self.core is None: self.core = float(atom.get("core"))

#   Get ecut data
    if tree.find("pw_ecut") is not None:
      ecut = tree.xpath("pw_ecut")[0]
      if self.ecut_low is None: self.ecut_low = float(ecut.get("low"))
      if self.ecut_medium is None: self.ecut_medium = float(ecut.get("medium"))
      if self.ecut_high is None: self.ecut_high = float(ecut.get("high"))
    else:
      self.ecut_low    = None
      self.ecut_medium = None
      self.ecut_high   = None

#   Get XC data
    xc = tree.xpath("xc_functional")[0]
    if self.xc_type == "unknown": self.xc_type = xc.get("type")
    if self.xc_name == "unknown":
      self.xc_name = xc.get("name")
      if self.xc_name == "LDA_X+LDA_C_PW": self.xc_name = "PW"
      if self.xc_name == "GGA_X_PBE+GGA_C_PBE": self.xc_name = "PBE"
      if self.xc_name == "GGA_X_PBE_SOL+GGA_C_PBE_SOL": self.xc_name = "PBEsol"

#   Get generator data
    gen = tree.xpath("generator")[0]
    if self.gen_type == "unknown": self.gen_type = gen.get("type")
    if self.gen_name == "unknown": self.gen_name = gen.get("name")
    # If generator name doesnt contain the version number, try to find it in the comments
    pattern = r"\b\d+\.\d+\.\d+\.\d+\b"
    if not re.search(pattern, self.gen_name):
      index_ver = next((i for i,stg in enumerate(flines) if 'contact info' in stg.lower()), None)
      if index_ver > 0:
        wds = flines[index_ver-1].lower().split()
        index_ver = wds.index("atompaw")+1
        if index_ver > 0: self.gen_name += "-" + wds[index_ver]

#   Get PAW radius
    check_rpaw = tree.xpath("paw_radius")
    if len(check_rpaw) == 0: check_rpaw = tree.xpath("PAW_radius")
    rpaw = check_rpaw[0]
    check_rc = rpaw.get("rc")
    if check_rc is None: check_rc = rpaw.get("rpaw")
    if self.rpaw is None and check_rc is not None: self.rpaw = float(check_rc)

    if self.valence == []:
      valence = tree.xpath("valence_states/state")
      self.valence = [] ; self.lmax = -1
      for vale in valence:
        if vale.get("l") is not None:
          self.lmax=max(self.lmax,int(vale.get("l")))
        if vale.get("n") is None:
          nn=-1
        else:
          nn=int(vale.get("n"))
          if nn > 10: nn=-1
        if vale.get("f") is None:
          ff=-1.0
        else:
          ff=float(vale.get("f"))
        self.valence.append((nn,int(vale.get("l")),float(vale.get("e")),ff))
    
#   Check charge
    vale_charge = sum([vv[3] if vv[0]>0 else 0. for vv in self.valence])
    if vale_charge != self.vale:
      print("Inconsistency between occupations and valence charge!")
      print("File name : "+self.xml_file_name)
      print("vale : "+str(self.vale))
      print("vale_charge : "+str(vale_charge))
      raise ValueError("Check XML file!")

#   Get electronic structure
    if self.estruct_short == "unknown":
      self.estruct_short = self.electronic_structure(option="short")
 
#-----------------------------------------
# Read properties from UPF file
  def read_from_upf(self,upf_filename):
  
#   Check presence of input file
    if not isfile_case_sensitive(upf_filename):
      raise ValueError("File "+upf_filename+" does not exist!")

#   Get MD5 checksum of UPF sile
    self.file_upf_md5 = hashlib.md5(open(upf_filename,'rb').read()).hexdigest()

#   Read file
    fupf = open(upf_filename,'r')
    flines = fupf.readlines()
    fupf.close()

#   Get input file
    if self.input_file_upf == []:
      try:
        ind1 = flines.index("         UPF file from ATOMPAW code with following input\n")
        ind2 = flines.index("  </PP_INFO>\n")
        self.input_file_upf = flines[ind1+1:ind2]
      except:
        self.input_file_upf = []

#   Read UPF options in input file
    if len(self.input_file_upf) > 0:
      #index_upf = next((i for i,stg in enumerate(self.input_file_upf) if 'upfout' in stg.lower()), None)
      index_upf = next((i for i,stg in enumerate(self.input_file_upf) if not any(sub in stg.lower() for sub in ['upfout','pwscfout'])), None)
      self.input_upf_lines = self.input_file_upf[index_upf:index_upf+2]
    
#   Get UPF file name
    self.upf_file_name = o.path.split(upf_filename)[-1]

#   Loop over UPF lines:
    for line in flines:
    
#     Get atom data
      if "element=" in line:
        if self.symbol is None: self.symbol = line.split("\"")[1].strip()
        if self.charge is None: self.charge = float(specie[self.symbol][1])
      if "z_valence=" in line:
        if self.vale is None: self.vale = float(line.split("\"")[1].strip())
        if self.core is None and self.charge != None: self.core = self.charge - self.vale

#     Get XC data
      if "functional=" in line:
        xc_string = line.split("\"")[1].strip()
        if "PZ" in xc_string and "NOGX" in xc_string and "NOGC" in xc_string:
          if self.xc_type == "unknown": self.xc_type = "LDA"
          if self.xc_name == "unknown": self.xc_name = "PZ"
        if "PW" in xc_string and "NOGX" in xc_string and "NOGC" in xc_string:
          if self.xc_type == "unknown": self.xc_type = "LDA"
          if self.xc_name == "unknown": self.xc_name = "PW"
        if "PW" in xc_string and "PBX" in xc_string and "PBC" in xc_string:
          if self.xc_type == "unknown": self.xc_type = "GGA"
          if self.xc_name == "unknown": self.xc_name = "PBE"
        if "PW" in xc_string and "PSX" in xc_string and "PSC" in xc_string:
          if self.xc_type == "unknown": self.xc_type = "GGA"
          if self.xc_name == "unknown": self.xc_name = "PBESOL"

#     Get generator data
      if "relativistic=" in line:
        if self.gen_name == "unknown": self.gen_name = "atompaw"
        rel_string = line.split("\"")[1].strip()
        if self.gen_type == "unknown":
          if rel_string == "no": self.gen_type = "non-relativistic"
          if rel_string != "no": self.gen_type = "relativistic"

#     Get l_max
      if "l_max=" in line:
        if self.l_max is None: self.l_max = int(line.split("\"")[1].strip())

#   Get electronic structure
    if self.estruct_short != "unknown":
      self.estruct_short = self.electronic_structure(option="short")

      #self.ecut_low    = float()
      #self.ecut_medium = float()
      #self.ecut_high   = float()
      #self.rpaw        = float()
      #self.valence     = []

#-----------------------------------------
# Merge content of UPF and XML input files 
  def merge_xml_upf_input(self,force_default=False,add_corewf=False):
  
    merged_input_file=[]

    # Suppress XML input lines
    if len(self.input_file_xml) > 0:
      if self.input_xml_lines is not None:
        merged_input_file = [s for s in self.input_file_xml if not any(sub in s for sub in self.input_xml_lines)]
      else:
        merged_input_file = self.input_file_xml

    # Suppress UPF input lines
    if len(merged_input_file) == 0:
      if len(self.input_file_upf) > 0:
        if self.input_upf_lines is not None:
          merged_input_file = [s for s in self.input_file_upf if not any(sub in s for sub in self.input_upf_lines)]
        else:
          merged_input_file=self.input_file_upf

    # Add XML and UPF input lines if any
    if len(merged_input_file) > 0:
      index_end = next((i for i, s in enumerate(merged_input_file) if 'END' in s), None)
      if index_end is not None:
        if self.input_xml_lines is not None and not force_default:
          xml_lines = self.input_xml_lines
        else:
          xml_lines = input_xml_lines_def
        xml_lines[1] = xml_lines[1].lower()
        if add_corewf and not 'prtcorewf' in xml_lines[1]:
          xml_lines[1] = 'prtcorewf ' + xml_lines[1].replace('default','')
        merged_input_file[index_end:index_end] = xml_lines
      index_end = next((i for i, s in enumerate(merged_input_file) if 'END' in s), None)
      if index_end is not None:
        if self.input_upf_lines is not None and not force_default:
          merged_input_file[index_end:index_end] = self.input_upf_lines
        else:
          merged_input_file[index_end:index_end] = input_upf_lines_def

    return merged_input_file

#-----------------------------------------
 # Read properties from dataset_info object
  def read_from_info(self,dataset_info):
 
    if self.symbol == None:
      if len(dataset_info[0])>0: self.symbol = dataset_info[0].capitalize()
    elif self.symbol != dataset_info[0]:
      print("Atomic symbol: inconsistency between XML and database_info!")
      print("Symbol=%s, DT_info=%s" % (self.symbol,dataset_info[0]))
      sys.exit()

    if self.xml_file_name == "unknown":
      if len(dataset_info[1])>0: self.xml_file_name = dataset_info[1]
    elif self.xml_file_name != dataset_info[1]:
      print("File name: inconsistency between XML and database_info!")
      print("xml_file_name=%s, DT_info=%s" % (self.xml_file_name,dataset_info[1]))
      sys.exit()

    if len(dataset_info[2])>0: self.category = dataset_info[2]
    if len(dataset_info[3])>0: self.status   = dataset_info[3]
    if len(dataset_info[4])>0: self.delta    = dataset_info[4]
    if len(dataset_info[5])>0: self.delta1   = dataset_info[5]
    if len(dataset_info)>6   : self.comment  = dataset_info[6:]


#-----------------------------------------
# Set "pseudo-dojo" dictionnary
  def set_pseudodojo_dict(self):

    pseudodojo_dict = atom_info_def.copy()
    pseudodojo_dict["hints"] = atom_info_def["hints"].copy()
    pseudodojo_dict["hints"]["low"]    = atom_info_def["hints"]["low"].copy()
    pseudodojo_dict["hints"]["normal"] = atom_info_def["hints"]["normal"].copy()
    pseudodojo_dict["hints"]["high"]   = atom_info_def["hints"]["high"].copy()

    if self.xml_file_name != "unknown":
      pseudodojo_dict["basename"] = self.xml_file_name
    if self.charge is not None:
      pseudodojo_dict["Z_val"] = float(self.charge)
    if self.lmax is not None:
       pseudodojo_dict["l_max"] = self.lmax
    if self.file_xml_md5 is not None:
       pseudodojo_dict["md5"] = self.file_xml_md5
    if self.delta is not None:
       pseudodojo_dict["dfact_meV"] = self.delta
    if self.delta1 is not None:
       pseudodojo_dict["dfactprime_meV"] = self.delta1
    if self.ecut_low is not None:
       pseudodojo_dict["hints"]["low"]["ecut"] = self.ecut_low
    if self.ecut_medium is not None:
       pseudodojo_dict["hints"]["normal"]["ecut"] = self.ecut_medium
    if self.ecut_high is not None:
       pseudodojo_dict["hints"]["high"]["ecut"] = self.ecut_high

    return pseudodojo_dict

#-----------------------------------------
# Find electronic structure (as a string)
  def electronic_structure(self,option="full"):

    #Valence
    estruct_vale = ''
    if len(self.valence)>0:
      valence_sorted = sorted(self.valence, key=lambda state: state[2])
      shell_vale = []
      for vv in valence_sorted:
        if vv[0]>0:
          shell_vale.append([vv[0],vv[1]])
          if len(estruct_vale)>0: estruct_vale += ' '
          estruct_vale += str(vv[0])+shell_name[vv[1]]+str(int(vv[3]))

    #Core
    estruct_core = ''
    core_charge=0. ; nn=0
    if self.core is not None:
      while core_charge < self.core:
        if shell_core[nn] not in shell_vale:
          shl,ll = shell_core[nn]
          core_charge += shell_charge[ll]
          if len(estruct_core)>0: estruct_core += ' '
          estruct_core += str(shl)+shell_name[ll]+str(shell_charge[ll])
        nn += 1
    if core_charge != self.core:
      print("Inconsistency between occupations and core charge!")
      print("File name : "+self.xml_file_name)
      print("core : "+str(self.core))
      print("core_charge : "+str(core_charge))
      raise ValueError("Check XML file!")

    #Replace by short version
    if option == "short":
      for rg in reversed(rare_gas):
        if rg[0] in estruct_core:
          estruct_core = estruct_core.replace(rg[0],rg[1])
          break

    if estruct_vale != '':
      return '['+estruct_core+'] ' + estruct_vale
    else:
      return 'core: ['+estruct_core+'] , valence: ' + str(self.vale) + 'electrons'

#-----------------------------------------
# Return lines describing the dataset, to be written in html
#  file_location = where the xml/upf/input files are located
  def html_lines(self,file_location="."):

    if self.xml_file_name == "unknown" and self.upf_file_name == "unknown": return

    my_html_lines = []
    my_html_lines.append('    <ul>\n')
    my_html_lines.append('      <b>PAW dataset: </b>\n')
    if self.xml_file_name != "unknown":
      my_html_lines.append('      <a href="'+file_location+'/'+self.xml_file_name+'">'+self.xml_file_name+'</a>\n')
      if self.upf_file_name != "unknown":
        my_html_lines.append('      ,&nbsp;<a href="./'+self.upf_file_name+'">'+self.upf_file_name+'</a>\n')
    elif self.upf_file_name != "unknown":
      my_html_lines.append('      <a href="./'+self.upf_file_name+'">'+self.upf_file_name+'</a>\n')
    my_html_lines.append('    </ul>\n')
    my_html_lines.append('    <dl style="margin-left: 40px;">\n')
    if self.status != "unknown":
      my_html_lines.append('      Status: <b>recommended</b><br>\n')
    my_html_lines.append('      Exchange-correlation functional: '+self.xc_type+" - "+self.xc_name+'<br>\n')
    my_html_lines.append('      Electronic structure ([core] val): '+self.estruct_short+'<br>\n')
    if self.rpaw is not None:
      my_html_lines.append('      Augmentation radius: %.2f a.u.<br>\n' % round(self.rpaw,2))
    if self.delta is not None and self.delta1 is not None:
      my_html_lines.append('      <a href="https://molmod.ugent.be/deltacodesdft" target="_blank">Delta factor</a>:\n')
      my_html_lines.append('      &Delta;-value= '+str(self.delta)+' meV, &Delta;<sub>1</sub>-value= '+str(self.delta1)+' meV<br>\n')
    if self.ecut_low is not None and self.ecut_medium is not None and self.ecut_high is not None:
      my_html_lines.append('      Suggested PW cut-off energies: ' \
          + 'low= %.1f'    % self.ecut_low    + ' Ha, ' \
          + 'medium= %.1f' % self.ecut_medium + ' Ha, ' \
          + 'high= %.1f'   % self.ecut_medium + ' Ha<br>\n')
    if self.gen_name != "unknown":
      my_html_lines.append('      Generator: '+self.gen_name)
      if self.inp_file_name != "unknown":
        my_html_lines.append(' (<a href="'+file_location+'/'+self.inp_file_name+'">input file</a>)<br>\n')
      elif len(self.input_file_xml) > 0 and len(self.input_file_upf) > 0:
        my_html_lines.append(' (input file included in the dataset itself)<br>\n')
      elif len(self.input_file_xml) > 0:
        my_html_lines.append(' (input file included in the XML dataset itself)<br>\n')
      elif len(self.input_file_upf) > 0:
        my_html_lines.append(' (input file included in the UPF dataset itself)<br>\n')
    for cm in self.comment:
      if len(cm)>0:
        my_html_lines.append('      '+cm+'<br>\n')
    my_html_lines.append('    </dl><br>\n')

    return my_html_lines

#-----------------------------------------
# Return lines describing the dataset, to be written in markdown
  def markdown_lines(self,github_table_link="."):

    if self.xml_file_name == "unknown" and self.upf_file_name == "unknown": return

    my_markdown_lines = []  
    my_markdown_lines.append('<br>\n')
    line = '**PAW dataset:**  \n'
    if self.xml_file_name != "unknown":
      line += ' ['+self.xml_file_name+']('+github_table_link+'/'+self.symbol+'/'+self.xml_file_name+')'
      if self.upf_file_name != "unknown":
        line += ', ['+self.upf_file_name+']('+github_table_link+"/"+self.symbol+'/'+self.upf_file_name+')'
    elif self.upf_file_name != "unknown":
      line += ' ['+self.upf_file_name+']('+github_table_link+'/'+self.symbol+'/'+self.upf_file_name+')'
    my_markdown_lines.append(line+'  \n')
    if self.status != "unknown":
      my_markdown_lines.append('Status: **'+self.status+'**  \n')
    my_markdown_lines.append('Exchange-correlation functional: '+self.xc_type+' - '+self.xc_name+'  \n')
    my_markdown_lines.append('Electronic structure ([core] val): '+self.estruct_short+'  \n')
    if self.rpaw is not None:
      my_markdown_lines.append('Augmentation radius: %.2f a.u.  \n' % round(self.rpaw,2))
    if self.delta is not None and self.delta1 is not None:
      my_markdown_lines.append('[Delta factor](https://molmod.ugent.be/deltacodesdft): $\\Delta$-value= ' \
              +str(self.delta) + ' meV, ' + '$\\Delta_1$-value= ' + str(self.delta1) + ' meV  \n')
    if self.ecut_low is not None and self.ecut_medium is not None and self.ecut_high is not None:
      my_markdown_lines.append('Suggested PW cut-off energies: ' \
          + 'low= %.1f'    % self.ecut_low    + ' Ha, ' \
          + 'medium= %.1f' % self.ecut_medium + ' Ha, ' \
          + 'high= %.1f'   % self.ecut_medium + ' Ha  \n')
    if self.gen_name != "unknown":
      my_markdown_lines.append('Generator: '+self.gen_name)
      if self.inp_file_name != "unknown":
        my_markdown_lines.append(' - [input file]('+github_table_link+'/'+self.symbol+'/'+self.inp_file_name+')  \n')
      elif len(self.input_file_xml) > 0 and len(self.input_file_upf) > 0:
        my_markdown_lines.append(' (input file included in the dataset itself)  \n')
      elif len(self.input_file_xml) > 0:
        my_markdown_lines.append(' (input file included in the XML dataset itself)  \n')
      elif len(self.input_file_upf) > 0:
        my_markdown_lines.append(' (input file included in the UPF dataset itself)  \n')
    if len(self.comment)>0:
      for cm in self.comment:
        if len(cm)>0:
          my_markdown_lines.append(cm+'\n')

    return my_markdown_lines


#=========================================
class database_info:
  """A class for the database info (from txt file)"""

#-----------------------------------------
# Init object
  def __init__(self,txt_filename="unknown"):
  
    self.ddb_name      = "unknown"
    self.file_name     = "unknown"
    self.info_list     = []
    self.atom_list     = []
    self.filename_list = []
    self.category_list = []
    self.delta_list    = []
    self.xc_names      = []

    if txt_filename != "unknown":
      self.read_from_txt(txt_filename)

#-----------------------------------------
# Print object
  def __str__(self):
    stg= 'Object of type database_info:\n' \
     + '  file_name = '+self.file_name+'\n' \
     + '  === info: \n'

    for i_inf,inf in enumerate(self.info_list):
      stg += '      '+str(i_inf+1)+': '+', '.join(map(str, inf))+'\n'

    stg += '  === xc_names: '+', '.join(map(str, self.xc_names))+'\n'
    return stg

#-----------------------------------------
# Read data from text file
  def read_from_txt(self,txt_filename):
  
#   Check presence of input file
    if not isfile_case_sensitive(txt_filename):
      raise ValueError("File "+txt_filename+" does not exist!")

    self.name      = txt_filename.split('/')[-2]
    self.file_name = txt_filename.split('/')[-1]

#   Read content of the file and fill object
    file_info = open(txt_filename,"r")
    self.info_list   = []
    for ln in file_info.readlines():
      wd_list = [wd.strip() for wd in ln.split('/')]
      if len(wd_list[0])>0:
        if wd_list[0][0] != '#':
          self.info_list.append(wd_list)
    file_info.close()

#   Extract some data
    self.extract_data()

#-----------------------------------------
# Extract data from info list
  def extract_data(self):

    self.atom_list     = []
    self.filename_list = []
    self.category_list = []
    self.delta_list    = []
    for info in self.info_list:
      self.atom_list.append(info[0])
      self.filename_list.append(info[1])
      if len(info[2])>0 and info[2] not in self.category_list:
        self.category_list.append(info[2])
      if len(info[4])>0 and len(info[5])>0:
        self.delta_list.append([float(info[4]),float(info[5])])
    return None

#-----------------------------------------
# Compute table delta factor (if any)
  def deltafactor(self):

    delta = 0. ; delta1 = 0.
    if len(self.delta_list)>0:
      for dlt in self.delta_list:
        delta += dlt[0] ; delta1 += dlt[1]
      delta  /= len(self.delta_list)
      delta1 /= len(self.delta_list)

    return [delta,delta1]

#=========================================
# Miscelaneous functions

#-----------------------------------------
#MacOS is not case sensistive wrt file names
def exists_case_sensitive(path_name) -> bool:
  my_test = False
  dir_name, name = os.path.split(path_name)
  if dir_name == "": dir_name=os.getcwd()
  if os.path.isdir(dir_name):
    my_test = (name in os.listdir(dir_name))
  return my_test

def isfile_case_sensitive(path_name) -> bool:
  my_test = False
  dir_name, name = os.path.split(path_name)
  if dir_name == "": dir_name=os.getcwd()
  if os.path.isdir(dir_name):
    if name in os.listdir(dir_name):
      my_test = os.path.isfile(path_name)
  return my_test

def isdir_case_sensitive(path_name) -> bool:
  my_test = False
  dir_name, name = os.path.split(path_name)
  if dir_name == "": dir_name=os.getcwd()
  if os.path.isdir(dir_name):
    if name in os.listdir(dir_name):
      my_test = os.path.isdir(path_name)
  return my_test

#-----------------------------------------
#Extract specie from a file name (first characters)
def specie_from_filename(file_name):

 specie_name = file_name.split('.')[0].capitalize()
 if specie_name == file_name:
   specie_name=file_name.split('_')[0].capitalize()
 if specie_name == file_name:
   return None
 else:
   return specie_name

#-----------------------------------------
#Extract specie from a directory name
def specie_from_dirname(dir_name):

 if "-" in dir_name:
   specie_name = dir_name.split('-')[1].capitalize()
 else:
   specie_name = dir_name.capitalize()

 if specie_name in specie.keys():
   return specie_name
 else:
   return None

#-----------------------------------------
#Check if strings are in a file
#strg = [list of possible strings] (or)
def string_is_in_file(strg_list,file_name):

  ff = open(file_name, "r")
  found = False
  while not found:
    line = ff.readline()
    if not line: break
    for st in strg_list:
      found = st in line
      if found: break
  ff.close()

  return found

#-----------------------------------------
#Extract table name from a string
#table_name = <table_type>-<table_xc>-v<table_version>
def table_name_from_string(strg):

  strgup = strg.upper()
  
  table_xc = "XC"
  if "LDA" in strgup: table_xc = "LDA"
  if "GGA" in strgup: xc_name = "GGA"
  if "PW" in strgup: table_xc = "PW"
  if "PBE" in strgup: table_xc = "PBE"
  if "PBESOL" in strgup: table_xc = "PBEsol"
  if "R2SCAN" in strgup: xc_name = "mGGA-R2SCAN"

  table_type = "JTH"
  if "JTH" in strgup:
    table_type = "JTH"
  elif "-" in strgup:
    if table_xc != strgup.split('-')[0]:
      table_type = strgup.split('-')[0]

  table_version = table_version_from_string(strgup)

  table_name = table_type + '-' + table_xc + '-v' + table_version

  return table_name

#-----------------------------------------
#Extract table version from a string
#table_version = x.y
def table_version_from_string(strg):

  table_version = "unknown"
  try:
    attempt = re.search(r'[0-9]+\.[0-9]+', strg).group(0)
  except:
    print("No version number found in table name!")
    sys.exit()
  if len(attempt)>=3: table_version = attempt
  
  return table_version

#-----------------------------------------
#Extract XC name from a string
#xc_name = LDA/PBE/PBEsol/...
def xc_name_from_string(strg):

  strgup = strg.upper()
  
  table_xc = "unknown"
  if "LDA" in strgup: xc_name = "LDA"
  if "GGA" in strgup: xc_name = "GGA"
  if "PW" in strgup: xc_name = "LDA-PW"
  if "PBE" in strgup: xc_name = "GGA-PBE"
  if "PBESOL" in strgup: xc_name = "GGA-PBEsol"
  if "R2SCAN" in strgup: xc_name = "mGGA-R2SCAN"

  return xc_name

#-----------------------------------------
#Replace string(s) in a file
#Example: file_replace_string(file_name,[[old1,new1][old2,new2],...])
def file_replace_string(file_name,strg_list=[]):

  if not isfile_case_sensitive(file_name):
    raise ValueError("File "+file_name+" does not exist!")

  f_in = open(file_name,'r')
  flines = f_in.readlines()
  f_in.close()

  shutil.move(file_name,file_name+".bak")

  f_out = open(file_name,'w')
  for fline in flines:
    for strg in strg_list:
      fline = fline.replace(strg[0],strg[1])
    f_out.write(fline)
  f_out.close()

  os.remove(file_name+".bak")
  return None

#-----------------------------------------
#Delete line(s) containing a string in a file
#Example: file_delete_lines(file_name,[string1,string2,...])
def file_delete_lines(file_name,line_list=[]):

  if not isfile_case_sensitive(file_name):
    raise ValueError("File "+file_name+" does not exist!")

  f_in = open(file_name,'r')
  flines = f_in.readlines()
  f_in.close()

  shutil.move(file_name,file_name+".bak")
  
  f_out = open(file_name,'w')
  for fline in flines:
    if all(line not in fline for line in line_list):
      f_out.write(fline)
  f_out.close()

  os.remove(file_name+".bak")
  return None

#-----------------------------------------
#Delete line(s) between 2 given lines
#Example: file_delete_lines(file_name,line_start,line_end)
def file_delete_lines_between(file_name,line_start="@@@",line_end="@@@"):

  if not isfile_case_sensitive(file_name):
    raise ValueError("File "+file_name+" does not exist!")

  f_in = open(file_name,'r')
  flines = f_in.readlines()
  f_in.close()

  shutil.move(file_name,file_name+".bak")
  
  f_out = open(file_name,'w')
  write_it=True
  for fline in flines:
    if line_end in fline: write_it=True
    if write_it: f_out.write(fline)
    if line_start in fline: write_it=False
  f_out.close()

  os.remove(file_name+".bak")
  return None

#-----------------------------------------
#Add line(s) in a file before a given line
#Example: file_add_lines(file_name,line_before,[line1,line2,...])
def file_add_lines(file_name,line_before="@@@",line_list=[]):

  if not isfile_case_sensitive(file_name):
    raise ValueError("File "+file_name+" does not exist!")

  f_in = open(file_name,'r')
  flines = f_in.readlines()
  f_in.close()

  shutil.move(file_name,file_name+".bak")
  
  f_out = open(file_name,'w')
  for fline in flines:
    if line_before in fline:
      for line in line_list:
        f_out.write(line) 
    f_out.write(fline)
  f_out.close()

  os.remove(file_name+".bak")
  return None

#-----------------------------------------
#Copy website template into destination directory
def copy_html_template(dest_dirname,pdf_table_path=None,with_subdirs=True,only_index_specie=False):

#   with_subdirs: False = creates ATOMIDATA/xxx-yy.html files
#                 True  = creates ATOMICDATA/xxx-yy/index.html files
#   only_index_specie: False = creates all website structure
#                      True  = resets only index.html files (in specie dirs)

  if pdf_table_path is not None:
    table_link_to_pdf = pdf_table_path
  else:
    table_link_to_pdf = link_to_error404

  #Ignore some files
  if with_subdirs:
    ignored_files=shutil.ignore_patterns(specie_html_template)
  else:
    ignored_files=shutil.ignore_patterns(specie_html_template,atomicdata_folder)

  #Copy dir structure
  if not only_index_specie:
    shutil.copytree(website_template,dest_dirname,dirs_exist_ok=True,ignore=ignored_files)
    if not with_subdirs: os.mkdir(os.path.join(dest_dirname,atomicdata_folder))            

  #Copy and modify index.html files
  for root, dirs, files in os.walk(os.path.join(website_template,atomicdata_folder)):
    for dir_name in dirs:
      specie_name = specie_from_dirname(dir_name)
      specie_fullname="%03d-%s" % (int(specie[specie_name][1]),specie_name.lower())
      
      #Copy index.html template
      file_index_src  = os.path.join(website_template,specie_html_template)
      if with_subdirs:
        file_index_dest = os.path.join(dest_dirname,atomicdata_folder,dir_name,indexhtml_filename)
      else:
        file_index_dest = os.path.join(dest_dirname,atomicdata_folder,specie_fullname+'.html')
      shutil.copy(file_index_src,file_index_dest)

      #Modifiy index.html
      strg_list = []
      strg_list.append(["$${ELEM_SHORT}", specie_name])
      strg_list.append(["$${ELEM_LONG}", specie[specie_name][0]])
      strg_list.append(["$${LINK_TO_REF}", table_link_to_pdf])
      strg_list.append(["$${LAST_MODIF_DATE}", last_modif_date])
      strg_list.append(["$${WEBMASTER}", web_master])
      file_replace_string(file_index_dest,strg_list)
      if pdf_table_path is None:
        strg_list=['Some reference results are given','!-- LINK TO PDF -->']
        file_delete_lines(file_index_dest,strg_list)

  return None

#-----------------------------------------
#Modify global index file of the website
# ddb = database object containing table info
# table_name = name of the table
# table_pdf_name = name of the PDF describing the table
# html_folder = destination folder (html table folder)
# tarball_src_folder = folder where to find source tarballs (full tables)
# tarball_folder_link = html link to tarballs in html
def modify_global_index(ddb,table_name,table_pdf_name,html_folder,tarball_src_folder, \
                        tarball_folder_link,with_subdirs=True,reset_tarbal=False):

#   with_subdirs: False = creates ATOMIDATA/xxx-yy.html files
#                 True  = creates ATOMICDATA/xxx-yy/index.html files
#   reset_tarbal: False = Add tar.gz file(s) to the existing ones
#                 True  = Reset tar.gz file list before adding them

  tarball_list = []
  for file_name in os.listdir(tarball_src_folder):
    if os.path.splitext(file_name)[-1] == ".gz": tarball_list.append(file_name)

  strg_list = []
  strg_list.append(["$${JTH_TABLE_VERSION}", "v"+table_version_from_string(table_name)])
  if table_pdf_name != None:
    strg_list.append(["$${JTH_TABLE_PDF}", table_pdf_name])
  if "PBE" in ddb.xc_names:
    strg_list.append(["$${JTH_TABLE_DELTA_VALUE}", "%.2f" % round(ddb.deltafactor()[0],2)])
    strg_list.append(["$${JTH_TABLE_DELTA1_VALUE}", "%.2f" % round(ddb.deltafactor()[1],2)])
  else:
    strg_list.append(["$${JTH_TABLE_DELTA_VALUE}", "N/A"])
    strg_list.append(["$${JTH_TABLE_DELTA1_VALUE}", "N/A"])
  html_lines = []
  for i,file_name in enumerate(tarball_list):
    strg='<a href="'+tarball_folder_link+'/'+file_name+'" target="_blank">'+xc_name_from_string(file_name)+'</a>'
    if len(tarball_list)>1 and i < len(tarball_list)-1: strg += ',&nbsp;'
    html_lines.append(strg+'\n')
  index_full_name = os.path.join(html_folder,globalindex_template)
  file_replace_string(index_full_name,strg_list)

  # Handle tar.gz files
  if reset_tarbal:
    file_delete_lines_between(index_full_name, \
         line_start="<!-- INSERT HERE TARBALLS TO FULL TABLE - START -->", \
         line_end="<!-- INSERT HERE TARBALLS TO FULL TABLE - END -->")
  file_add_lines(index_full_name,line_before="INSERT HERE TARBALLS TO FULL TABLE - END",line_list=html_lines)

  # If needed, in global index file, replace subdirs with html files
  if not with_subdirs:
    pattern = r"(ATOMICDATA/\w+-\w+)/"
    index_full_name = os.path.join(html_folder,globalindex_template)
    with open(index_full_name, "r", encoding="utf-8") as f: content = f.read()
    new_content = re.sub(pattern, r"\1.html", content)
    shutil.move(index_full_name,index_full_name+".bak")
    with open(index_full_name, "w", encoding="utf-8") as f: f.write(new_content)
    os.remove(index_full_name+".bak")

#-----------------------------------------
#From "Comments" file (data_folder), create "dataset_info.txt" file (github_folder)
#if info_file is None or doesnt exists on disk, then create it and write header
#if info_file exists on disk, then append new lines to it
def infofile_from_commentfile(comment_filename,info_filename):

# Read comment_file
  comment_file = open(comment_filename,"r")
  flines = comment_file.readlines()
  comment_file.close()

# Open info_file and write header if necessary
  if info_filename is not None and isfile_case_sensitive(info_filename):
    info_file = open(info_filename,"a")
  else:
    info_file = open(info_filename,"w")
    if flines[0][0] == '#' and "omment" in flines[0]:
      info_file.write(flines[0])
    else:
      info_file.write("# Comments to the "+table_name+" table\n")
    info_file.write("# specie / file name / category / status / delta_factor / delta_factor1 / additional comment(s)\n")
    info_file.write("# =============================================================================================\n")

# Write lines in info_file
  for fline in flines:
    if fline[0] != '#':
      fword = fline.split('/')
      x_specie = fword[0].strip() ; x_filename = fword[1].strip()
      x_core_val = "" ; x_xc = "" ; x_generator = ""
      x_status = "" ; x_category = "" ; x_comment = []
      x_delta = None ; x_delta1 = None ; x_rpaw = None
      for ifw,fw in enumerate(fword[2:]):
        fwl = fw.lower().strip()
        if "ecommended" in fwl:
          x_status   = "recommended"
          x_category = "standard"
        elif "gga" in fwl or "lda" in fwl:
          x_xc = fwl
        elif "s1" in fwl or "s2" in fwl:
          x_core_val = fwl
        elif "rpaw=" in fwl:
          ww = fwl.split()
          for w in ww:
            i = w.find("rpaw=")
            if i >= 0:  x_rpaw  = float(w[i+5:])
        elif "delta" in fwl:
          ww = fwl.split()
          for i,w in enumerate(ww):
            if "delta=" in w:  x_delta  = float(ww[i+1])
            if "delta1=" in w: x_delta1 = float(ww[i+1])
        elif "generator" in fwl:
          x_generator = fwl
        else:
           x_comment.append(fwl)
      info_file.write("%3s / %24s / %8s / %11s / " \
        % (x_specie,x_filename,x_category,x_status))
      if x_delta is not None:
        info_file.write("%6.3f / " % x_delta)
      else:
        info_file.write("       / ")
      if x_delta1 is not None:
        info_file.write("%6.3f /" % x_delta1)
      else:
        info_file.write("       /")
      for cm in x_comment:
        if len(cm.strip())>0:
          info_file.write(" "+cm.strip()+ " /")
      info_file.write("\n")

# Close info_file
  info_file.close()

  return None

#--------------------------------------------------------------------------------
# MAIN PROGRAM

def usage():
  print ('Usage: '+sys.argv[0].split('/')[-1] \
  +'\n  [--help]' \
  +'\n' \
  +'\n  [--action <action>] (default: none)  Possible actions:' \
  +'\n       create_github_from_table, create_html_from_github,' \
  +'\n       create_html_from_table, create_inputs_from_table' \
  +'\n' \
  +'\n  [--root <root_folder>] (default: current folder, can be table_folder)' \
  +'\n  [--dest <dest_folder>] (default: none, can be github_folder or html_folder or inputs_folder)' \
  +'\n' \
  +'\n  [--erase-dest] (default: no. Erase destination folder [be careful])' \
  +'\n  [--with-subdirs] (default: no. Valid only if action = create_html_from_github)' \
  +'\n                    If yes, creates ATOMICADATA/xxx-yy/index.html files.' \
  +'\n                    If no,  creates ATOMICDATA/xxx-yyy.html files.' \
  +'\n  [--add-corewf] (default: no. Valid only if action = create_inputs_from_table)' \
  +'\n                    If yes, add printing of core WF in Atompaw XML input files.' \
  +'\n' \
  +'\nGlossary:' \
  +'\ntable_folder : source folder as written by F. Jollet' \
  +'\ngithub_folder: destination folder as present in pseudo-dojo github' \
  +'\nhtml_folder  : destination folder to be uploaded to abinit web site' \
  +'\ninputs_folder : destination folder containing all input files')

if __name__ == "__main__":
  root = os.getcwd()
  dest = None
  action = None
  erase_dest = False
  with_subdirs = False
  add_corewf = False
  for i in range(len(sys.argv)):
    if sys.argv[i]=="--help":
      usage() ; sys.exit()
    elif sys.argv[i]=="--root":
      if len(sys.argv)<i+2:
        print("Option 'root' needs an argument!");sys.exit()
      else:
        root=sys.argv[i+1]
    elif sys.argv[i]=="--dest":
      if len(sys.argv)<i+2:
        print("Option 'dest' needs an argument!");sys.exit()
      else:
        dest=sys.argv[i+1]
    elif sys.argv[i]=="--action":
      if len(sys.argv)<i+2:
        print("Option 'action' needs an argument!");sys.exit()
      else:
        action=sys.argv[i+1]
    elif sys.argv[i]=="--erase-dest":
      erase_dest = True
    elif sys.argv[i]=="--with-subdirs":
      with_subdirs = True
    elif sys.argv[i]=="--add-corewf":
      add_corewf = True

  if root is not None:
    if not isdir_case_sensitive(root):
      print("Root directory does not exist!")
      print("root="+root);sys.exit()    
  if dest is not None:
  #  if not isdir_case_sensitive(dest):
  #    print("Dest directory does not exist!")
  #    print("dest="+dest);sys.exit()    
    if erase_dest and isdir_case_sensitive(dest):
      if exists_case_sensitive(dest): shutil.rmtree(dest,ignore_errors=True)

  if action =="create_github_from_table":
    if dest is None:
      main_create_github_from_table(root)
    else:
      main_create_github_from_table(root,github_folder=dest)    
  elif action =="create_html_from_table":
    if dest is None:
      print("Action 'create_html_from_table' needs a 'dest' argument!");sys.exit()    
    main_create_html_from_table(root,dest)    
  elif action =="create_inputs_from_table":
    if dest is None:
      print("Action 'create_inputs_from_table' needs a 'dest' argument!");sys.exit()    
    main_create_inputs_from_table(root,dest,add_corewf=add_corewf)    
  elif action =="create_html_from_github":
    if dest is None:
      print("Action 'create_html_from_github' needs a 'dest' argument!");sys.exit()    
    main_create_html_from_github(dest,github_table_folder=root,with_subdirs=with_subdirs)
  elif action is None:
    print("Need a 'action' argument!")
    sys.exit()
  else:
    print("Wrong 'action' argument!")
    sys.exit()
