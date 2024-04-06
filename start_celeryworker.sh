#!/bin/sh
#  This line sets the environment variable PYTHONBREAKPOINT to celery.contrib.rdb.set_trace. This means that when Python hits a breakpoint() function call while running, it will use the Celery remote debugger, allowing you to debug tasks that run in Celery workers.
export PYTHONBREAKPOINT=celery.contrib.rdb.set_trace
# The watchmedo command is part of the watchdog Python package, which monitors file system events. Here, it's configured to automatically restart a given process (in this case, the celery worker process) when certain files change.
# The -d flag specifies the directories to watch, and the -p flag specifies the file patterns to watch. The -R flag tells watchmedo to watch recursively. The -- flag separates the watchmedo arguments from the command to run (celery -A config worker -l INFO).
watchmedo auto-restart -d apps/ -d config/  -p '*.py' -R -- celery -A config worker -l INFO
# optionally can specify the ques as: -Q celery
