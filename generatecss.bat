@echo off
echo Generating Tailwind CSS...

:: Assuming tailwindcss.exe is now in the bin directory at the project root
tailwindcss.exe -i .\sortx\tailwind\styles.css -o .\sortx\assets\tailwind.css --minify 

echo Tailwind CSS generated successfully.
pause
