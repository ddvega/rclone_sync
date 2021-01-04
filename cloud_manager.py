import os
from decouple import config
from utils import *


class CloudManager():
    def __init__(self, cloud_remote) -> None:
        self.cloud_remote = cloud_remote
        self.local_path = self.set_local_path()
        self.create_main_folder()
        self.local_dirs = {}
        self.cloud_dirs = {}
        self.cloud_dirs_sizes = {}
        self.local_dirs_sizes = {}
        self.set_local_dirs()
        self.set_cloud_dirs()

    def set_cloud_dirs(self):
        """
        Requests a list of all directories from cloud and stores them in the 
        class variable self.all_cloud_dirs for later use.
        """
        self.cloud_dirs = {}
        a = os.popen(f"rclone lsd {self.cloud_remote}:").readlines()
        for i in range(len(a)):
            self.cloud_dirs[i] = a[i].split(' ')[-1].strip('\n')

    def set_local_path(self):
        home = os.path.expanduser("~")
        return f'{home}/{self.cloud_remote}'

    def set_local_dirs(self):
        self.local_dirs = {}
        l_dirs = os.listdir(self.local_path)
        for i in range(len(l_dirs)):
            self.local_dirs[i] = l_dirs[i]

    def set_cloud_dirs_sizes(self):
        """
        create a json object with directory name as key and size of directory as
        the value. Directory data will come from cloud folder using rclone.
        """
        self.cloud_dirs_sizes = {}
        print("Fetching directory sizes from cloud...")
        for k, v in self.local_dirs.items():
            os.system(f"rclone mkdir {self.cloud_remote}:/{v}")
            a = os.popen(f"rclone size {self.cloud_remote}:/{v}").readlines()

            dir_size = get_val_from_rclone_str(a[1])

            self.cloud_dirs_sizes[v] = dir_size

    def set_local_dirs_sizes(self) -> object:
        """
        create a json object with directory name as key and size of directory as
        the value. Directory data will come from local directories.
        """
        self.local_dirs_sizes = {}
        for k, v in self.local_dirs.items():
            dir_size = get_local_dir_size(f'{self.local_path}/{v}')
            #print(f'Local Directory: {i}  Size: {dir_size}')
            self.local_dirs_sizes[v] = dir_size

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

    def safety_check(self, action):
        """
        Checks if there's a difference between the size of a local and cloud 
        directory. Asks user to verify if they want to proceed.
        """
        for k, v in self.local_dirs_sizes.items():
            # cloud has more data, a push from local will delete it
            if self.cloud_dirs_sizes[k] > v and action == "push":
                diff = self.cloud_dirs_sizes[k]-v
                msg = f'{diff} bytes will be DELETED from {k} in cloud.'
                kill_switch(msg)

            # local has more data, a pull from cloud will delete it
            if v > self.cloud_dirs_sizes[k] and action == "pull":
                diff = v-self.cloud_dirs_sizes[k]
                msg = f'{diff} bytes will be DELETED from {k} on local machine.'
                kill_switch(msg)

    def push_to_cloud(self):
        """
        Syncs data from local to cloud.
        """
        self.set_cloud_dirs_sizes()
        self.set_local_dirs_sizes()
        self.safety_check('push')

        for k, v in self.local_dirs.items():
            os.system(f"rclone mkdir {self.cloud_remote}:/{v}")
            os.system(
                f"rclone sync {self.local_path}/{v} {self.cloud_remote}:/{v} -P")

    def pull_from_cloud(self):
        """
        Syncs data from cloud to local.
        """
        self.set_cloud_dirs_sizes()
        self.set_local_dirs_sizes()
        self.safety_check('pull')
        for k, v in self.local_dirs.items():
            os.system(
                f"rclone sync {self.cloud_remote}:/{v} {self.local_path}/{v} -P")

    def purge_cloud_dir(self):
        """
        Removes a directory from the cloud. Certain folders are off limits.
        """

        for k, v in self.cloud_dirs.items():
            print(f'[{k}] - {v}')
        msg = "Please Select a directory to DELETE."
        a = valid_input(msg, len(self.cloud_dirs))
        if a == -1:
            return

        if self.cloud_dirs[a] not in config('OFF_LIMITS'):
            msg = f"You are about to purge {self.cloud_dirs[a]}"
            kill_switch(msg)
            os.system(
                f"rclone purge {self.cloud_remote}:/{self.cloud_dirs[a]}")
        else:
            print(f"{self.cloud_dirs[a]} is off limits!")

    def purge_local_dir(self):
        for k, v in self.local_dirs.items():
            print(f'[{k}] - {v}')
        msg = "Please Select a directory to DELETE."
        a = valid_input(msg, len(self.local_dirs))
        if a == -1:
            return

        print(self.local_dirs[a])
        msg = f'You are about to purge {self.local_dirs[a]}'
        kill_switch(msg)
        os.system(f"rm -rf {self.local_dirs[a]}")

    def copy_cloud_dir(self):
        """
        Checks if cloud folder already exists in local folder.  If it doesn't,
        it creates it and then syncs the data from cloud to local.
        """
        msg = "Please Select a directory to COPY."
        for k, v in self.cloud_dirs.items():
            print(f'[{k}] - {v}')

        a = valid_input(msg, len(self.cloud_dirs))
        if a == -1:
            return

        if not os.path.exists(f'{self.local_path}/{self.cloud_dirs[a]}'):
            os.mkdir(f'{self.local_path}/{self.cloud_dirs[a]}')
            self.set_local_dirs()

        self.pull_from_cloud()

    def print_all_cloud_dir(self):
        """
        Prints cloud directories.
        """
        # self.set_local_dirs()
        for k, v in self.cloud_dirs.items():
            print(f'[{k}] - {v}')

    def print_local_dirs(self):
        """
        Reads the directories in the local folder and prints them.
        """
        # self.set_local_dirs()
        for k, v in self.local_dirs.items():
            print(f'[{k}] - {v}')
