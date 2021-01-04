import os
import sys
from cloud_functions import *


class CloudManager():
    def __init__(self, cloud_remote) -> None:
        self.cloud_remote = cloud_remote
        self.all_cloud_dirs = {}
        self.local_path = self.set_local_dir()
        self.create_main_folder()
        self.local_path_dirs = []
        self.cloud_data_sizes = {}
        self.local_data_sizes = {}
        self.set_local_path_dirs()

    def set_cloud_dirs(self):
        a = os.popen(f"rclone lsd {self.cloud_remote}:").readlines()
        for i in range(len(a)):
            self.all_cloud_dirs[i] = a[i].split(' ')[-1].strip('\n')

    def set_local_dir(self):
        home = os.path.expanduser("~")
        return f'{home}/{self.cloud_remote}'

    def create_main_folder(self):
        if not os.path.exists(self.local_path):
            print(
                "Looks like this is your first time using this application.\n" +
                f"A folder called {self.cloud_remote} has been added to your home\n" +
                "directory.\nAny directory in this folder, will get synced with " +
                f"your cloud service. \nPlease add directories to {self.cloud_remote} " +
                "and re-run application."
            )
            os.mkdir(self.local_path)

    def set_local_path_dirs(self):
        self.local_path_dirs = os.listdir(self.local_path)
    
    def set_cloud_dirs_sizes(self):
        """
        create a json object with directory name as key and size of directory as
        the value. Directory data will come from cloud folder using rclone.
        """
        self.cloud_data_sizes = {}
        print("Fetching directory sizes from cloud...")
        for i in self.local_path_dirs:
            os.system(f"rclone mkdir {self.cloud_remote}:/{i}")
            a = os.popen(f"rclone size {self.cloud_remote}:/{i}").readlines()
            dir_size = get_val_from_rclone_str(a[1])
            #print(f'Cloud Directory: {i}  Size: {dir_size}')
            self.cloud_data_sizes[i] = dir_size

    def set_local_dirs_sizes(self) -> object:
        """
        create a json object with directory name as key and size of directory as
        the value. Directory data will come from local directories.
        """
        self.local_data_sizes = {}
        for i in self.local_path_dirs:
            dir_size = get_local_dir_size(f'{self.local_path}/{i}')
            #print(f'Local Directory: {i}  Size: {dir_size}')
            self.local_data_sizes[i] = dir_size

    def safety_check(self, action):
        for k, v in self.local_data_sizes.items():
            # cloud has more data, a push from local will delete it
            if self.cloud_data_sizes[k] > v and action == "push":
                diff = self.cloud_data_sizes[k]-v
                print(f'{diff} bytes will be DELETED from {k} in cloud.')
                abort_or_continue()

            # local has more data, a pull from cloud will delete it
            if v > self.cloud_data_sizes[k] and action == "pull":
                diff = v-self.cloud_data_sizes[k]
                print(f'{diff} bytes will be DELETED from {k} on local machine.')
                abort_or_continue()

    def push_to_cloud(self):
        self.set_cloud_dirs_sizes()
        self.set_local_dirs_sizes()
        self.safety_check('push')
        for i in self.local_path_dirs:
            os.system(
                f"rclone sync {self.local_path}/{i} {self.cloud_remote}:/{i} -P")

    def pull_from_cloud(self):
        self.set_cloud_dirs_sizes()
        self.set_local_dirs_sizes()
        self.safety_check('pull')
        for i in self.local_path_dirs:
            os.system(
                f"rclone sync {self.cloud_remote}:/{i} {self.local_path}/{i} -P")

    def print_all_cloud_dir(self):
        for k, v in self.all_cloud_dirs.items():
            print(f'[{k}] - {v}')

    def purge_dir_from_cloud(self):
        off_limits = [".Trash-1000", ".lock", ".resource", ".sync", "apps"]

        print("Please Select a directory to delete.")
        for k, v in self.all_cloud_dirs.items():
            print(f'[{k}] - {v}')
        a = int(input("->"))

        if self.all_cloud_dirs[a] not in off_limits:
            print(f"You are about to purge {self.all_cloud_dirs[a]}")
            abort_or_continue()
            os.system(
                f"rclone purge {self.cloud_remote}:/{self.all_cloud_dirs[a]}")
        else:
            print(f"You are not permitted to purge {self.all_cloud_dirs[a]}")

    def set_all_cloud_dirs(self):
        self.all_cloud_dirs = {}
        a = os.popen(f"rclone lsd {self.cloud_remote}:").readlines()
        for i in range(len(a)):
            self.all_cloud_dirs[i] = a[i].split(' ')[-1].strip('\n')

    def copy_cloud_dir(self):
        print("Please Select a directory to copy.")
        for k, v in self.all_cloud_dirs.items():
            print(f'[{k}] - {v}')
        a = int(input("->"))

        if not os.path.exists(f'{self.local_path}/{self.all_cloud_dirs[a]}'):
            os.mkdir(f'{self.local_path}/{self.all_cloud_dirs[a]}')
            self.set_local_path_dirs()

        self.pull_from_cloud()

    def print_local_dirs(self):
        self.set_local_path_dirs()
        for i in range(len(self.local_path_dirs)):
            print(f'[{i}] - {self.local_path_dirs[i]}')
