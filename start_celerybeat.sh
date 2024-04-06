#!/bin/sh
# The watchmedo command is part of the watchdog Python package, which monitors file system events. Here, it's configured to automatically restart a given process (in this case, the celery worker process) when certain files change.
# The -d flag specifies the directories to watch, and the -p flag specifies the file patterns to watch. The -R flag tells watchmedo to watch recursively. The -- flag separates the watchmedo arguments from the command to run (celery -A config beat -l INFO).
watchmedo auto-restart -d apps/ -d config/  -p '*.py' -R -- celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
