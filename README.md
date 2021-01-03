# rclone_sync

This application a python application that uses rclone to interact with a remote database. Before using this application, please you make sure you do the following:
1. install rclone https://rclone.org/downloads/
2. add configuration for cloud_remote e.g https://rclone.org/pcloud/
   *instead of using `remote` name as shown in the tutorial, make sure you use e.g `pcloud` as the name.*


rclone_sync will look for directories in your local folder. E.G `/home/david/pcloud`

##### if you run the application without creating this folder, the application will create it for you and then exit. Once you have your local folder created, add directories to it.

e.g
```
/home/david/pcloud/Wallpapers
/home/david/pcloud/Pictures
```
*rclone_sync will use these directories to push to or pull from cloud*

##### Important Note
*make sure you only have directories in your main local folder `/home/david/pcloud`. Loose files will not sync and will instead create folders in your cloud with those names.*

###### If no directory exists in local folder

>nothing will sync

###### If directory exists in your local folder but not in your remote cloud folder

> directory and it's contents will be added to your remote cloud folder

###### If directory exists in both your local folder and in your remote cloud folder

>contents will be synced either to your remote cloud or from your remote cloud

##### Please be careful when you are pushing to or pulling from your cloud.

Certain safety features have been put in place but if you ignore them, you run the risk of losing your data.

##### To push to the cloud run the following:
    python3 rclone.py [name of cloud remote] push


##### To pull from the cloud, run the following:
    python3 rclone.py [name of cloud remote] pull