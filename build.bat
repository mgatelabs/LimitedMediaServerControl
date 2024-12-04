rmdir  build /s /q
rmdir  dist /s /q
pyinstaller control.spec
copy dist\limitedmediaserver_control.exe .\limitedmediaserver_control.exe
call limitedmediaserver_control.exe