set CWD=%cd%
set SCRIPT_DIR=%~dp0
set HOME_DIR=%SCRIPT_DIR%..

cd %HOME_DIR%
del /s /q dist\*
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist\*
cd %CWD%
