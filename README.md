# Macro Manager

## Wykonane przez:
- Michał Ślęzak 56113
- Adam Skawiński 55184



## Przed instalacją requirements.txt
```
Python: 1.13.X
virtualenv: 20.XX.X

```
## Wymagane biblioteki requirements.txt
### Plik requirements.txt jest automatycznie instalowany przy odpaleniu run.bat jeżeli folder .venv nie istnieje!

```requirements.txt
customtkinter==5.2.2
darkdetect==0.8.0
jsonpickle==4.1.1
packaging==25.0
pynput==1.8.1
six==1.17.0
```

## Instalacja i uruchomienie przez plik run.bat

```run.bat
{disc}:\{path}> run.bat 
```

### Jeżeli wirtualne środowisko nie istnieje:
- tworzy folder .venv (wirtualne środowisko)
- uruchamia wirtualne środowisko
- uruchamia plik main.py (./main.py)

### Jeżeli wirtualne środowisko istnieje:
- uruchamia wirtualne środowisko
- uruchamia plik main.py (./main.py)