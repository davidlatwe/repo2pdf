@echo off

set PATH="C:\Progra~1\wkhtmltopdf\bin";"C:\Progra~2\wkhtmltopdf\bin";%PATH%

python %~dp0repo2pdf.py %*
