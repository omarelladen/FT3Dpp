# FT3D++

[FT3D](https://www.abenge.org.br/cobenge/legado/arquivos/18/trabalhos/NTM090.pdf)
rewrite

<p align="center" width="100%">
<img src="imgs/main.png">
</p>

## Install dependencies
### Debian Linux packages
```sh
sudo apt install python3-matplotlib python3-numpy python3-tk
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

## Features
### FT3D
- [x] Visual insertion in z plane
- [ ] Visual insertion in s plane
- [x] Insertion from coordinates in z plane
- [ ] Insertion from coordinates in s plane
- [ ] Transfer function insertion
- [x] Clear all insertions
- [x] Frame with poles and zeros coordinates
- [x] Magnitude plot for z plane
- [x] Magnitude plot in dB for z plane
- [x] Phase plot for z plane
- [ ] Magnitude plot for s plane
- [ ] Magnitude plot in dB for s plane
- [ ] Phase plot for s plane
- [ ] s <-> z mapping
- [x] 3D plot from z plane
- [ ] 3D plot from s plane
- [ ] 3D customization
- [x] 3D navigation
- [x] 2D plot navigation
- [x] Choose frequency response limits from z plane
- [ ] Choose frequency response limits from s plane
- [ ] Topography heat map plot
- [ ] Topography heat map customization
- [x] System classification
- [ ] System classification reasons
- [ ] Impulse response plot
- [ ] Step response plot
- [ ] Choose impulse response sample size
- [ ] Choose step response sample size
- [ ] Choose plane limits
- [x] Save plots
- [ ] Save system
- [x] Choose 2D plot colors
- [ ] Reset 2D plot colors
- [x] Show mouse coordinates below 2D plots
- [ ] Show magnitude value below z plane
- [ ] Show magnitude value below s plane
- [ ] Show magnitude and phase values below both plots
- [ ] Show exact frequency response at mouse x position
- [ ] Choose sample rate
- [ ] Calculate minimum phase system
- [ ] Calculate maximum phase system
- [ ] Calculate inverse phase system
- [ ] Undo insertion
- [ ] Redo insertion
- [ ] Undo mapping
- [ ] Redo mapping
- [ ] Shortcuts to close app, and to open and save files
- [ ] Button hints
- [ ] Help page
### New
- [x] Insertion from polar form in z plane
- [x] Choose frequency response resolution
- [x] Choose phase unit
- [x] Choose normalized frequency response
- [x] Labels for plane axes
- [ ] Shortcuts to undo and redo insertion
- [x] Choose transfer function format
- [x] Padding between related buttons
- [x] Window resize
- [ ] 2D plot resize along window resize
- [x] 3D plot resize along window resize
- [x] Save plot in multiple formats
- [x] Allow poles and zeros removal regardless of which one is selected
- [ ] Allow poles and zeros move regardless of which one is selected
- [ ] Show number of poles and zeros
- [x] Show mouse coordinates below 3D plots
- [ ] Choose to add spaces inside transfer function
- [ ] Choose font size of transfer function
- [ ] Choose font size of coordinates
- [x] No button duplication in menu
- [ ] Translations

## Credits
- Icons: The icons were extracted from FT3D
- 3D inspiration:
[Z-plane to Frequency Response](https://dspfirst.gatech.edu/chapters/08feedbac/demos/z2freq/index.html)

## License
[GPLv3](./LICENSE)

Copyright 2026 Omar Zagonel El Laden
