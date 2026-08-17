## Install dependencies

### Debian packages
```sh
sudo apt install python3-tk python3-matplotlib python3-numpy
```

### or from PyPI with pip

#### Linux
```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

#### Windows
```sh
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
venv\Scripts\activate
pip install -r requirements.txt
```
