@echo off
cd ..
echo "Current working dir is..."
cd

echo "Activating venv..."
call .\venv\Scripts\activate.bat

echo "Executing conversion script..."
python .\scripts\build_ui.py

echo "Conversion done... Press any key to exit."
pause
