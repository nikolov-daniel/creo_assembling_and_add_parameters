print("\n Assemble and change parameters for revision\n")
print("Made by Daniel Nikolov")

print("""
-----------------------------------------------------------------------
                    Read me
This program is used for adding parameters
in each part or assembly
add what is changed in revision changed parameter 
add todays date in revision date parameter
add user in revision user parameter
assembling parts or assemblies in temporary assembly
for easier replacing components usefull for assemblies
opens all existing drawings pauses to edit them and saves 

You must have started CREO and active workspace on windchill,
It's recomended to have clean workspace 
      
                    IMPORTANT 
      In case of emergency stop press CTRL + C
                or CTRL + C + ENTER
                    IMPORTANT 
-----------------------------------------------------------------------
""")

import os
from datetime import datetime, timedelta
from pathlib import Path
import creopyson
from functools import reduce  # Python 3 compatibility
import time
import json
import sys
import getpass


user_default = getpass.getuser()
user = user_default.lower()
if user == "daniel" or "nikolov":
    user_fullname = "Daniel Nikolov"
else:
    user_fullname = input("Enter your full name (e.g. Darth Vader): ")

#json works fine for implementation somewhere else!!
#json_file = open(f"C:\\Users\\{user_default}\\Documents\\assemble_parameters_json\\parameters.json", "r")
#json_data =json_file.read()
#obj=json.loads(json_data)

parameter_date = "D__REV__"    #obj["parameter_user"]       #input("Enter parameter date with '__REV__' insteed actual revision (e.g. DATUM_WIJZ__REV__): ")
parameter_user = "O__REV__"   #obj["parameter_date"]       #input("Enter parameter user with '__REV__' insteed actual revision (e.g. ONTWERPER__REV__): ")
parameter_changed ="W__REV__" #obj["parameter_changed"]    #input("Enter parameter for changed with '__REV__' insteed actual revision (e.g. CHANGED__REV__): ")
##


yes = ["yes","YES", "Y", "y", "", " "]
no = ["no", "NO", "N", "n"]
part = ["p","P"]
assembly = ["a","A"]

#starting creoson

creoson_path = Path(f"C:\\Users\\{user}\\Desktop\\creoson")
os.chdir(creoson_path)
run_path = Path(creoson_path) / "creoson_run.bat"
os.startfile(run_path.resolve().as_posix())
print("Creoson starting!")
c = creopyson.Client()
c.connect()

#definiranje funkcija dali e startuvan creo
def creo_run():
    while c.is_creo_running()==False:
        print("""
    --------------------
    Creo is not running
    Please start Creo!
    --------------------""")
        time.sleep(10)
    else:
        print("Creo is running!")

creo_run()

#login

def login_windchill():

    if user == "user":
        password = "password"
    elif user == "user2":
        password = "password2"
    #protected
    else:
        print("username:", user)
        password = input("Enter your password: ")
        try:
            c.windchill_authorize(user, password)
        except Exception as e:
            print(e)
            print("wrong password")
            raise
        user_fullname= input()
    c.windchill_authorize(user, password)
    print("login successful")
print
login_windchill()
#UNcomment later
#user_fullname = "Daniel Nikolov"

####################################################################################################
#TODO  UNBLOCK login_windchill WHEN MAKING EXE

creo_set_creo_version = 8
#PROTECTED!
today = datetime.now()
todays_date = datetime.today().strftime('%Y-%m-%d')
feature = datetime(2024,2,28)
while today > feature:
    print("Lost licence, please reconfigure.")
    time.sleep(100)
    c.kill_creo()
    c.disconnect()
#PROTECTED!

#TODO ADD ACTUAL PARAMETERS SO WONT BE NEEDED AS INPUT
#parameter_date = input("Enter parameter date with '__REV__' insteed actual revision (e.g. DATUM_WIJZ__REV__): ")
#parameter_user = input("Enter parameter user with '__REV__' insteed actual revision (e.g. ONTWERPER__REV__): ")
#parameter_changed = input("Enter parameter for changed with '__REV__' insteed actual revision (e.g. CHANGED__REV__): ")
temp_asm = "temporary_asm" #input("Enter the name of the assembly you need to place parts or assemblies: ")
what_is_changed = input("Enter what is changed (e.g. PK XXXXXX: yyyyyyy is replaced with zzzzzz): ")
# working directory
current_directory = c.creo_pwd() #  return current working directory.


#TODO uncomment and comment temp variable path_to_list_txt
path_to_list_txt = input("insert only path to txt file of the list of files: ")
#path_to_list_txt = r"C:\Users\daniel\Desktop\ASSEMBLY_PROGRAM\s"
files = []
i=0
#read all txt files in dir
for file in os.listdir(path_to_list_txt):
    if file.endswith(".txt"):
        files.append(file)
        print(f"[{i}] - {file}")
        i=i+1
if len(files) > 1:
    i= int(input("Enter order number for choosing file: "))
else:
    i = 0
txt_file = files[i]
print(f"chosen file: {txt_file}" )
pateka_txt_files = f"{path_to_list_txt}\{txt_file}"

#############################################################################################################
#TODO not sure if needed!!!
workspace = c.windchill_get_workspace()
#list_of_drawings = c.windchill_list_workspace_files(workspace, "*.drw")

#read list
raw_list_numbers = open(pateka_txt_files).read().splitlines()
#remove spaces and tab from empty str
raw_list_numbers = [elem for elem in raw_list_numbers if elem.strip()]
#remove spaces and tabs from not empty str
raw_list_numbers = [x.strip(' ') for x in raw_list_numbers]
#remove empty  
raw_list_numbers = [x for x in raw_list_numbers if x]



list_numbers_asm = [sub + ".asm" for sub in raw_list_numbers]
list_numbers_prt = [sub + ".prt" for sub in raw_list_numbers]
list_numbers_drw = [sub + ".drw" for sub in raw_list_numbers]

assemble_part_or_assembly = input("Enter P for collecting part or A for assembly: ")
while True:
    if assemble_part_or_assembly in assembly:
        list_numbers_assemble =list_numbers_asm
        #print(assemble_part_or_assembly)
        break
    elif assemble_part_or_assembly in part:
        list_numbers_assemble =list_numbers_prt
        #print(assemble_part_or_assembly)
        break
    else:
        while assemble_part_or_assembly not in assembly+part:
            assemble_part_or_assembly = input("Enter P for part or A for assembly: ")

do_assemble = input("Enter Y if you need to assemble all parts or asm in one assembly or N do not assemble: ")



add_parameters = input("Enter Y if you need to add parameters for date, version, and user or N do not add parameters: ")
if add_parameters in yes:

    for file in list_numbers_assemble:
        file_name = list(file.rsplit(".", maxsplit=1))
        file_name = file_name[0]
        try:
            c.file_open(file, display=True)

            parametar_revision_raw = c.parameter_list(file_=file, name="PTC_WM_REVISION")
            revision = reduce(lambda a, b: dict(a, **b), parametar_revision_raw)
            revision = (revision["value"])
            #revision = "A"
            #print(f"file: {file}, revision: {revision}")
            add_parameter_date = parameter_date.replace("__REV__", revision)
            try:
                c.parameter_set(name=add_parameter_date, value =todays_date)
            except Exception as e:
                print(e)
            add_parameter_user = parameter_user.replace("__REV__", revision)
            try:
                c.parameter_set(name=add_parameter_user, value =user_fullname)
            except Exception as e:
                print(e)
            add_parameter_changed = parameter_changed.replace("__REV__", revision)
            try:
                c.parameter_set(name=add_parameter_changed, value =what_is_changed)
            except Exception as e:
                print(e)

            c.file_save()
            c.file_close_window(file)


        except Exception as e:
            print(e)
elif add_parameters in no:
    print("chose do not add parameters")


if do_assemble in yes:
    temp_asm_exist = c.file_exists(f"{temp_asm}.asm")

    try:
        c.file_open(file_=f"{temp_asm}.asm", display=True)
    except Exception as e:
        print(e)
        mapkey_make_temp_asm=f"""mapkey _mapkey_make_new_asm @MAPKEY_NAMEmake new assembly;\
@MAPKEY_LABELmake new assembly;~ Select `main_dlg_cur` `appl_casc`;\
~ Close `main_dlg_cur` `appl_casc`;~ Command `ProCmdModelNew` ;\
~ Select `new` `Type` 1 `Assembly`;~ Input `new` `InputPanel1` `{temp_asm}`;\
~ Input `new` `InputPanel1` `{temp_asm}`;~ Input `new` `InputPanel1` `{temp_asm}`;\
~ Update `new` `InputPanel1` `{temp_asm}`;~ Activate `new` `OK`;\
~ FocusOut `new_file_opts` `inp_template_name`;\
~ Activate `new_file_opts` `chk_create_drawing` 0;\
~ Activate `new_file_opts` `psh_ok`;~ Select `main_dlg_cur` `appl_casc`;\
~ Close `main_dlg_cur` `appl_casc`;~ Command `ProCmdModelSave` ;\
~ Activate `file_saveas` `OK`;
"""
        c.interface_mapkey(mapkey_make_temp_asm)
    for file in list_numbers_assemble:
        #works withouth placing to default
        #c.file_assemble(file_ = file, into_asm=temp_asm,assemble_to_root=False)
        try:
            mapkey_assemble = f"""
mapkey xxxx @MAPKEY_NAMEassemble to Automatic;@MAPKEY_LABELmapkey assemble;\
~Activate `main_dlg_cur` `page_Model_control_btn` 1;\
~Command `ProCmdCompAssem` ;\
~Trail `UI Desktop` `UI Desktop` `DLG_PREVIEW_POST` `file_open`;\
~Select `file_open` `Ph_list.Filelist` 1 `{file}`;\
~Input `file_open` `Inputname` `{file}`;\
~Update `file_open` `Inputname` `{file}`;\
~Select `open_rep` `replist` 1 `MASTER REP`;\
~Activate `open_rep` `replist` 1 `MASTER REP`;\
~Command `ProFileSelPushOpen_Standard@context_dlg_open_cmd` ;\
~Trigger `ScrLayout.3.0` `PH.L.S.l0.assem_ref_represent.l0.s0` `0`;\
~Trigger `ScrLayout.3.0` `PH.L.S.l0.assem_ref_represent.l0.s0` ``;\
~Trigger `ScrLayout.3.0` `PH.L.S.l0.comp_ref_represent.l0.s0` `0`;\
~Trigger `ScrLayout.3.0` `PH.L.S.l0.comp_ref_represent.l0.s0` ``;\
~Trigger `ScrLayout.3.0` `PH.L.S.l0.comp_ref_represent.l0.s0` `0`;\
~Trigger `ScrLayout.3.0` `PH.L.S.l0.comp_ref_represent.l0.s0` ``;\
~Open `ScrLayout.3.0` `PH.pop_constr_offset_type`;\
~Close `ScrLayout.3.0` `PH.pop_constr_offset_type`;\
~Open `ScrLayout.3.0` `PH.pop_constr_offset_type`;\
~Close `ScrLayout.3.0` `PH.pop_constr_offset_type`;\
~Select `ScrLayout.3.0` `PH.pop_constr_offset_type` 1 `Automatic`;\
~Open `ScrLayout.3.0` `PH.pop_constr_offset_type`;\
~Close `ScrLayout.3.0` `PH.pop_constr_offset_type`;\
~Activate `main_dlg_cur` `dashInst0.stdbtn_1`;
        """
            c.interface_mapkey(mapkey_assemble)
            print(f"{file}: assembled")
        except Exception as e:
            print(f"{file}: {e}")

    c.file_save()

input("""           Important!
this is intentional pause to find and replace parts in the assembly
when you are done press Enter to start opening the drawings: """)
print("\n when you are done with the drawing done press Enter\n")
for file in list_numbers_drw:
    try:
        c.file_open(file)
        c.drawing_regenerate(file)
        input(f"this is pause to prepare the drawing when done press enter {file} ")
        c.file_save(file)
        c.file_close_window(file)
    except Exception as e:
        print(f"{file}: {e}")
    #c.file_close_window(file)
        
input("finished, press Enter to close the program! ")
