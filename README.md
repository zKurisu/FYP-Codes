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
git checkout 03501da
cd tutorials/vm-ubuntu-24.04
vagrant up dev --provider=virtualbox
```
It will take some time (maybe one hour...) to download packages and compile to executable files. Pay attention to the specific version, latest version may meet some problems.

You may get `ssh error`, which can be ignored. But make sure all scripts described in `Vagrantfile` have done, including `root-dev-bootstrap.sh`, `root-common-bootstrap.sh`, `user-dev-bootstrap.sh`, `user-common-bootstrap.sh` (some scripts should handle `pip install xxx --break-system-packages`). Then login to GUI, you could reboot or `startx`.

## Mininet-wifi
```sh
git clone https://github.com/intrig-unicamp/mininet-wifi
cd mininet-wifi
sudo util/install.sh -WlnfvP6
sudo pip3 install . --break-system-packages
sudo apt-get openvswitch-switch openvswitch-testcontroller openvswitch-common
sudo mn --wifi
```

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
cd FYP-Codes
pip install -r requirements-ryu.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
cp -r mygrpc ~/ryu/lib/python3.8/site-packages/
ryu-manager --version
```

Run example application to verify Ryu:
```sh
cd
git clone https://github.com/faucetsdn/ryu.git Ryu
ryu-manager ./Ryu/ryu/app/simple_switch.py
```

## Prometheus
Check the OS version and pull the latest bin file:
```sh
cd FYP-Codes/prometheus
wget https://github.com/prometheus/prometheus/releases/download/v3.2.1/prometheus-3.2.1.linux-386.tar.gz
tar xzf prometheus-3.2.1.linux-386.tar.gz
mv prometheus-3.2.1.linux-386.tar.gz ori
```


# Start Project
Install requirements for other components (except Ryu venv):
```sh
cd FYP-Codes
pip install -r requirements-main.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
sudo pip install -r requirements-main.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --break-system-packages
```

You must stop `NetworkManager` first, it will try to control WLAN interface created by `mininet-wifi`.
```sh

sudo systemctl stop NetworkManager # For this time
sudo systemctl disable --now NetworkManager # For all time
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

# Common error
## GUI, XDG\_RUNTIME\_DIR not set
```sh
echo "export XDG_RUNTIME_DIR=/run/user/$(id -u)" >> ~/.bashrc
```

Edit Makefile, change to:
```makefile
run:
    sudo -E PYTHONPATH=. python main.py
```
May fix this error.









