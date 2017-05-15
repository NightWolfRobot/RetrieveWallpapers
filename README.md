# Retrieve lockscreen Windows wallpapers

Windows store on your computer the wallpapers of your lockscreen in a weird way. This script will help you to retrieve them easily.

### Python
This script has been tested on `python 3.5.3`. No add-ons needed.

### Exemples of use

```sh 
$ python User
```
This line will only copy raw files from the Windows location to the new one (`Wallpapers`) and add them their extension.
You may have several useless elements in your Wallpapers repository.

```sh
$ python retrieveWallpapers.py User -vrcd MyDestinationFolder
```
In this line we use all the options. 
- The verbose mode is activated so we will see on the output all the logs. 
- We will also rename the files by the pattern `wallpaper_XX.png`.
- We will clean the repository (delete all files < 100ko and those who have a width < height)
- We choose the destination folder, here `MyDestinationFolder`


### Positional argument
The user_name is needed to complete the link where the wallpapers are.
`C:\Users\USER_NAME\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets`

| Option | Description |
| ------ | ------ |
| user_name | Enter the name of your Windows user |

### Optional arguments

Be carefull when you use those options, if you already have a directory with the name of the destination folder and you chose to clean out the repository, you may delete more than you want, meaning more than only the new wallpapers.

| Option | Description |
| ------ | ------ |
| -h, --help | Print help on the output |
| -v, --verbose | Display each action from the script `(Logging.DEBUG) `|
| -r, --rename | Rename copied files by the pattern `wallpaper_XX.png` |
| -c, --clean | Clean repository. BE CAREFULL ! It will also wipe out every file under 100ko |
| -d, --dst | Destination name of folder, by default it is set to `Wallpapers` |


### Licence

This script is Free to use, modify and everything, do what you want with it. Hope you'll enjoy.

