#!/usr/bin/env python3 

# provide a multi-tailer for continuously updated logs which monitors
# the log files and then emits the valid lines to standard output and the
# invalid lines to standard error with some amount of re-odering to try
# and give a coherent single timeline of log messages.

# globals:
# logdir from command line -D: no default (required)
# maxwait in ms from cmdline -T: default 1000
# maxwaits in s: default 1, derived from maxwait
# beginning from cmdline -B: default False
# buf: dict with posix timestamp (seconds since unix epoch) for key
# fcount: count of log files
# fobjs: array of log file objects via open, fobjs[i].name re filename

debug = False
logdir = None
maxwait = 1000
maxwaits = 1
beginning = False
buf = {}
fcount = 0
fobjs = []

import sys, signal, glob, os, time, datetime, json

def handler(signum, frame):
    print ('Signal handler called with signal', signum)
    cleanup()
    sys.exit()

def startup():
    """ parse cmd line, find and open log files, setup signal handler """
    global logdir, maxwait, maxwaits, beginning, buf, fcount, fobjs

    from optparse import OptionParser
    [...]
    parser = OptionParser()
    parser.add_option("-D", dest="logdir",
                  help="log file directory", metavar="DIR")
    parser.add_option("-T", dest="maxwait",
                  help="max wait in ms", metavar="MAXWAIT", default=1000)
    parser.add_option("-B", dest="beginning", action="store_true",
                  help="read from beginning", default=False)

    (options, args) = parser.parse_args()

    if not options.logdir:
        parser.error("-D logdir must be specified")
        if args:
            print ("extra args", args, file=sys.stderr)
            parser.error("extra args not recognised")
    logdir = options.logdir
    maxwait = options.maxwait
    maxwaits = options.maxwait / 1000
    beginning = options.beginning

    # handle ctl-c and kill
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    # find logs
    logs = glob.glob(logdir+"/*.log")
    for file in logs:
        if os.path.isfile(file): # not a directory
            fh = open(file, 'r')
            fobjs.append(fh)
            fcount += 1
            if not beginning: fh.seek(0, os.SEEK_END)

def cleanup():
    """ empty buffer, close files """
    global fcount, fobjs
    putlines()
    for i in range(fcount): fobjs[i].close()

def validate(line):
    """ validate log record line via json, check for at and note """
    try:
        jsonobj = json.loads(line)
        if not "note" in jsonobj: 
            if debug: print("validate failed: no note")
            return False
        if not "at" in jsonobj: 
            if debug: print("validate failed: no at")
            return False
        if debug: print("validate ok")
        return True
    except ValueError: 
        if debug: print("validate failed: ValueError in try json.loads")
        return False

def timestamp(line):
    """ get timestamp from line via json if there (at), convert to seconds """
    """ if not there use current time """
    try:
        jsonobj = json.loads(line)
        if not "at" in jsonobj: return time.time()
        format = "%a %b %d %H:%M:%S %Z %Y"
        logtime = datetime.datetime.strptime(jsonobj["at"], format)
        return logtime.timeatamp()
    except ValueError: return time.time()

def prettyprint(line, fh):
    """ pretty print line (stdout) via json, prefix with filename """
    jsonobj = json.loads(line)
    print("input:", fh.name, 
          json.dumps(jsonobj, sort_keys=True, indent=4, separators=(',', ':')))

def unprettyprint(line):
    """ print line to stderr after escaping quotes and backslashes """
    s1 = line.replace('\\', '\\\\')
    s2 = s1.replace('\"', '\\"')
    print("# INVALID_LINE:", s2, file=sys.stderr) 

def getlines():
    """ get lines from log files, parse json, insert into buffer """
    global fcount, fobjs
    # tried using poll here but it always returned 1 (POLLIN)
    for i in range(fcount): 
        line = fobjs[i].readline()
        if line != '': # not eof
            valid = validate(line)
            if debug and not valid: print(line)
            ts = timestamp(line)
            if ts in buf: 
                buf[ts].append(line)
                buf[ts].append(valid)
                buf[ts].append(i)
            else: 
                buf[ts] = [line, valid, i]

def putlines():
    """ get lines from buffer, print valid to stdout, invalid to stderr """
    for ts in sorted(buf):
        while len(buf[ts]):
            line = buf[ts].pop(0)
            valid = buf[ts].pop(0)
            i = buf[ts].pop(0)
            if valid: prettyprint(line, fobjs[i])
            else: unprettyprint(line)
        del buf[ts] # no more lines for this timestamp

if __name__ == '__main__':
    startup()
    debug = False
    if debug:
        print("logdir=", logdir)
        print("maxwait=", maxwait)
        print("beginning=", beginning)
        print("buf=", buf)
        print("fcount=", fcount)
        print("fobjs=", fobjs)

    while True:
        getlines()
        putlines()
        time.sleep(maxwaits)
