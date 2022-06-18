@echo off

:: Pull the Nuke EXE from an environment variable. This EXE should
:: be set as an environment variable in the environment settings to
:: allow for easily changing the Nuke version.
"%IOG_NUKE_EXE%" -t "%~dp0\iognukepy_subcore.py" %*
