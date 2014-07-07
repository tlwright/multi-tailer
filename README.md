multi-tailer.py
===============

python 3 code example

Provides a multi-tailer for continuously updated logs which monitors
the log files and then emits the valid lines to standard output and the
invalid lines to standard error with some amount of re-odering to try
and give a coherent single timeline of log messages.

Run multi-tailer.py in one window and genlogs2.py in another.
When genlog2 finishes, press ctl-c in the multi-tailer window to stop it.

Tested on Mac OS X Version 10.9.4 with Python 3.4.1.
