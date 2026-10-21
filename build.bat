@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [1/2] 필요한 패키지 설치 중...
python -m pip install -r requirements-build.txt || goto :err
echo [2/2] exe 만드는 중...
python -m PyInstaller --onefile --clean --name PDF마스킹제거 pdf_unmask.py || goto :err
echo.
echo 완료: dist\PDF마스킹제거.exe
pause
exit /b 0
:err
echo 실패했습니다. Python이 설치돼 있는지 확인하세요. (python.org, 설치 시 "Add to PATH" 체크)
pause
exit /b 1
