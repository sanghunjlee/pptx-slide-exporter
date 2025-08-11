@echo off
pyinstaller --onefile --noconsole ^
    --name="PptxExporter" ^
    --icon=assets/icon.ico ^
    --add-data "assets;assets" ^
    main.py

echo Build complete! Check the dist/ folder.
pause
