# Usage
Get this repository by:
```sh
git clone https://github.com/zKurisu/FYP-Codes.git
```

# Environment setup
## VM
Using virtual machine template supplied by P4Tutorial:
```sh
mkdir p4-dev
git clone https://github.com/p4lang/tutorials.git
cd tutorials/vm-ubuntu-24.04
git checkout 03501da
vagrant up dev --provider=virtualbox
```
It will take some time (maybe one hour...) to download packages and compile to executable files. Pay attention to the specific version, latest version may meet some problems.

You may get `ssh error`, which can be ignored. Then login to GUI, you could reboot or `startx`.

## Ryu
Using Python venv to separate:
```sh
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8 python3.8-venv
python3.8 -m venv ryu
source ryu/bin/activate
pip install --upgrade pip
pip install ryu
pip uninstall eventlet
pip install eventlet==0.30.0
ryu-manager --version
```

Run example application to verify Ryu:
```
git clone https://github.com/faucetsdn/ryu.git
ryu-manager ./ryu/ryu/app/simple_switch.py
```

## Mininet-wifi
```sh
git clone https://github.com/intrig-unicamp/mininet-wifi
cd mininet-wifi
sudo util/install.sh -WlnfvP6
sudo make install
```

# Start Project
Install requirements for other components (except Ryu venv):
```sh
cd FYP-Codes
pip install -r requirements-main.txt
```

For Ryu venv:
```sh
source ryu/bin/activate
cd FYP-Codes
pip install -r requirements-ryu.txt
```

Open several terminal to run separately.

For frontend page:
```sh
make Mrest
```

For Prometheus:
```sh
make Mprom
```

For Ryu controller:
```sh
make Mryu
```

For mininet-wifi:
```sh
make run
```




