@echo off

:: The Nuke bin directory contains a python.exe executable compatible with
:: the Nuke libraries. As long as the Nuke bin directory is first in the
:: environment's PATH, this python executable will be found.
python.exe "%~dp0\iognukepy_subcore.py" %*
