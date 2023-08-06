# python-pulseaudio-profiles-trayicon
Python library that adds a tray icon for easily changing and creating pulseaudio profiles.

Uses the [python-pulseaudio-profiles](https://github.com/fracpete/python-pulseaudio-profiles) 
library under the hood.

You can start the tray icon with `ppp-tray`.

## Installation

Make sure you have the following dependencies installed:

```commandline
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 
```

On Ubuntu 18.04 and older: 

```commandline
sudo apt install gir1.2-appindicator3 
```

On Ubuntu 20.04 and newer:

```commandline
sudo apt install gir1.2-ayatanaappindicator3-0.1
```

You can install the tool as follows:

```
pip install python-pulseaudio-profiles-trayicon
```

Or, when running Debian/Ubuntu, download and install the Debian package from the 
[Releases section](https://github.com/fracpete/python-pulseaudio-profiles-trayicon/releases).


### Usage

Once the application started up and you see the tray icon (a speaker with *PA* next to it), you can 
right-click and choose from the following actions:

* **Create** - allows you to store the current pulseaudio setup under a profile name or your choosing 
* **Apply** - sub-menu for applying profiles
* **Delete** - sub-menu for deleting profiles 
* **Refresh** - refreshes the menu, e.g., when you created or deleted profiles manually through the commandline
* **Exit** - exits the tray icon
