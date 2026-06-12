# FT3D++

FT3D Rewrite

## Install dependencies
### Debian Linux packages
```sh
sudo apt install python3-matplotlib python3-numpy
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


## Run

### Linux
```sh
python3 src/main.py
```

### Windows
```sh
python src/main.py
```
