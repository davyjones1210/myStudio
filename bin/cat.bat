echo "Hello world, test using cat.bat batch file"

if "%1"=="-open" (
    if "%2"=="blender4.3" python e:/pipelineDevelopment/myStudio/bin/cat.py
    if "%2"=="maya" python e:/pipelineDevelopment/myStudio/bin/cat-maya.py

)


