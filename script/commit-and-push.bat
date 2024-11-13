@echo off

:: Prompt for commit message
set /p commit="Masukan commit label: "

:: Stage changes, commit, and push
git add .
git commit -m "%commit%"
git push -u origin master

echo Changes pushed successfully.
