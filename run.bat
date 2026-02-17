@echo off
if not exist ".venv" (
    echo Creating venv...
    py -m venv .venv
    if errorlevel 1 (
        echo Cannot create venv
        exit /b 1
        pause
    )
    call .venv\Scripts\activate.bat

    if exist requirements.txt (
        echo Instaling requirements...
        py -m pip install --upgrade pip
        py -m pip install -r requirements.txt
        if errorlevel 1 (
            echo Cannot install
            pause
            exit /b 1
        )
    )
)
call .venv\Scripts\activate.bat

.venv\Scripts\python.exe -m main

pause