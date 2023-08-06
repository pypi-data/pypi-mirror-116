# Algo Tides

### Description
This Python application is a graphic interface for the user who owns or have access to an Algorand
node and would like to issue operations through a GUI rather than CLI. (i.e.: manage wallets and addresses,
send transactions, save a contact list)

### Disclaimer
Clone this repo only if you want to develop. If you are just a user please download the python package following
instructions below.  
This repo is not guaranteed to work between commits.

### Installation
`$ pip install algotides` or you can download the `.tar.gz` package and install it that way.

Users shouldn't download from this repo because it is not guaranteed to work between commits.  
Better to install via `pip`

### Security
Please keep in mind that this software stores some serialized data inside `<HOME_FOLDER>/.algo-tides`.  
As a result of this any user should put over this folder permissions that are stricter than usual.  
It is possible to inject arbitrary code when deserializing `jsonpickle` files so please be mindful.

### Donations
Please consider donating ALGO to this project at the following address:  
`TIDESVS3UR7WQTR5J3M5ADEJVOUUS2C2YOEIU4Z6VTPU2EMQME7PSDK76A`

Any donation will be used to fund the development and maintenance of Algo Tides.  

*Algo Tides will always remain a free and open source app. Donations are on a voluntary basis.*

### Requirements
* Python 3.7

Packages:
- PySide2
- py-algorand-sdk
- jsonpickle
- qasync
- aioify

### Troubleshoot
* #### qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
    This step creates a symlink from the existing library to the needed library:


    on MXLinux 19.4:

    sudo ln -s /usr/lib/x86_64-linux-gnu/libxcb-util.so.0.0.0 /usr/lib/x86_64-linux-gnu/libxcb-util.so.1
  

    on Debian 10:
  
    sudo ln -s /usr/lib/x86_64-linux-gnu/libxcb-util.so /usr/lib/x86_64-linux-gnu/libxcb-util.so.1