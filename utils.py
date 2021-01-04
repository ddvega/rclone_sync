import os
import sys


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


def get_val_from_rclone_str(s: str) -> int:
    """
    capture size value(bytes) from string returned from rclone
    """

    s = s.split('(')[1].split(')')[0]
    return int(s.split(' ')[0])


def kill_switch(msg):
    """
    allows the user to close application to avoid loss of data.
    """
    print(msg)
    a = input("ENTER [c] to Continue or [any key] to Abort: ").lower()
    if a != 'c':
        sys.exit()


def valid_input(msg, limit):

    while True:
        print(f'\n{msg}')
        print("[e] - EXIT")
        a = input("-> ")

        if a.lower() == 'e':
            return -1

        if not a.isdigit():
            print("Please enter an integer.")

        elif 0 <= int(a) < limit:
            return int(a)
        else:
            print("Please enter a valid integer.")
