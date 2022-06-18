@echo off

:: Pull the Nuke command from an environment variable. This command should
:: be set as an environment variable in the environment settings to
:: allow for easily changing the Nuke version.
"%IOG_NUKE_COMMAND%" -t "%~dp0\iognukepy_subcore.py" %*
