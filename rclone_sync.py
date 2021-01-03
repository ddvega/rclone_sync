import os
import sys
from typing import List


def get_val_from_rclone_str(s: str) -> int:
    """
    capture size value(bytes) from string returned from rclone
    """
    s = s.split('(')[1].split(')')[0]
    return int(s.split(' ')[0])


def cloud_dirs_sizes_obj(dirs: List, cloud_remote) -> object:
    """
    create a json object with directory name as key and size of directory as
    the value. Directory data will come from cloud folder using rclone.
    """
    data = {}
    for i in dirs:
        os.system(f"rclone mkdir {cloud_remote}:/{i}")
        a = os.popen(f"rclone size {cloud_remote}:/{i}").readlines()

        data[i] = get_val_from_rclone_str(a[1])
    return data


def get_local_dir_size(path: str) -> int:
    """
    return sum of the sizes of every directory and file within a directory
    https://www.codespeedy.com/get-the-size-of-a-folder-in-python/
    """
    # initialize the size
    total_size = 0

    # use the walk() method to navigate through directory tree
    for dirpath, dirnames, filenames in os.walk(path):
        for i in filenames:

            # use join to concatenate all the components of path
            f = os.path.join(dirpath, i)

            # use getsize to generate size in bytes and add it to the total size
            total_size += os.path.getsize(f)
    return total_size


def local_dirs_sizes_obj(dirs: List, dname: str) -> object:
    """
    create a json object with directory name as key and size of directory as
    the value. Directory data will come from local directories.
    """
    data = {}
    for i in dirs:
        data[i] = get_local_dir_size(f'{dname}/{i}')
    return data


def get_local_dirs(dirname) -> List:
    """
    return all of the directorys in local cloud_remote folder. These will be 
    the directories that get synced with cloud
    """
    return os.listdir(dirname)


###############################################################################
# main
###############################################################################
# name of the cloud remote service to use
cloud_remote = sys.argv[1]

# push to or pull from cloud are the options
# push or pull
action = sys.argv[2]

# get users home directory
home = os.path.expanduser("~")

# local cloud_remote directory
dname = f'{home}/{cloud_remote}'

if not os.path.exists(dname):
    print(
        "Looks like this is your first time using this application.\n" +
        "A folder called cloud_remote has been added to your home directory.\n" +
        "Any directory in this folder, will get synced with your cloud_remote.\n" +
        "Please add directories to cloud_remote folder and re-run application."
    )
    os.mkdir(dname)
    sys.exit()

# get names of all of the directories in local cloud_remote directory
local_dirs = get_local_dirs(dname)

# create object with sizes of directories in cloud
cloud_data_sizes = cloud_dirs_sizes_obj(local_dirs, cloud_remote)

# create object with sizes of directories on local machine
local_data_sizes = local_dirs_sizes_obj(local_dirs, dname)

# safety against overwriting data
for k, v in local_data_sizes.items():
    # cloud has more data, a push from local will delete it
    if cloud_data_sizes[k] > v and action == "push":
        diff = cloud_data_sizes[k]-v
        print(f'{diff} bytes will be DELETED from {k} in cloud.')
        a = input("ENTER [c] to Continue or [any key] to Abort: ").lower()
        if a != 'c':
            sys.exit()
    # local has more data, a pull from cloud will delete it
    if v > cloud_data_sizes[k] and action == "pull":
        diff = v-cloud_data_sizes[k]
        print(f'{diff} bytes will be DELETED from {k} on local machine.')
        a = input("ENTER [c] to Continue or [any key]to Abort: ").lower()
        if a != 'c':
            sys.exit()

# sync local machine with plcoud
for i in local_dirs:
    if action == "push":
        os.system(f"rclone sync {dname}/{i} {cloud_remote}:/{i} -P")
    elif action == "pull":
        os.system(f"rclone sync {cloud_remote}:/{i} {dname}/{i} -P")


sys.exit(0)
