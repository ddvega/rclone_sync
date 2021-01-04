import os
import sys
from typing import List
from cloud_manager import CloudManager
from utils import valid_input

cm = CloudManager(sys.argv[1])

try:
    if len(sys.argv[2]) > 1:
        if sys.argv[2] == "push":
            cm.push_to_cloud()
        elif sys.argv[2] == "pull":
            cm.pull_from_cloud()
        sys.exit()
except IndexError:
    pass

menu = "\nPlease Select from the following options:\n" \
    "[0] List Cloud Directories\n" \
    "[1] List Local Directories\n" \
    "[2] Push local to cloud\n" \
    "[3] Pull cloud to local\n" \
    "[4] DELETE Cloud Directory\n" \
    "[5] DELETE Local Directory\n" \
    "[6] Copy cloud dir to local\n"

switch = {
    
    0: cm.print_all_cloud_dir,
    1: cm.print_local_dirs,
    2: cm.push_to_cloud,
    3: cm.pull_from_cloud,
    4: cm.purge_cloud_dir,
    5: cm.purge_local_dir,
    6: cm.copy_cloud_dir,
    -1: sys.exit,
}

while True:
    cm.set_cloud_dirs()
    cm.set_local_dirs()
    ans = valid_input(f"{menu}", len(switch))
    os.system("clear")
    switch[ans]()
