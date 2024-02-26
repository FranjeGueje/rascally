# RASCALLY
![Rascally](https://raw.githubusercontent.com/FranjeGueje/rascally/master/grid/grid_h.jpeg)

A light and fast client to add games to SteamOS from official Launchers.
A perfect program to add to SteamOS Gamemode and use it to add your games from official launchers like Epic Game Launcher, Ubisoft Connect and any game with desktop shortcut.

Rascally will not be for you if you are happy with your third party launcher (like Heroic, Bottles, ...) It will be for you if you use official launchers added to Steam and you would like to separate it into different "CompatData" to have different configurations.

![Rascally](https://raw.githubusercontent.com/FranjeGueje/rascally/master/doc/main.png)

## How does it work?
With an interface adapted to the touch screen, and with the possibility of scrolling with your finger, Rascally will search all your CompatData for games of the selected engine showing the images of these (if you entered your SteamGridDB key) and will allow you to add them in different ways. Once the game has been added, you must choose a Proton compatibility tool.

## Engines

Currently an engine is available for Epic Game Launcher, Ubisoft Connect and any software that has director access on the desktop.

![Epic](https://raw.githubusercontent.com/FranjeGueje/rascally/master/doc/Epic.png)
**Epic**

![Ubisoft](https://raw.githubusercontent.com/FranjeGueje/rascally/master/doc/Ubi.png)
**Ubisoft**

## Configuration

![Config](https://raw.githubusercontent.com/FranjeGueje/rascally/master/doc/config.png)
This is the **rascally** configuration. Each of them is listed below with a short description:
* Steam path : is the path of Steam. Necessary and very important. If it is not properly configured **rascally** will not work.
* SteamGridDB key: it is the key to log in SteamGridDB to download the images. You can get your key at https://www.steamgriddb.com/profile/preferences/api by logging in with your Steam account.
* Lnk Location: location where the links that will be used to start your games. That is, where Steam will point to start your game.
* Clonning mode: perhaps the most important parameter. **Rascally** will add the game and create a new compatdata for it, but you can choose how it will be created. The options are: __Symlink clone__ will create a symbolic link of the original compatdata, sSo its size is zero, but beware, the compatdata of this game, the launcher and all games launched through it share the same data. Be sure to choose the same Proton in all of them. So you SHOULD use the same compatibility tool to not damage the other games; __Full clone__ will copy the original compatdata for your new game, this will have the highest compatibility, you can choose any compatibility tool you want, BUT it will duplicate the disk space of that compatdata; __Balanced clone__ will be a mix of the two previous ones. .. some paths will be copied, some will be symbolic links and you can even use the Proton you want, so it will be the most balanced option. Your choice.
* Discard Repeat Games: games that the system detects that you already own will not be displayed.
* CompatData exceptions: it will be the compatdata that you don't want the engines to scan.

## Credits
I dedicate this program, as always, to my wife and children for their patience with my hobby not my job.

**Rascally** uses other python libraries:
* vdf: https://pypi.org/project/vdf/
* python-steamgriddb: https://pypi.org/project/python-steamgriddb/
* mslink: https://www.mamachine.org/mslink/
