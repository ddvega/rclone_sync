import os
import sys
from typing import List
from maintenance_class import CloudManager

cm = CloudManager(sys.argv[1])

menu = "\nPlease Select from the following options:\n" \
    "[1] List Cloud Directories\n" \
    "[2] List Local Directories\n" \
    "[3] Push local to cloud\n" \
    "[4] Pull cloud to local\n" \
    "[5] Purge Directory\n" \
    "[6] Get Cloud info\n" \
    "[7] Copy cloud dir to local\n" \
    "[8] Quit"


while True:
    cm.set_all_cloud_dirs()
    ans = input(f"{menu}\n-> ")
    os.system("clear")
    if ans == '1':
        cm.print_all_cloud_dir()
    if ans == '2':
        cm.print_local_dirs()
    if ans == '3':
        cm.push_to_cloud()
    if ans == '4':
        cm.pull_from_cloud()
    if ans == '5':
        cm.purge_dir_from_cloud()
    if ans == '7':
        cm.copy_cloud_dir()

    if ans == '8':
        break

sys.exit()
